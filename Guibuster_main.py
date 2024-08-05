import os
import subprocess
import sys
import tkinter as tk

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

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guibuster Main")
        self.root.geometry("420x420")
        self.root.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.root, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Guibuster", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=10)

        self.create_mode_button(button_frame, "Run DIR", "Directory enumeration mode", "Guibuster_dir.py", 0, 0)
        self.create_mode_button(button_frame, "Run VHOST", "VHOST enumeration mode", "Guibuster_vhost.py", 0, 1)
        self.create_mode_button(button_frame, "Run DNS", "DNS subdomain enumeration mode", "Guibuster_dns.py", 1, 0)
        self.create_mode_button(button_frame, "Run FUZZ", "Fuzzing mode", "Guibuster_fuzz.py", 1, 1)
        self.create_mode_button(button_frame, "Run S3", "AWS bucket enumeration mode", "Guibuster_s3.py", 2, 0)
        self.create_mode_button(button_frame, "Run TFTP", "TFTP enumeration mode", "Guibuster_tftp.py", 2, 1)
        self.create_mode_button(button_frame, "Run GCS", "Google Cloud bucket enumeration mode", "Guibuster_gcs.py", 3, 0)
        
        # Added Cancel button at the end
        self.create_mode_button(button_frame, "Cancel", "Exit the application", None, 3, 1, is_cancel=True)

    def create_mode_button(self, frame, text, description, script_name, row, col, is_cancel=False):
        tk.Label(frame, text=description, fg=FG_COLOR, bg=BG_COLOR).grid(row=row * 2, column=col, pady=5)
        if is_cancel:
            tk.Button(frame, text=text, command=self.root.quit, bg=BG_COLOR, fg=FG_COLOR, height=2, width=15).grid(row=row * 2 + 1, column=col, padx=10, pady=5)
        else:
            tk.Button(frame, text=text, command=lambda: self.run_script(script_name), bg=BG_COLOR, fg=FG_COLOR, height=2, width=15).grid(row=row * 2 + 1, column=col, padx=10, pady=5)

    def run_script(self, script_name):
        subprocess.Popen([sys.executable, script_name])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
