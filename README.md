# Email Account Finder

Email Account Finder is a beginner-friendly cybersecurity and OSINT tool that checks public email-related signals and provides safe official review links for popular websites.

The project is built for learning, ethical OSINT practice, and portfolio use. It includes both a web interface and a command-line interface, making it suitable for Kali Linux users, Windows users, and macOS users.

> This tool only uses public information and legal methods. It does not hack accounts, bypass passwords, brute force logins, scrape private data, or perform illegal account enumeration.

## Project Objective

The goal of Email Account Finder is to help users enter an email address and review legal public signals that may indicate whether the email appears in public account-related sources.

The tool shows:

- Website name
- Account status
- Public source or official recovery/help link
- Method used
- Notes explaining the result

## Features

- Simple email input box
- Search button
- Scans multiple popular websites
- Clean results table
- Clean, human-friendly interface
- Loading animation while scanning
- Saves local search history
- Export results to CSV
- Export results to PDF
- Web interface for localhost use
- CLI mode for terminal users
- Beginner-friendly Python code
- Useful for ethical OSINT learning

## Legal And Ethical Use

Use this project only for:

- Your own email addresses
- Authorized security testing
- Educational OSINT practice
- Public information gathering
- Portfolio or classroom demonstrations

Do not use this project for:

- Harassment
- Stalking
- Unauthorized investigations
- Credential attacks
- Password reset abuse
- Account takeover attempts
- Bypassing login systems
- Scraping private user data

Many major websites intentionally prevent automated email account checks. For those websites, this tool shows `Protected` and provides an official public help or recovery page. The tool does not guess usernames or claim that an account belongs to an email without a direct public signal.

## Status Meanings

| Status | Meaning |
| --- | --- |
| Found | A public source returned a direct signal for the email. |
| Not Found | No public signal was found for that check. |
| Unknown | The check could not complete because of network, API, or rate-limit issues. |
| Protected | The website restricts reliable automated checks. A legal public help or recovery link is provided. |

## Websites Covered

The tool includes public checks or safe review links for services such as:

- Facebook
- Instagram
- YouTube
- TikTok
- Snapchat
- Reddit
- X (formerly Twitter)
- Pinterest
- LinkedIn
- GitHub
- Threads
- Discord
- Quora
- Twitch
- Telegram
- Gravatar

Some platforms allow limited public email-signal checks. Others block reliable automated account confirmation, so they are marked as protected.

## Installation And Setup

### Kali Linux Setup

Update your system:

```bash
sudo apt update
sudo apt upgrade -y
```

Install required packages:

```bash
sudo apt install python3 python3-pip python3-venv git -y
```

Clone the repository:

```bash
git clone https://github.com/prajwolacharyaa/email-account-finder.git
```


Enter the project directory:

```bash
cd email-account-finder
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the web app:

```bash
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

You can also use the included setup script on Kali Linux:

```bash
chmod +x setup.sh
./setup.sh
```

### Windows Setup

Install Python from:

```text
https://www.python.org/downloads/
```

During installation, enable:

```text
Add Python to PATH
```

Install Git from:

```text
https://git-scm.com/downloads
```

Open Command Prompt or PowerShell.

Clone the repository:

```bash
git clone https://github.com/prajwolacharyaa/email-account-finder.git
```


Enter the project directory:

```bash
cd email-account-finder
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment in Command Prompt:

```bash
.venv\Scripts\activate
```

Activate the virtual environment in PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then try again:

```bash
.venv\Scripts\Activate.ps1
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the web app:

```bash
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

### macOS Setup

Install Homebrew from:

```text
https://brew.sh/
```

Install Python and Git:

```bash
brew install python git
```

Clone the repository:

```bash
git clone https://github.com/prajwolacharyaa/email-account-finder.git
```


Enter the project directory:

```bash
cd email-account-finder
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the web app:

```bash
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

## Running The Tool

### Web Mode

Start the Flask web app:

```bash
python app.py
```

Then visit:

```text
http://127.0.0.1:5000
```

Enter an email address and click the search button.

### CLI Mode

You can also run the tool directly from the terminal:

```bash
python cli.py target@example.com
```

Export results to CSV:

```bash
python cli.py target@example.com --csv
```

Export results to PDF:

```bash
python cli.py target@example.com --pdf
```

## Example Output

```text
Website           | Status         | Link
------------------------------------------------
Gravatar          | Found          | https://www.gravatar.com/...
GitHub            | Not Found      | -
Facebook          | Protected      | https://www.facebook.com/login/identify
Instagram         | Protected      | https://www.instagram.com/accounts/password/reset/
X (formerly Twitter) | Protected   | https://twitter.com/account/begin_password_reset
```

## Exporting Results

The tool supports:

- CSV export
- PDF export

Exports are useful for:

- OSINT reports
- Cybersecurity class projects
- Portfolio demonstrations
- Authorized investigation notes

## Troubleshooting

### `python` Command Not Found

Try:

```bash
python3 --version
```

Then use `python3` instead of `python`.

### `pip` Command Not Found

Try:

```bash
python -m pip install -r requirements.txt
```

or:

```bash
python3 -m pip install -r requirements.txt
```

### Flask Is Not Installed

Run:

```bash
pip install -r requirements.txt
```

Make sure your virtual environment is activated first.

### Port 5000 Is Already In Use

Stop the other process or change the port in `app.py`.

Example:

```python
app.run(host="127.0.0.1", port=5050, debug=False)
```

Then open:

```text
http://127.0.0.1:5050
```

### PowerShell Blocks Virtual Environment Activation

Run:

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```bash
.venv\Scripts\Activate.ps1
```

## Uploading To GitHub

If this project is not already uploaded to GitHub, use these commands:

```bash
git init
git add .
git commit -m "Initial Email Account Finder project"
git branch -M main
git remote add origin https://github.com/prajwolacharyaa/email-account-finder.git
git push -u origin main
```


## Beginner Notes

This project is intentionally simple so beginners can understand how it works.

Main concepts used:

- Python
- Flask
- HTML
- CSS
- JavaScript
- Requests
- Public OSINT checks
- CSV export
- PDF report generation

You can improve this project by adding:

- More public OSINT sources
- Better rate-limit handling
- API key support for official services
- Better report templates
- Docker support
- Authentication for private local use
- More advanced result filtering

## Disclaimer

Email Account Finder is made for educational and authorized OSINT use only.

The results may be incomplete, outdated, or inaccurate because websites frequently change their public behavior and many services intentionally prevent email-based account discovery.

The developer is not responsible for misuse of this tool. Always follow the law, respect privacy, and only investigate accounts you own or are authorized to test.
