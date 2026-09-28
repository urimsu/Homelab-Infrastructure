# Discord automation example

This minimal example demonstrates an allowlisted status command. It does not execute shell commands or shut down hosts. A real bot token is supplied via `DISCORD_TOKEN`; configure one or more numeric authorized user IDs through `AUTHORIZED_USER_IDS`.

The prefix command example enables Discord's privileged Message Content intent. Enable that intent for the bot in the Discord developer settings only if needed, and keep the bot's server permissions narrow.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r scripts/discord-bot/requirements.txt
export DISCORD_TOKEN='your-local-token'
export AUTHORIZED_USER_IDS='123456789012345678'
python scripts/discord-bot/bot.py
```

Do not paste token values into source, command history, logs, screenshots, or Git. Use a dedicated test server and grant the bot only required Discord permissions. For privileged host actions, use a separately reviewed narrow SSH command and command-specific sudo policy.
