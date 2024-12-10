import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta

# Load configuration
with open("config.json") as config_file:
    config = json.load(config_file)

TOKEN = config["bot_token"]
GEN_CHANNEL_ID = config["gen_channel_id"]
NO_COOLDOWN_ROLE_ID = config["no_cooldown_role_id"]  # Role ID for cooldown bypass

# Cooldowns JSON file
COOLDOWN_FILE = "cooldowns.json"

# Load cooldown data or initialize if file doesn't exist
if not os.path.exists(COOLDOWN_FILE):
    with open(COOLDOWN_FILE, "w") as file:
        json.dump({}, file)
else:
    with open(COOLDOWN_FILE, "r") as file:
        cooldowns = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is ready!")

def save_cooldowns():
    """Saves the cooldowns dictionary to the cooldowns.json file."""
    with open(COOLDOWN_FILE, "w") as file:
        json.dump(cooldowns, file)

@bot.command()
async def gen(ctx, service: str):
    # Check if the command is used in the correct channel
    if ctx.channel.id != GEN_CHANNEL_ID:
        await ctx.send(embed=discord.Embed(
            description="This command can only be used in the designated generation channel.",
            color=discord.Color.red()
        ))
        return

    user_id = str(ctx.author.id)
    current_time = datetime.utcnow()

    # Check if user has the no-cooldown role
    member = ctx.author
    if NO_COOLDOWN_ROLE_ID in [role.id for role in member.roles]:
        bypass_cooldown = True
    else:
        bypass_cooldown = False

    # Check if user is on cooldown (only if they do not bypass cooldown)
    if not bypass_cooldown and user_id in cooldowns:
        last_used = datetime.strptime(cooldowns[user_id], "%Y-%m-%d %H:%M:%S")
        if current_time < last_used + timedelta(minutes=60):
            remaining_time = (last_used + timedelta(minutes=60)) - current_time
            minutes, seconds = divmod(remaining_time.seconds, 60)
            await ctx.send(embed=discord.Embed(
                description=f"⏳ You can generate another account in `{minutes}m {seconds}s`.",
                color=discord.Color.red()
            ))
            return

    # Ensure service file exists
    service_file = f"{service}.txt"
    if not os.path.exists(service_file):
        await ctx.send(embed=discord.Embed(
            description=f"No serials found for the service: `{service}`.",
            color=discord.Color.red()
        ))
        return

    # Read a serial from the file
    with open(service_file, "r") as file:
        lines = file.readlines()

    if not lines:
        await ctx.send(embed=discord.Embed(
            description=f"No more serials available for the service: `{service}`.",
            color=discord.Color.red()
        ))
        return

    # Get the first serial and remove it from the file
    serial = lines[0].strip()
    with open(service_file, "w") as file:
        file.writelines(lines[1:])

    # Create an embed for the DM
    embed_dm = discord.Embed(
        title="Generated Account",
        color=discord.Color.green(),
        timestamp=current_time  # Automatically add timestamp to the embed
    )
    embed_dm.add_field(name="Service", value=f"```{service.capitalize()}```", inline=False)
    embed_dm.add_field(name="Account", value=f"```{serial}```", inline=False)

    try:
        # Send the embed to the user's DMs
        await ctx.author.send(embed=embed_dm)

        # Notify in the channel that the serial was sent
        embed_public = discord.Embed(
            description=f"✅ A serial for `{service}` has been sent to your DMs!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed_public)

        # Update cooldown and save (if not bypassing)
        if not bypass_cooldown:
            cooldowns[user_id] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            save_cooldowns()

    except discord.Forbidden:
        # If the bot cannot send a DM, notify the user
        await ctx.send(embed=discord.Embed(
            description="❌ I couldn't send you a DM. Please make sure your DMs are open.",
            color=discord.Color.red()
        ))

@bot.command()
async def stock(ctx):
    # Check if the command is used in the correct channel
    if ctx.channel.id != GEN_CHANNEL_ID:
        await ctx.send(embed=discord.Embed(
            description="This command can only be used in the designated generation channel.",
            color=discord.Color.red()
        ))
        return

    stock_list = []
    for file in os.listdir():
        if file.endswith(".txt"):
            service_name = file.replace(".txt", "")
            with open(file, "r") as f:
                stock_count = len(f.readlines())
            stock_list.append((service_name, stock_count))

    if not stock_list:
        await ctx.send(embed=discord.Embed(
            description="No services found with stock.",
            color=discord.Color.red()
        ))
        return

    embed = discord.Embed(
        title="Stock for All Services",
        color=discord.Color.blue()
    )

    for service_name, stock_count in stock_list:
        embed.add_field(
            name=service_name.capitalize(),
            value=f"📦 `{stock_count}` serials available",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(
            description="Usage: `!gen <service>`",
            color=discord.Color.red()
        ))
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(embed=discord.Embed(
            description="An error occurred while processing your request.",
            color=discord.Color.red()
        ))
    else:
        raise error

# Run the bot
bot.run(TOKEN)
