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

class GobusterMain:
    def __init__(self, root):
        self.root = root
        self.root.title("Gobuster Interface")
        self.root.geometry("400x400")
        self.root.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.root, bg=BG_COLOR)
        title_frame.pack(pady=20)
        tk.Label(title_frame, text="Gobuster Interface", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=20)

        self.create_command_button(button_frame, "DNS Subcommand", "Gobuster_dns.py", 0)
        self.create_command_button(button_frame, "DIR Subcommand", "Gobuster_dir.py", 1)
        self.create_command_button(button_frame, "VHOST Subcommand", "Gobuster_vhost.py", 2)
        self.create_command_button(button_frame, "FUZZ Subcommand", "Gobuster_fuzz.py", 3)
        self.create_command_button(button_frame, "S3 Subcommand", "Gobuster_s3.py", 4)
        self.create_command_button(button_frame, "GCS Subcommand", "Gobuster_gcs.py", 5)
        self.create_command_button(button_frame, "TFTP Subcommand", "Gobuster_tftp.py", 6)

    def create_command_button(self, parent, text, script, row):
        tk.Button(parent, text=text, command=lambda: self.run_script(script), bg=BG_COLOR, fg=FG_COLOR, width=20).grid(row=row, column=0, padx=5, pady=5)

    def run_script(self, script):
        subprocess.Popen([sys.executable, script])

if __name__ == "__main__":
    root = tk.Tk()
    app = GobusterMain(root)
    root.mainloop()
