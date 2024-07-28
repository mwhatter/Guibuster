import os
import subprocess
import sys

VENV_DIR = "venv"

# Color scheme
BG_COLOR = "#001f1f"
FG_COLOR = "#2FFFA3"

def is_running_in_venv():
    return sys.prefix != sys.base_prefix

def setup_virtual_environment():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe' if os.name == 'nt' else 'bin', 'python')
    subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python_executable, "-m", "pip", "install", "tk"])

def check_and_activate_venv():
    if not is_running_in_venv():
        setup_virtual_environment()
        python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe' if os.name == 'nt' else 'bin', 'python')
        subprocess.run([python_executable] + sys.argv)
        sys.exit(0)

check_and_activate_venv()
import tkinter as tk

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guibuster Main")
        self.root.geometry("400x300")
        self.root.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.root, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Guibuster", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Run DIR", command=lambda: self.run_script("Guibuster_dir.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Run VHOST", command=lambda: self.run_script("Guibuster_vhost.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Run FUZZ", command=lambda: self.run_script("Guibuster_fuzz.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Run S3", command=lambda: self.run_script("Guibuster_s3.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Run GCS", command=lambda: self.run_script("Guibuster_gcs.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Run TFTP", command=lambda: self.run_script("Guibuster_tftp.py"), bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Cancel", command=self.root.quit, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    def run_script(self, script_name):
        subprocess.Popen([sys.executable, script_name])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
