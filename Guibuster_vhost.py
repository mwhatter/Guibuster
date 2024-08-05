import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

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

class VHOSTWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Guibuster VHOST")
        self.window.geometry("800x550")  # Increased height for better spacing
        self.window.configure(bg=BG_COLOR)

        title_frame = tk.Frame(self.window, bg=BG_COLOR)
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Guibuster VHOST", font=("Helvetica", 20, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack()

        command_frame = tk.Frame(self.window, bg=BG_COLOR)
        command_frame.pack(pady=10)

        self.create_vhost_section(command_frame)

        button_frame = tk.Frame(self.window, bg=BG_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Help", command=self.show_help, bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=1, padx=5, pady=5)

    def create_vhost_section(self, parent_frame):
        vhost_frame = tk.LabelFrame(parent_frame, text="VHOST Subcommand", fg=FG_COLOR, bg=BG_COLOR, font=("Helvetica", 12, "bold"), width=600)
        vhost_frame.pack(pady=10)

        self.vhost_checkbuttons = {}
        self.vhost_entries = {}

        # Target URL
        tk.Label(vhost_frame, text="Target URL (-u)", fg=FG_COLOR, bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.vhost_entries["-u"] = tk.Entry(vhost_frame, bg=BG_COLOR, fg=FG_COLOR, width=50)
        self.vhost_entries["-u"].grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky='w')

        # Path to Wordlist
        tk.Label(vhost_frame, text="Path to Wordlist (-w)", fg=FG_COLOR, bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        default_wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"  # Adjust this path if necessary
        self.vhost_entries["-w"] = tk.Entry(vhost_frame, bg=BG_COLOR, fg=FG_COLOR, width=50)
        self.vhost_entries["-w"].insert(0, default_wordlist)
        self.vhost_entries["-w"].grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky='w')

        # Boolean Flags in one row
        flags_without_entries = ["--no-color", "--no-error", "-z", "-q", "-v"]
        boolean_frame = tk.Frame(vhost_frame, bg=BG_COLOR)
        boolean_frame.grid(row=2, column=0, columnspan=4, pady=5)

        for i, flag in enumerate(flags_without_entries):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(boolean_frame, text=flag, variable=var, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
            chk.grid(row=0, column=i, padx=5, pady=2, sticky='w')
            self.vhost_checkbuttons[flag] = var

        # Textbox Flags, max 7 rows
        flags_with_entries = ["--append-domain", "-c", "--cookies", "--domain", "--exclude-length", "-r", "-H", "-m", "-k", "-P", "--proxy", "--random-agent", "--retry", "--retry-attempts", "--timeout", "-a", "-U", "-o", "-p", "-t"]
        entry_frame = tk.Frame(vhost_frame, bg=BG_COLOR)
        entry_frame.grid(row=3, column=0, columnspan=4, pady=5)

        for i, flag in enumerate(flags_with_entries):
            tk.Label(entry_frame, text=flag, fg=FG_COLOR, bg=BG_COLOR).grid(row=i%7, column=(i//7)*2, padx=5, pady=2, sticky='w')
            entry = tk.Entry(entry_frame, bg=BG_COLOR, fg=FG_COLOR)
            entry.grid(row=i%7, column=(i//7)*2+1, padx=5, pady=2, sticky='w')
            self.vhost_entries[flag] = entry

        # Proxychains checkbox
        self.proxychains_var = tk.BooleanVar()
        tk.Checkbutton(vhost_frame, text="Use Proxychains", variable=self.proxychains_var, fg=FG_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR).grid(row=4, column=0, padx=5, pady=5, sticky='w')

        tk.Button(vhost_frame, text="Run VHOST", command=self.run_vhost, bg=BG_COLOR, fg=FG_COLOR).grid(row=5, column=0, columnspan=4, pady=10)

    def show_help(self):
        help_text = """\
VHOST Subcommand:
  --append-domain              Append main domain from URL to words from wordlist. Otherwise the fully qualified domains need to be specified in the wordlist.
  -c, --cookies string         Cookies to use for the requests
  --domain string              The domain to append when using an IP address as URL. If left empty and you specify a domain based URL the hostname from the URL is extracted
      --exclude-length ints    Exclude the following content length (completely ignores the status). Supply multiple times to exclude multiple sizes.
  -r, --follow-redirect        Follow redirects
  -H, --headers stringArray    Specify HTTP headers, -H 'Header1: val1' -H 'Header2: val2'
  -m, --method string          Use the following HTTP method (default "GET")
  -k, --no-tls-validation      Skip TLS certificate verification
  -P, --password string        Password for Basic Auth
      --proxy string           Proxy to use for requests [http(s)://host:port]
      --random-agent           Use a random User-Agent string
      --retry                  Should retry on request timeout
      --retry-attempts int     Times to retry on request timeout (default 3)
      --timeout duration       HTTP Timeout (default 10s)
  -u, --url string             The target URL
  -a, --useragent string       Set the User-Agent string (default "gobuster/3.2.0")
  -U, --username string        Username for Basic Auth

Global Flags:
      --delay duration         Time each thread waits between requests (e.g. 1500ms)
      --no-color               Disable color output
      --no-error               Don't display errors
  -z, --no-progress            Don't display progress
  -o, --output string          Output file to write results to (defaults to stdout)
  -p, --pattern string         File containing replacement patterns
  -q, --quiet                  Don't print the banner and other noise
  -t, --threads int            Number of concurrent threads (default 10)
  -v, --verbose                Verbose output (errors)
  -w, --wordlist string        Path to the wordlist"""

        ScrollableHelpWindow(self.window, "VHOST Help", help_text)

    def run_vhost(self):
        command = ["gobuster", "vhost"]

        if self.proxychains_var.get():
            command.insert(0, "proxychains")

        for flag, var in self.vhost_checkbuttons.items():
            if var.get():
                command.append(flag)

        for flag, entry in self.vhost_entries.items():
            value = entry.get().strip()
            if value:
                command.extend([flag, value])

        print("Running command:", " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True)
        messagebox.showinfo("Command Output", result.stdout)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = VHOSTWindow(root)
    root.mainloop()
