from datetime import datetime
from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
from app.llm_calls.server_and_code_gen_bridge import handle_llm_request
router = APIRouter()

class Message(BaseModel):
    message: str
    # user: str
    # timestamp: str
    # id: int
    # conversation_id: int

messages = {}

@router.post("/{conversation_id}/message/")
def send_message(request:Request, conversation_id, message: Message, background_tasks: BackgroundTasks):
    """
    Start a new conversation.
    """
    # Initialize a new conversation if no converation_id is provided
    # If conversation_id is provided, append the message to the existing conversation

    # Create new conversation for user
    # Store session id for annonymous user?
    
    # After getting message and conversation, send this to background task?
    # This task will be responsible for generating the code based on the message
    # Then we will call the second task to run the manim code
    # and generate the video
    user_id = request.cookies.get("anonymous_id")
    actual_message = {
        "message": message.message,
        "timestamp": datetime.now().isoformat(),
    }
    if not user_id:
        return {"error": "User not found."}
    if not conversation_id:
        # Create a new conversation
        if not user_id in messages:
            messages[user_id] = {conversation_id: [actual_message]}
    else:
        if not user_id in messages:
            messages[user_id] = {}
        if conversation_id not in messages[user_id]:
            messages[user_id][conversation_id] = []
        messages[user_id][conversation_id].append(actual_message)
    background_tasks.add_task(
        handle_llm_request, user_id, conversation_id, message.message
    )
    return {"message": "Video processing started. Comeback later to check the status."}

@router.get("/{conversation_id}/messages/")
def get_messages(conversation_id: str, request: Request):
    """
    Get all messages for a conversation.
    """
    print(messages)
    # Return all messages for the conversation
    # If conversation_id is not provided, return all messages for the user
    user_id = request.cookies.get("anonymous_id")
    if user_id in messages:
        return messages[user_id].get(conversation_id, [])
    else:
        return {"error": "Conversation not found."}

# Once code is generated, we store it in s3, and provide the code to a docker container
# that will run the manim code and generate the video

# Add credit based system for each user for video generation