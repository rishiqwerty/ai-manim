from app.llm_calls.gemini import start_conversation
from worker.manim import code_cleanup, code_runner
from datetime import datetime


def handle_llm_request(user_id, conversation_id, message, err="", retry=0):
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
    script_path = code_cleanup.save_code_to_file(code, f"temp_scripts/{user_id}_{conversation_id}_{current_time}.py")
    if not script_path:
        print("Failed to save the code to a file.")
        return {"error": "Failed to save the code."}
    # Format the code using Black
    code_cleanup.format_code_with_black(script_path)
    # Run the Manim script
    try:
        print(f"Running Manim script: {script_path}")
        video_file_path, err = code_runner.run_manim_script(script_path, f"{user_id}_{conversation_id}_{current_time}")
        if err:
            if retry >= 1:
                print(f"Failed to run Manim script after 3 retries: {err}")
                return {"error": "Failed to run the Manim script after multiple attempts."}
            retry += 1
            print(f"Error running Manim script: {err} retrying...{retry}")
            return handle_llm_request(user_id, conversation_id, code, err, retry)
    except Exception as e:
        print(f"Error running Manim script: {e}")
        return {"error": "Failed to run the Manim script."}

    print(f"Video generated successfully: {video_file_path}")
    return video_file_path
