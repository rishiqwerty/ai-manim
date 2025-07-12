import subprocess
import os

OUTPUT_DIR = os.environ.get("OUTPUT_PATH")

# If script failed provide error message to llm and retry

def run_manim_script(script_path, scene_name):
    try:
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Build Manim CLI command
        command = [
            "manim",
            "-pql",
            script_path,
            scene_name,
            "--media_dir",
            OUTPUT_DIR
        ]

        # Run subprocess safely
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Manim rendering failed:\n{result.stderr}")

        # Video path (by Manim default structure)
        video_file_path = os.path.join(
            OUTPUT_DIR, "videos", scene_name, "480p15", f"VideoScene.mp4"
        )

        if not os.path.exists(video_file_path):
            raise FileNotFoundError(f"Expected video file not found: {video_file_path}")

        return video_file_path, ""
    except Exception as e:
        print(f"Error running Manim script: {e}")
        return None, str(e)
