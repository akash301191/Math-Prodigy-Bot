import tempfile, re
import streamlit as st
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    st.sidebar.markdown("---")

def render_solution_preferences():
    st.markdown("---")
    col1, col2 = st.columns([1, 1])  # Wider second column for preferences

    # Column 1: Image Upload
    with col1:
        st.subheader("🖼️ Upload Screenshot")
        uploaded_image = st.file_uploader(
            "Upload a screenshot of a math problem",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Solution Preferences
    with col2:
        st.subheader("🧮 Solution Preferences")

        explanation_detail = st.selectbox(
            "How detailed would you like the explanation to be?",
            ["Brief overview", "Standard step-by-step", "In-depth explanation with reasoning"],
        )

        practice_set = st.radio(
            "Would you like a set of similar problems for practice?",
            ["Yes", "No"],
            horizontal=True
        )

    return {
        "uploaded_image": uploaded_image,
        "explanation_detail": explanation_detail,
        "practice_set": practice_set
    }

def generate_solution(solution_preferences):
    # Save uploaded image to a temporary file
    uploaded_image = solution_preferences["uploaded_image"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    explanation_detail = solution_preferences["explanation_detail"]
    practice_set = solution_preferences["practice_set"]

    math_solver_agent = Agent(
        model=OpenAIChat(id="o4-mini", api_key=st.session_state.openai_api_key),
        name="Math Solver",
        role="A math tutor that solves problems from screenshots and provides explanations in varying depth based on the user's preference.",
        description=(
            "You are a helpful and accurate math tutor. Your task is to interpret the math problem shown in the uploaded image, "
            "solve it step-by-step, and explain it according to the chosen explanation detail. "
            "If requested, provide similar practice problems as well."
        ),
        instructions=[
            "Carefully read and understand the math problem from the uploaded image.",
            "Solve the problem methodically, building up to the final answer without revealing it at the beginning.",
            "Adapt the explanation style based on the user's selected preference:",
            "- For **Brief overview**: Focus on key steps only, no detailed reasoning.",
            "- For **Standard step-by-step**: Show all steps clearly with brief justifications.",
            "- For **In-depth explanation with reasoning**: Include detailed reasoning and concept-level insights for each step.",
            "If the user requested additional practice, include 2–3 similar math problems at the end.",
            "Follow this structured response format:\n\n"
            "### 🧮 Step-by-Step Breakdown\n"
            "<Break the problem down progressively>\n\n"
            "### 📘 Solution\n"
            "<Conclude with reasoning and final boxed answer>\n\n"
            "### 📝 Practice Problems (if requested)\n"
            "<Include 2–3 related problems with or without solutions>",
            "Only use what is visible in the image. Avoid assuming or fabricating any information.",
            "Format all math expressions clearly using Markdown and LaTeX."
        ],
        markdown=True
    )

    prompt = f"""
    A user has uploaded a screenshot of a math problem.

    Please solve it and provide a **{explanation_detail.lower()}** explanation, as per the defined explanation styles.

    The user has requested **{"similar problems for practice" if practice_set == "Yes" else "only the solution"}**.

    Structure your response clearly and format all math using Markdown and LaTeX.
    """

    response = math_solver_agent.run(prompt.strip(), images=[Image(filepath=image_path)])
    solution = response.content

    return solution

def convert_latex_to_markdown_format(text: str) -> str:
    """
    Converts LaTeX expressions wrapped in \(..\) or \[..\] to markdown-compatible
    formats using $..$ for inline and $$..$$ for block-level math.
    """
    # Convert block LaTeX: \[...\] → $$...$$
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)

    # Convert inline LaTeX: \(...\) → $...$
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text)

    return text

def main() -> None:
    # Page config
    st.set_page_config(page_title="Math Prodigy Bot", page_icon="🧮", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🧮 Math Prodigy Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Math Prodigy Bot — a Streamlit-powered learning tool that analyzes math problems from screenshots and provides complete, step-by-step solutions.",
        unsafe_allow_html=True
    )

    render_sidebar()
    solution_preferences = render_solution_preferences()

    st.markdown("---")

    # UI button to trigger solution generation
    if st.button("🧠 Generate Math Solution"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not solution_preferences["uploaded_image"]:
            st.error("Please upload a math problem screenshot to proceed.")
        else:
            with st.spinner("Solving your math problem..."):
                solution = generate_solution(solution_preferences)

                # Save results to session state
                st.session_state.solution = convert_latex_to_markdown_format(solution)
                st.session_state.image = solution_preferences["uploaded_image"]

    # Display result if available
    if "solution" in st.session_state and "image" in st.session_state:
        st.markdown("## 🖼️ Problem")
        st.image(st.session_state.image, use_container_width=False)

        st.markdown("## 🧮 Solution")
        st.write(st.session_state.solution)

        st.markdown("⚠️ **Disclaimer:** This bot may occasionally misinterpret or inaccurately solve certain math problems.Please review outputs before relying on them.")

        st.markdown("---")

        st.download_button(
            label="📥 Download Solution",
            data=st.session_state.solution,
            file_name="math_solution.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()


