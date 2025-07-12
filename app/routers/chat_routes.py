from datetime import datetime
from fastapi import APIRouter, Request, BackgroundTasks, Depends
from pydantic import BaseModel
from shared_models.models import Conversation, Message, Job
# from app.llm_calls.server_and_code_gen_bridge import handle_llm_request
from app.celery_app import celery_app
from sqlalchemy.orm import Session
from shared_models.database import get_db
router = APIRouter()

class MessageSerializer(BaseModel):
    message: str
    # user: str
    # timestamp: str
    # id: int
    # conversation_id: int

@router.post("/{conversation_id}/message/")
def send_message(request:Request, conversation_id, message: MessageSerializer, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
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
    conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return {"error": "Conversation not found."}
    db_message = Message(
        conversation_id=conversation_id,
        message_type="user",
        content=message.message,
        created_at=datetime.now(),
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    job = Job(
        conversation_id=conversation_id,
        created_at=datetime.now(),
        status="pending"
    )
    db.add(job)
    db.commit()

    # background_tasks.add_task(
    #     handle_llm_request, user_id, conversation_id, message.message
    # )
    celery_app.send_task(
        "tasks.code_generation_tasks.generate_code",
        args=[user_id, conversation_id, message.message],
        queue="code_generation_queue",
        kwargs={"err": "", "retry": 0},
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

@router.post("/conversation/")
def create_conversation(request: Request, db: Session = Depends(get_db)):
    """
    Create a new conversation.
    """
    user_id = request.cookies.get("anonymous_id")
    if not user_id:
        return {"error": "User not found."}
    
    # Create a new conversation
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return {"conversation_id": conversation.id, "message": "Conversation created successfully."}

@router.get("/jobs/status/{conversation_id}")
def get_job_status(conversation_id: str, request: Request, db: Session = Depends(get_db)):
    """
    Get the status of the job for a conversation.
    """
    user_id = request.cookies.get("anonymous_id")
    if not user_id:
        return {"error": "User not found."}
    
    # Get the job status for the conversation
    job = db.query(Job).filter_by(conversation_id=conversation_id).first()
    if not job:
        return {"error": "Job not found."}
    
    return {
        "status": job.status,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
        "video_path": job.video_path,
        "logs": job.logs
    }
#router
# Once code is generated, we store it in s3, and provide the code to a docker container
# that will run the manim code and generate the video

# Add credit based system for each user for video generation