from datetime import datetime
import os
from worker.manim import code_runner
from worker.celery_app import celery_app
from worker.tasks.code_generation_tasks import server_and_code_gen_bridge
from worker.aws.upload_to_s3 import upload_file_to_s3
from shared_models.database import SessionLocal
from shared_models.models import JobStatus, Job

@celery_app.task(name="tasks.video_rendering_tasks.run_manim_script")
def run_manim_script(script_path, user_id, conversation_id, code, retry=0):
    session = SessionLocal()
    try:
        job = session.query(Job).filter_by(conversation_id=conversation_id).first()
        if not job:
            print("Job not found for the given conversation and user.")
        print(f"Running Manim script: {script_path}")
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_file_path, err = code_runner.run_manim_script(script_path, f"{user_id}_{conversation_id}_{current_time}")
        if err:
            if retry >= 1:
                print(f"Failed to run Manim script after 3 retries: {err}")
                return {"error": "Failed to run the Manim script after multiple attempts."}
            retry += 1
            if job:
                print(f"Error running Manim script: {err} retrying...{retry}")
                job.status = JobStatus.pending
                job.updated_at = datetime.now()
                job.logs = f"Error running Manim script: {err}. Retrying...{retry}"
                session.commit()
                session.close()
            server_and_code_gen_bridge.apply_async(
                args=[user_id, conversation_id, code],
                queue="code_generation_queue",
                kwargs={"err": err, "retry": retry},
            )
        job.status = JobStatus.completed
        job.updated_at = datetime.now()
        job.video_path = video_file_path
        job.logs = "Video generated successfully."

        if os.environ.get("DEVELOPMENT") != "true":
            upload_file_to_s3(
                video_file_path,
                f"videos/{user_id}/{conversation_id}/{os.path.basename(video_file_path)}"
            )
            if video_file_path:
                os.remove(video_file_path)
        session.commit()
        session.close()
        
        
    except Exception as e:
        job = session.query(Job).filter_by(conversation_id=conversation_id).first()
        if not job:
            print("Job not found for the given conversation and user.")
        job.status = JobStatus.failed
        job.updated_at = datetime.now()
        job.logs = f"Error running Manim script: {str(e)}"
        session.commit()
        print(f"Error running Manim script: {e}")
        return {"error": "Failed to run the Manim script."}
    finally:
        session.close()
    print(f"Video generated successfully: {video_file_path}")
    return video_file_path