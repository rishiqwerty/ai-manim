import getpass
import os

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# system_message
# user_message
pre_prompt_instructions = """
You are a helpful assistant. When asked to write code, reply with the complete Python code only. 
Do not add any explanations, descriptions, or markdown code fences. 
Just output the raw, properly indented Python code.
Provide the proper code with all the necessary imports and functions.
Do not use any external libraries that are not already installed in the environment.
**Important:
- Use only the standard libraries and one relevant for manim.
- Manim version is 0.19.0. So write code compatible with this version only.
- Avoid writing code where it requires to create a temporary file Ex: Avoid using Code() since it requires temp file.
- Also make sure scene name in manim code will always be VideoScene.
"""

def start_conversation(text):
    print("Starting conversation with Google Gemini...")
    # Initialize the chat model
    text = pre_prompt_instructions + "\n" + text
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    response = model.invoke(text)
    return response.content
