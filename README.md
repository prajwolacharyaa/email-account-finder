# Email Account Finder

Email Account Finder is a beginner-friendly cybersecurity and OSINT project. A user enters an email address, and the tool checks public sources for account-related signals on popular websites.

This project is designed for learning, portfolio use, and legal OSINT workflows on Kali Linux.

## Important Legal Notice

Use this tool only for:

- Your own email addresses
- Authorized security testing
- OSINT training in a legal environment
- Public information gathering

This tool does not hack accounts, bypass passwords, brute force logins, scrape private data, or evade rate limits. Many major websites intentionally block automated account enumeration, so the app marks those sites as `Manual Review`.

## Features

- Simple email input box
- Search button
- Public checks across multiple websites
- Clean results table
- Dark cybersecurity-style interface
- Loading animation while scanning
- Local search history
- Export results to CSV or PDF
- Web app and CLI mode
- Beginner-friendly Python code with comments

## What The Statuses Mean

| Status | Meaning |
| --- | --- |
| Found | A public source returned a direct signal for the email. |
| Possible Match | A public profile exists for a username guessed from the email local part. This does not prove ownership. |
| Not Found | No public signal was found for that check. |
| Unknown | The check could not complete because of network, API, or rate-limit issues. |
| Manual Review | The website restricts reliable automated email checks. A legal public help/recovery link is provided. |

## Websites Covered

Direct or public-signal checks:

- Gravatar
- GitHub public user search
- Reddit username profile
- TikTok username profile
- GitHub username profile
- Twitter/X username profile
- Instagram username profile

Manual review links:

- Facebook
- Instagram
- LinkedIn
- Discord
- Spotify
- Google
- Microsoft
- Amazon
- Netflix
- PayPal

## Installation On Kali Linux

```bash
git clone https://github.com/YOUR-USERNAME/email-account-finder.git
cd email-account-finder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You can also run:

```bash
chmod +x setup.sh
./setup.sh
```

## Run The Web App

```bash
source .venv/bin/activate
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

## Run The CLI Tool

```bash
source .venv/bin/activate
python cli.py target@example.com
```

Export from CLI:

```bash
python cli.py target@example.com --csv
python cli.py target@example.com --pdf
```

## Example Output

```text
Website           | Status         | Link
------------------------------------------------
Gravatar          | Found          | https://www.gravatar.com/...
GitHub            | Not Found      | -
Reddit            | Possible Match | https://www.reddit.com/user/...
Facebook          | Manual Review  | https://www.facebook.com/login/identify
```

## Project Structure

```text
email-account-finder/
├── app.py
├── cli.py
├── scanner.py
├── requirements.txt
├── setup.sh
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── styles.css
└── README.md
```

## Notes For GitHub Upload

Before uploading:

```bash
git init
git add .
git commit -m "Initial Email Account Finder project"
```

Then create a GitHub repository named `email-account-finder` and push your code.

## Disclaimer

This project is for educational and authorized OSINT use only. The results may be incomplete or inaccurate because websites change their public behavior and many services intentionally prevent account enumeration.
