# ai-manim
LLM based tech concept animator

Pre:
ffmpeg
Installation
- for pycairo need to install  `brew install cairo pkg-config`

need to add poetry
[tool.poetry.dependencies]
python = "^3.7"

For langchain 
poetry add --allow-prereleases langchain-text-splitters



User sends prompt - > store it as a background task
User sign in 


Once user is done with chat, Clean up and summarize the text and store in db

store per user's project wise conversation in chat_history table, limit the history


Annoynomous user -> makes request ->