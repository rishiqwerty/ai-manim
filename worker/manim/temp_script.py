import getpass
import os

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# system_message
# user_message

def start_conversation(text):
    print("Starting conversation with Google Gemini...")
    # Initialize the chat model
    model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    response = model.invoke(text)
    return response


# model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# memory = ConversationBufferMemory()

# conversation = ConversationChain(
#     llm=model,
#     memory=memory,
#     verbose=True,
# )

# # print(conversation.predict(input="Hello, My name is GPT?"))
# print(conversation.predict(input="Can you recall my name?"))
