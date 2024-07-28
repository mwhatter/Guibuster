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
from tkinter import messagebox

class ScrollableHelpWindow:
    def __init__(self, parent, title, help_text):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.configure(bg=BG_COLOR)
        
        frame = tk.Frame(self.window, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(frame, wrap=tk.WORD, bg=BG_COLOR, fg=FG_COLOR)
        self.text_widget.insert(tk.END, help_text)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(self.window, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

class DNSWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Gobuster DNS")
        self.window.geometry("800x600")
        self.window.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.window, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Gobuster DNS", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        command_frame = tk.Frame(self.window, bg=BG_COLOR)
        command_frame.pack(pady=10)

        self.create_dns_section(command_frame)

        button_frame = tk.Frame(self.window, bg=BG_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Help", command=self.show_help, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=1, padx=5, pady=5)

    def create_dns_section(self, parent_frame):
        dns_frame = tk.LabelFrame(parent_frame, text="DNS Subcommand", fg=FG_COLOR, bg=BG_COLOR, font=("Helvetica", 12, "bold"), width=600)
        dns_frame.pack(pady=10)

        self.dns_checkbuttons = {}
        self.dns_entries = {}

        flags_with_entries = ["-d", "-r", "--timeout", "--delay", "-o", "-p", "-t", "-w"]
        flags_without_entries = ["-c", "-i", "--wildcard", "--no-color", "--no-error", "-z", "-q", "-v"]

        boolean_frame = tk.Frame(dns_frame, bg=BG_COLOR)
        boolean_frame.pack(pady=5)

        for i, flag in enumerate(flags_without_entries):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(boolean_frame, text=flag, variable=var, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
            chk.grid(row=i//4, column=i%4, padx=5, pady=2, sticky='w')
            self.dns_checkbuttons[flag] = var

        entry_frame = tk.Frame(dns_frame, bg=BG_COLOR)
        entry_frame.pack(pady=5)

        for i, flag in enumerate(flags_with_entries):
            tk.Label(entry_frame, text=flag, fg=FG_COLOR, bg=BG_COLOR).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            entry = tk.Entry(entry_frame, bg=BG_COLOR, fg=FG_COLOR)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            self.dns_entries[flag] = entry

        tk.Button(dns_frame, text="Run DNS", command=self.run_dns, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    def show_help(self):
        help_text = """\
DNS Subcommand:
  -d, --domain string      The target domain
  -r, --resolver string    Use custom DNS server (format server.com or server.com:port)
  -c, --show-cname         Show CNAME records (cannot be used with '-i' option)
  -i, --show-ips           Show IP addresses
      --timeout duration   DNS resolver timeout (default 1s)
      --wildcard           Force continued operation when wildcard found

Global Flags:
      --delay duration    Time each thread waits between requests (e.g. 1500ms)
      --no-color          Disable color output
      --no-error          Don't display errors
  -z, --no-progress       Don't display progress
  -o, --output string     Output file to write results to (defaults to stdout)
  -p, --pattern string    File containing replacement patterns
  -q, --quiet             Don't print the banner and other noise
  -t, --threads int       Number of concurrent threads (default 10)
  -v, --verbose           Verbose output (errors)
  -w, --wordlist string   Path to the wordlist

Examples:
gobuster dns -d mysite.com -t 50 -w common-names.txt
"""
        ScrollableHelpWindow(self.root, "DNS Help", help_text)

    def run_dns(self):
        command = ["gobuster", "dns"]
        for flag, var in self.dns_checkbuttons.items():
            if var.get():
                command.append(flag)
        for flag, entry in self.dns_entries.items():
            value = entry.get().strip()
            if value:
                command.extend([flag, value])
        self.execute_command(command)

    def execute_command(self, command):
        output = os.popen(" ".join(command)).read()
        messagebox.showinfo("Command Output", output)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = DNSWindow(root)
    root.mainloop()
