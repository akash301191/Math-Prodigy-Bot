# Math Prodigy Bot

Math Prodigy Bot is a smart Streamlit application that helps you solve math problems from screenshots with step-by-step explanations. Powered by [Agno](https://github.com/agno-agi/agno) and OpenAI's o4-mini, the bot reads your uploaded image, understands the math problem, and generates a complete solution — optionally including similar problems for practice.

## Folder Structure

```
Math-Prodigy-Bot/
├── math-prodigy-bot.py
├── README.md
└── requirements.txt
```

- **math-prodigy-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Screenshot-Based Input**  
  Upload an image of a math problem — typed or handwritten — and let the bot interpret it visually.

- **Step-by-Step Solutions**  
  Choose your preferred explanation depth: brief, standard, or in-depth — and receive the solution accordingly.

- **Practice Problem Generator**  
  Optionally receive a set of similar math problems for continued practice and learning reinforcement.

- **Clean LaTeX Formatting**  
  Solutions are rendered in markdown with properly formatted LaTeX expressions for mathematical clarity.

- **Download Option**  
  Download the generated solution as a `.md` file to keep a copy of the explanation and practice set.

- **Streamlit UI**  
  Built with Streamlit for a fast, focused, and responsive experience.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Math-Prodigy-Bot.git
   cd Math-Prodigy-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run math-prodigy-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI API key in the sidebar.
   - Upload a screenshot of a math problem.
   - Choose your explanation detail and whether you'd like extra practice.
   - Click **🧠 Generate Math Solution**.
   - View and download the full solution.

3. **Download Option**  
   Use the **📥 Download Solution** button to save your work as a Markdown file.

---

## Code Overview

- **`render_sidebar()`**: Accepts and stores the OpenAI API key in session state.
- **`render_solution_preferences()`**: Captures the uploaded screenshot and user preferences.
- **`generate_solution()`**:  
  - Sends the image to a math-solving agent via Agno.  
  - Returns a structured response with solution steps and optional practice problems.
- **`convert_latex_to_markdown_format()`**: Converts LaTeX expressions from `\(...\)` and `\[...\]` to markdown-compatible `$...$` and `$$...$$`.
- **`main()`**: Coordinates layout, handles interaction flow, and manages final output rendering.

## Contributions

Contributions are welcome! Feel free to fork the repo, report bugs, suggest improvements, or open a pull request. Make sure your changes are clean, well-tested, and align with the learning-focused vision of this tool.
