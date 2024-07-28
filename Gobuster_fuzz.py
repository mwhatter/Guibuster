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

class FUZZWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Gobuster FUZZ")
        self.window.geometry("800x600")
        self.window.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.window, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Gobuster FUZZ", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        command_frame = tk.Frame(self.window, bg=BG_COLOR)
        command_frame.pack(pady=10)

        self.create_fuzz_section(command_frame)

        button_frame = tk.Frame(self.window, bg=BG_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Help", command=self.show_help, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=1, padx=5, pady=5)

    def create_fuzz_section(self, parent_frame):
        fuzz_frame = tk.LabelFrame(parent_frame, text="FUZZ Subcommand", fg=FG_COLOR, bg=BG_COLOR, font=("Helvetica", 12, "bold"), width=600)
        fuzz_frame.pack(pady=10)

        self.fuzz_checkbuttons = {}
        self.fuzz_entries = {}

        flags_with_entries = ["-u", "-c", "--exclude-length", "-H", "-m", "-P", "--proxy", "--timeout", "-a", "-U", "--delay", "-o", "-p", "-t", "-w"]
        flags_without_entries = ["-r", "--follow-redirect", "--random-agent", "--retry", "-k", "--no-tls-validation", "--no-error", "-z", "-q", "-v"]

        boolean_frame = tk.Frame(fuzz_frame, bg=BG_COLOR)
        boolean_frame.pack(pady=5)

        for i, flag in enumerate(flags_without_entries):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(boolean_frame, text=flag, variable=var, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
            chk.grid(row=i//4, column=i%4, padx=5, pady=2, sticky='w')
            self.fuzz_checkbuttons[flag] = var

        entry_frame = tk.Frame(fuzz_frame, bg=BG_COLOR)
        entry_frame.pack(pady=5)

        for i, flag in enumerate(flags_with_entries):
            tk.Label(entry_frame, text=flag, fg=FG_COLOR, bg=BG_COLOR).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            entry = tk.Entry(entry_frame, bg=BG_COLOR, fg=FG_COLOR)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            self.fuzz_entries[flag] = entry

        tk.Button(fuzz_frame, text="Run FUZZ", command=self.run_fuzz, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

    def show_help(self):
        help_text = """\
FUZZ Subcommand:
  -c, --cookies string              Cookies to use for the requests
      --exclude-length ints         Exclude the following content length (completely ignores the status). Supply multiple times to exclude multiple sizes.
  -b, --excludestatuscodes string   Negative status codes (will override statuscodes if set)
  -r, --follow-redirect             Follow redirects
  -H, --headers stringArray         Specify HTTP headers, -H 'Header1: val1' -H 'Header2: val2'
  -h, --help                        Help for fuzz
  -m, --method string               Use the following HTTP method (default "GET")
  -k, --no-tls-validation           Skip TLS certificate verification
  -P, --password string             Password for Basic Auth
      --proxy string                Proxy to use for requests [http(s)://host:port]
      --random-agent                Use a random User-Agent string
      --retry                       Should retry on request timeout
      --retry-attempts int          Times to retry on request timeout (default 3)
      --timeout duration            HTTP Timeout (default 10s)
  -u, --url string                  The target URL
  -a, --useragent string            Set the User-Agent string (default "gobuster/3.2.0")
  -U, --username string             Username for Basic Auth

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
gobuster fuzz -u https://example.com?FUZZ=test -w parameter-names.txt
"""
        ScrollableHelpWindow(self.root, "FUZZ Help", help_text)

    def run_fuzz(self):
        command = ["gobuster", "fuzz"]
        for flag, var in self.fuzz_checkbuttons.items():
            if var.get():
                command.append(flag)
        for flag, entry in self.fuzz_entries.items():
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
    app = FUZZWindow(root)
    root.mainloop()
