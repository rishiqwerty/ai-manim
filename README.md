
---

📽️ AI-Manim Code Generator

This is a simple AI-powered Manim animation generator.
It uses a language model (LLM) to generate Manim code from text prompts, cleans and formats the code, runs it to render videos, and serves the video output.


---

### 📦 Features

🔤 Prompt-based Manim code generation using LLM

🧹 Automatic cleanup of generated code

📝 Forced consistent Scene class name (GeneratedScene) for reliable rendering

🎥 Runs Manim CLI to render videos

🧯 Handles rendering errors and LaTeX failures gracefully

📦 Stores prompts, generated code, status, and video paths in a database



---

### 📐 Tech Stack

FastAPI for API server

Manim for animation rendering

Gemini (or any LLM API) for code generation

subprocess for safe Manim CLI execution

---

### 🚀 How it works

1. User submits a text prompt


2. LLM generates Manim code (Text/LaTeX animations)


3. The code is cleaned, validated, and wrapped.


4. Manim CLI renders the scene to a video file


5. Video path is stored and returned to the user


6. Errors are captured and reported via prompt status updates




---

### ⚙️ Requirements
- Python 3.12+
- Poetry
- Manim Community Edition
- Gemini API key (or any LLM API)
- ffmpeg
- pycairo
- LaTeX installed (if using Tex / MathTex animations)


On macOS:

brew install --cask mactex

On Ubuntu:

sudo apt-get install texlive-full


---

📦 Install Dependencies

poetry install


---

🏃‍♂️ Run the Server

uvicorn main:app --reload





















<!-- # ai-manim
LLM based tech concept animator
Miscellaneous
Pre:
ffmpeg
Installation
- for pycairo need to install  `brew install cairo pkg-config`
- also install mactex for latex

need to add poetry
[tool.poetry.dependencies]
python = "^3.7"

For langchain 
poetry add --allow-prereleases langchain-text-splitters



User sends prompt - > store it as a background task
User sign in 


Once user is done with chat, Clean up and summarize the text and store in db

store per user's project wise conversation in chat_history table, limit the history


Annoynomous user -> makes request -> -->