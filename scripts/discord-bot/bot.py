"""Small allowlisted Discord status bot; no shell or host control is exposed."""

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))

PROXMOX_HOST = "192.168.0.229"
PROXMOX_USER = "rasp-pi-bot"

# WICHTIG:
# Falls wol.py woanders liegt, diesen Pfad ändern.
WOL_SCRIPT = "/home/pi/wol.py"


bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.default()
)


def authorized(ctx):
    return ctx.author.id == ALLOWED_USER_ID


async def run_ssh(*command):
    process = await asyncio.create_subprocess_exec(
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=5",
        "{}@{}".format(PROXMOX_USER, PROXMOX_HOST),
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    return (
        process.returncode,
        stdout.decode().strip(),
        stderr.decode().strip()
    )


@bot.event
async def on_ready():
    print("Bot online als {}".format(bot.user))


# =========================================================
# !proxmox
# =========================================================

@bot.command()
async def proxmox(ctx):

    if not authorized(ctx):
        await ctx.send("⛔ Keine Berechtigung.")
        return

    code, hostname, error = await run_ssh("hostname")

    if code != 0:
        await ctx.send(
            "🔴 **Proxmox ist nicht erreichbar.**"
        )
        return

    code, uptime, error = await run_ssh("uptime", "-p")

    if code != 0:
        uptime = "unbekannt"

    await ctx.send(
        "🟢 **Proxmox ist online**\n"
        "🖥️ Host: `{}`\n"
        "⏱️ Uptime: `{}`\n"
        "🌐 IP: `{}`".format(
            hostname,
            uptime,
            PROXMOX_HOST
        )
    )


# =========================================================
# !shutdown
# =========================================================

@bot.command()
async def shutdown(ctx):

    if not authorized(ctx):
        await ctx.send("⛔ Keine Berechtigung.")
        return

    await ctx.send(
        "⚠️ **Proxmox wirklich herunterfahren?**\n\n"
        "Tippe innerhalb von 30 Sekunden:\n"
        "`!confirm`"
    )

    def check(message):
        return (
            message.author.id == ALLOWED_USER_ID
            and message.channel.id == ctx.channel.id
            and message.content.lower() == "!confirm"
        )

    try:
        await bot.wait_for(
            "message",
            timeout=30.0,
            check=check
        )

    except asyncio.TimeoutError:
        await ctx.send(
            "❌ Shutdown abgebrochen – Zeit abgelaufen."
        )
        return

    await ctx.send(
        "🔴 **Proxmox wird heruntergefahren...**"
    )

    code, output, error = await run_ssh(
        "sudo",
        "/usr/sbin/shutdown",
        "-h",
        "now"
    )

    if code != 0:
        await ctx.send(
            "❌ Shutdown fehlgeschlagen:\n`{}`".format(error)
        )


# =========================================================
# !reboot
# =========================================================

@bot.command()
async def reboot(ctx):

    if not authorized(ctx):
        await ctx.send("⛔ Keine Berechtigung.")
        return

    await ctx.send(
        "⚠️ **Proxmox wirklich neustarten?**\n\n"
        "Tippe innerhalb von 30 Sekunden:\n"
        "`!confirmreboot`"
    )

    def check(message):
        return (
            message.author.id == ALLOWED_USER_ID
            and message.channel.id == ctx.channel.id
            and message.content.lower() == "!confirmreboot"
        )

    try:
        await bot.wait_for(
            "message",
            timeout=30.0,
            check=check
        )

    except asyncio.TimeoutError:
        await ctx.send(
            "❌ Neustart abgebrochen – Zeit abgelaufen."
        )
        return

    await ctx.send(
        "🔄 **Proxmox wird neugestartet...**"
    )

    code, output, error = await run_ssh(
        "sudo",
        "/usr/sbin/shutdown",
        "-r",
        "now"
    )

    if code != 0:
        await ctx.send(
            "❌ Neustart fehlgeschlagen:\n`{}`".format(error)
        )


# =========================================================
# !turnon
# =========================================================

@bot.command()
async def turnon(ctx):

    if not authorized(ctx):
        await ctx.send("⛔ Keine Berechtigung.")
        return

    # Erst prüfen, ob Proxmox vielleicht schon läuft
    code, output, error = await run_ssh("hostname")

    if code == 0:
        await ctx.send(
            "🟢 **Proxmox läuft bereits.**"
        )
        return

    await ctx.send(
        "⚡ Wake-on-LAN wird gesendet..."
    )

    process = await asyncio.create_subprocess_exec(
        "python3",
        WOL_SCRIPT,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        await ctx.send(
            "❌ Wake-on-LAN fehlgeschlagen:\n`{}`".format(
                stderr.decode().strip()
            )
        )
        return

    await ctx.send(
        "📡 **Wake-on-LAN gesendet.**\n"
        "Ich warte auf Proxmox..."
    )

    # Maximal ca. 2 Minuten auf Proxmox warten
    for attempt in range(12):

        await asyncio.sleep(10)

        code, hostname, error = await run_ssh("hostname")

        if code == 0:
            await ctx.send(
                "🟢 **Proxmox {} ist wieder online!**".format(
                    hostname
                )
            )
            return

    await ctx.send(
        "🟠 Wake-on-LAN wurde gesendet, "
        "aber Proxmox ist nach 2 Minuten noch nicht erreichbar."
    )


# =========================================================
# !helpme
# =========================================================

@bot.command()
async def helpme(ctx):

    if not authorized(ctx):
        await ctx.send("⛔ Keine Berechtigung.")
        return

    await ctx.send(
        "🖥️ **SuTech Homelab Control**\n\n"
        "`!proxmox` – Status anzeigen\n"
        "`!turnon` – Proxmox per Wake-on-LAN starten\n"
        "`!shutdown` – Proxmox herunterfahren\n"
        "`!reboot` – Proxmox neustarten\n"
        "`!helpme` – Diese Übersicht anzeigen"
    )


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN fehlt in .env")

bot.run(TOKEN)
