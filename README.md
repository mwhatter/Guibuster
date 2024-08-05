# Guibuster

Guibuster is a user-friendly graphical interface built to simplify the use of the popular command-line tool, Gobuster. This GUI tool allows you to perform various enumeration tasks such as directory enumeration, VHOST enumeration, fuzzing, and more, with easy-to-use buttons and inputs.

## Features

- **Directory Enumeration**: Easily run directory brute-forcing on web servers.
- **VHOST Enumeration**: Discover virtual hosts on the target server.
- **Fuzzing Mode**: Perform fuzzing on web applications.
- **S3 Bucket Enumeration**: Enumerate AWS S3 buckets.
- **GCS Bucket Enumeration**: Enumerate Google Cloud Storage buckets.
- **TFTP Enumeration**: Perform TFTP enumeration.
- **DNS Subdomain Enumeration**: Find subdomains of a target domain.
- **Integrated ProxyChains**: Optionally run all commands through ProxyChains for anonymity.
- **Cross-Platform Support**: Works on both Windows and Linux.

## Installation

### Prerequisites

- **Python** (version 3.6 or higher)
- **Go**
- **Git** (if not already installed)

### Installation Steps

1. Clone this repository:
    ```bash
    git clone https://github.com/mwhatter/Guibuster/Guibuster.git
    cd Guibuster
    ```

2. Run the setup script to install all dependencies and set up the environment:
    ```bash
    python setup.py
    ```

3. Run Guibuster:
    ```bash
    python Guibuster.py
    ```

## Usage

Guibuster is designed to be intuitive. Each mode has dedicated buttons to trigger the corresponding Gobuster commands. Here's how you can use each feature:

1. **Run DIR**: Perform directory enumeration.
2. **Run VHOST**: Discover virtual hosts.
3. **Run FUZZ**: Fuzz web applications.
4. **Run S3**: Enumerate AWS S3 buckets.
5. **Run GCS**: Enumerate Google Cloud Storage buckets.
6. **Run TFTP**: Perform TFTP enumeration.
7. **Run DNS**: Find subdomains of a target domain.

### ProxyChains

You can enable ProxyChains by selecting the "Use ProxyChains" checkbox before running any command.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.


