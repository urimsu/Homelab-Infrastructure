"""Small allowlisted Discord status bot; no shell or host control is exposed."""

from __future__ import annotations

import os
import sys

try:
    import discord
    from discord.ext import commands
except ImportError as exc:
    print("Install the dependencies from requirements.txt first.", file=sys.stderr)
    raise SystemExit(1) from exc


def configured_user_ids() -> set[int]:
    raw = os.environ.get("AUTHORIZED_USER_IDS", "")
    try:
        return {int(item.strip()) for item in raw.split(",") if item.strip()}
    except ValueError as exc:
        raise ValueError("AUTHORIZED_USER_IDS must contain comma-separated numeric IDs") from exc


def main() -> int:
    token = os.environ.get("DISCORD_TOKEN")
    if not token or token == "replace_me":
        print("Set DISCORD_TOKEN in the process environment.", file=sys.stderr)
        return 2
    try:
        allowed_users = configured_user_ids()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if not allowed_users:
        print("Set at least one AUTHORIZED_USER_IDS value.", file=sys.stderr)
        return 2

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command(name="status")
    async def status_command(ctx: commands.Context) -> None:
        if ctx.author.id not in allowed_users:
            await ctx.reply("You are not authorized to use this command.", mention_author=False)
            return
        await ctx.reply("Bot is online. Host status is not queried by this example.", mention_author=False)

    try:
        bot.run(token, log_handler=None)
    except (discord.LoginFailure, OSError) as exc:
        print(f"Bot could not start: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
