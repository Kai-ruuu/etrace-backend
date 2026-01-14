import sys
import subprocess

if __name__ == "__main__":
    command = ["uvicorn", "app.main:app"]
    
    if "-d" in sys.argv:
        command.append("--reload")
    
    subprocess.run(command)

