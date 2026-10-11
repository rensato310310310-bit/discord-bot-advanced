# Discord Bot Project

This project includes:
- Discord bot with chat commands
- Web OAuth login with Discord
- Ticket creation system
- Role panel buttons
- Pinned message feature

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Copy `.env.example` to `.env` and fill in values.

3. Run the app:
   python app.py

## Features

- `!ticket` : create a support ticket channel
- `!rolepanel` : create a role panel in the current channel
- `!pinmsg <message>` : pin and update a fixed message in the current channel
- `http://localhost:5000/login` : Discord OAuth login page

## Notes

This project is structured so each feature is isolated in its own file for easier maintenance.
