# Discord bot dependency and runtime limitations

## Problem

The bot environment was constrained by a Raspberry Pi running Python 3.7.x and discord.py 1.7.x.

## Symptoms

Newer library releases may no longer support the installed interpreter, while unpinned installs can change behavior over time.

## Architecture / Context

Discord bot on Raspberry Pi → status or restricted SSH/Wake-on-LAN operation. The versions above describe a historical implementation context, not a recommended current deployment.

## Hypotheses

Interpreter support mismatch; incompatible dependency resolution; outdated API usage; token/configuration error; network connectivity issue.

## Investigation

Record Python and package versions, inspect install errors, and separate startup/authentication failures from command handling. Check the upstream compatibility matrix before selecting versions.

## Commands Used

```bash
python3 --version
python3 -m pip show discord.py
python3 -m pip check
```

## Root Cause

The older interpreter imposed compatibility constraints; a precise failure for every incident is not claimed.

## Solution

Prefer upgrading to a supported OS and Python runtime. Pin dependencies in a virtual environment after verifying compatibility. Keep the bot token in an environment variable.

## Verification

Start the bot with a test account/server, verify only allowlisted users can invoke commands, and inspect logs for accidental secrets.

## Security Considerations

Never paste tokens into source, screenshots, or logs. Avoid arbitrary shell command handlers and broad sudo privileges.

## What I Learned

Runtime lifecycle and dependency compatibility are part of automation reliability.
