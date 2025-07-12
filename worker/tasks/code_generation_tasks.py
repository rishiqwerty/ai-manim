from datetime import datetime
import os
from worker.celery_app import celery_app
from worker.manim import code_cleanup
from worker.llm.gemini import start_conversation
from worker.aws.upload_to_s3 import upload_code_to_s3

@celery_app.task(name="tasks.code_generation_tasks.generate_code")
def server_and_code_gen_bridge(user_id, conversation_id, message, retry=0, err=""):
    """
    This task serves as a bridge between the server and code generation processes.
    It can be used to handle tasks that require interaction with both the server and code generation components.
    """
    run_code_generation_and_cleanup(user_id, conversation_id, message, err, retry)
    

    

    
def run_code_generation_and_cleanup(user_id, conversation_id, message, err="", retry=0):
    """
    Handles the request to the LLM and processes the response.
    This function is called by the FastAPI route handler.
    """
    if err:
        print(f"Error running the Manim script: {err}. Retrying...{retry}")
        message = f"Got error running the Manim script: {err}. Please fix the code and try again.\n\n{message}"
    # Call the LLM with the provided message
    response = start_conversation(message)

    # Extract code from the response
    print("Starting code extraction from the response...", response)
    code = code_cleanup.extract_code(response)
    if not code:
        print("No code found in the response.")
        return {"error": "No valid code found in the response."}
    # Save the code to a temporary file
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    if os.environ.get("DEVELOPMENT") != "true":
        script_path = upload_code_to_s3(
            file_content=code,
            s3_key=f"code/{user_id}/{conversation_id}/{user_id}_{conversation_id}_{current_time}.py"
        )
    else:
        script_path = code_cleanup.save_code_to_file(code, f"{user_id}_{conversation_id}_{current_time}.py")
    if not script_path:
        print("Failed to save the code to a file.")
        return {"error": "Failed to save the code."}
    # Format the code using Black
    code_cleanup.format_code_with_black(script_path)
    # Run the Manim script

    from worker.tasks.video_rendering_tasks import run_manim_script
    run_manim_script.apply_async(
        args=[script_path, user_id, conversation_id, code],
        queue="video_render_queue",
        kwargs={"retry": retry},
        )
    
    
