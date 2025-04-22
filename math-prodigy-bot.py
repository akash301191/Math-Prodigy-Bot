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
        role="Solves math problems from screenshots and explains them in a student-friendly manner.",
        description=(
            "You are a helpful math tutor who reads math problems from screenshots "
            "and generates step-by-step explanations based on the user's preference. "
            "You may also generate similar practice problems if requested."
        ),
        instructions=[
            "Start by analyzing the uploaded image to extract the math problem accurately.",
            "Then solve the problem step-by-step based on the selected explanation detail.",
            "Do NOT show the final answer at the beginning. Build toward it gradually through steps.",
            "Use the following response format:\n\n"
            "### 🧮 Step-by-Step Breakdown\n"
            "<Break the problem down clearly and methodically>\n\n"
            "### 📘 Solution\n"
            "<Explain the logic used in each step and present the final answer at the end>\n\n"
            "### 📝 Practice Problems (if requested)\n"
            "<Provide 2–3 similar math problems with or without answers>",
            "Avoid fabricating data or introducing assumptions not visible in the screenshot.",
            "Use clean markdown formatting and LaTeX for math symbols where helpful."
        ],
        markdown=True
    )

    prompt = f"""
    A user has uploaded a screenshot of a math problem.

    Solve the problem and provide a **{explanation_detail.lower()}** solution.

    The user has requested **{"a set of similar problems for practice" if practice_set == "Yes" else "only the solution"}**.
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


