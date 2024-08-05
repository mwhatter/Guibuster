import os
import subprocess
import sys
import platform
import shutil

VENV_DIR = "venv"
REPO_URL = "https://github.com/yourusername/guibuster.git"
WORDLIST_URL = "https://github.com/danielmiessler/SecLists/raw/master/Discovery/DNS/common.txt"

def is_windows():
    return platform.system().lower() == "windows"

def is_linux():
    return platform.system().lower() == "linux"

def check_prerequisites():
    """Check if Python, Go, and Git are installed. Install Git if missing."""
    try:
        subprocess.check_call(["python", "--version"])
    except subprocess.CalledProcessError:
        print("Python is not installed. Please install it and rerun this script.")
        sys.exit(1)
    
    try:
        subprocess.check_call(["go", "version"])
    except subprocess.CalledProcessError:
        print("Go is not installed. Please install it and rerun this script.")
        sys.exit(1)

    if not check_git_installed():
        install_git()

def check_git_installed():
    """Check if Git is installed."""
    try:
        subprocess.check_call(["git", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False

def install_git():
    """Install Git on Windows or Linux."""
    if is_windows():
        print("Installing Git on Windows...")
        git_installer = "Git-2.37.1-64-bit.exe"
        subprocess.check_call(["powershell", "-Command", 
                               f"Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.37.1.windows.1/{git_installer} -OutFile {git_installer}"])
        subprocess.check_call([git_installer, "/VERYSILENT", "/NORESTART"])
        os.remove(git_installer)
    elif is_linux():
        print("Installing Git on Linux...")
        subprocess.check_call(["sudo", "apt-get", "update"])
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "git"])
    else:
        print("Unsupported OS. Please install Git manually.")
        sys.exit(1)

def setup_virtual_environment():
    """Set up a Python virtual environment."""
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

def activate_virtual_environment():
    """Activate the Python virtual environment."""
    if is_windows():
        activate_script = os.path.join(VENV_DIR, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
    exec(open(activate_script).read(), dict(__file__=activate_script))

def install_python_packages():
    """Install necessary Python packages."""
    print("Installing Python packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])

def download_guibuster():
    """Clone the Guibuster repository."""
    if not os.path.exists("guibuster"):
        print("Cloning Guibuster repository...")
        subprocess.check_call(["git", "clone", REPO_URL])
    else:
        print("Guibuster repository already cloned.")

def download_wordlist():
    """Download the common.txt wordlist."""
    if not os.path.exists("common.txt"):
        print("Downloading wordlist...")
        subprocess.check_call(["curl", "-O", WORDLIST_URL])
    else:
        print("Wordlist already exists.")

def setup_shortcuts():
    """Set up shortcuts for the scripts."""
    if is_windows():
        desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

    guibuster_dir = os.path.abspath("guibuster")

    for script in os.listdir(guibuster_dir):
        if script.endswith(".py"):
            script_path = os.path.join(guibuster_dir, script)
            shortcut_path = os.path.join(desktop_dir, f"{script[:-3]}.lnk" if is_windows() else f"{script[:-3]}.desktop")
            
            if is_windows():
                import winshell
                winshell.CreateShortcut(
                    Path=shortcut_path,
                    Target=script_path,
                    Icon=(script_path, 0),
                    Description=f"Shortcut to {script}"
                )
            else:
                with open(shortcut_path, 'w') as f:
                    f.write(f"[Desktop Entry]\n"
                            f"Name={script[:-3]}\n"
                            f"Exec=python3 {script_path}\n"
                            f"Type=Application\n"
                            f"Terminal=false\n"
                            f"Icon=utilities-terminal\n")
                os.chmod(shortcut_path, 0o755)

def setup_proxychains():
    """Set up proxychains on Linux."""
    if is_linux():
        check_and_install_dependency(["proxychains4", "--version"], "sudo apt-get install proxychains4 -y")
        
        config_path = "/etc/proxychains.conf"
        if not os.path.exists(config_path):
            print("Creating proxychains configuration...")
            with open(config_path, "w") as f:
                f.write("strict_chain\n"
                        "proxy_dns\n"
                        "remote_dns_subnet 224\n"
                        "tcp_read_time_out 15000\n"
                        "tcp_connect_time_out 8000\n"
                        "socks4 127.0.0.1 9050\n")

        print("Proxychains setup complete. Edit /etc/proxychains.conf to configure your proxy settings.")

def check_and_install_dependency(command, install_command):
    """Check and install a dependency if not present."""
    try:
        subprocess.check_output(command, shell=True)
        print(f"{command[0]} is already installed.")
    except subprocess.CalledProcessError:
        print(f"{command[0]} is not installed. Installing...")
        try:
            subprocess.check_call(install_command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {command[0]}. Error: {e}")
            sys.exit(1)

def main_setup():
    """Main setup function."""
    check_prerequisites()
    setup_virtual_environment()
    activate_virtual_environment()
    install_python_packages()
    download_guibuster()
    download_wordlist()
    setup_shortcuts()
    setup_proxychains()
    print("Setup completed successfully!")

if __name__ == "__main__":
    main_setup()
