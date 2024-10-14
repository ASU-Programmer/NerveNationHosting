import nextcord
import os
from nextcord.ext import commands
from nextcord import Interaction, Embed
from datetime import timedelta
from keep_alive import keep_alive

DISCORD_KEY = os.envrion['discordkey']

intents = nextcord.Intents.default()
intents.guilds = True
intents.message_content = True
intents.members = True  # Required to fetch member details
client = commands.Bot(command_prefix="!", intents=intents)

AUTHORIZED_USER_ID = 476985163230871556  # Your Discord user ID

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


# Function to check if the user is authorized
def is_authorized(interaction: Interaction):
    return interaction.user.id == AUTHORIZED_USER_ID

@client.slash_command(guild_ids=[1153064476627714158], description="Seal a user for 3000 years.")
async def seal(interaction: Interaction, member: nextcord.Member, reason: str = "No reason provided"):
    if not is_authorized(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    # Calculate the mute duration (3000 years in seconds)
    duration = 3000 * 365 * 24 * 60 * 60  # 3000 years in seconds

    # Create an embed for the mute message
    embed = Embed(
        title="User Muted",
        description=f"{member.mention} has been muted for 3000 years!",
        color=nextcord.Color.red()
    )
    embed.add_field(name="Reason", value=reason,inline=False)
    embed.add_field(name="Duration", value="3000 years", inline=False)
    embed.set_footer(text=f"Muted by {interaction.user}")
    embed.set_image(url="https://media1.tenor.com/m/pOXLuJVd6NAAAAAd/gate-close-jujutsu-kaisen.gif")

    # Mute the user (this requires a role or permission-based muting system)
    mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
    if mute_role:
        await member.add_roles(mute_role, reason=reason)
        await interaction.response.send_message(embed=embed)

        # You would likely use a scheduler or background task for unmuting after 3000 years,
        # but for such a long duration, it's mostly symbolic.
    else:
        await interaction.response.send_message("Mute role not found! Please set up a role named 'Muted'.", ephemeral=True)


@client.slash_command(guild_ids=[1153064476627714158], description="Unseal a user.")
async def unseal(interaction: Interaction, member: nextcord.Member, reason: str = "No reason provided"):
    if not is_authorized(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    # Create an embed for the unmute message
    embed = Embed(
        title="User Unmuted",
        description=f"{member.mention} has been unmuted!",
        color=nextcord.Color.green()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text=f"Unmuted by {interaction.user}")
    embed.set_image(url="https://media1.tenor.com/m/SskG7kHqNiYAAAAd/madara-edo-madara-uchiha-edo.gif")

    # Unmute the user by removing the "Muted" role
    mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role, reason=reason)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"{member.mention} is not muted.", ephemeral=True)



@client.slash_command(guild_ids=[1153064476627714158],description="List all sealed users (in prison).")
async def prisonlist(interaction: Interaction):
    if not is_authorized(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    # Get the "Muted" role
    mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")

    if not mute_role:
        await interaction.response.send_message("Mute role not found!", ephemeral=True)
        return

    # Get all members with the "Muted" role
    muted_members = [member.mention for member in interaction.guild.members if mute_role in member.roles]

    # Create the embed
    embed = Embed(
        title="Prison List",
        description="These users are currently muted (in prison):",
        color=nextcord.Color.dark_red()
    )

    if muted_members:
        embed.add_field(name="Muted Members", value="\n".join(muted_members), inline=False)
    else:
        embed.add_field(name="Muted Members", value="No one is currently muted.", inline=False)

    embed.set_footer(text=f"Requested by {interaction.user}")

    # Send the embed
    await interaction.response.send_message(embed=embed)


@client.slash_command(guild_ids=[1153064476627714158],description="Unseall all users who are currently sealed.")
async def unsealall(interaction: Interaction):
    if not is_authorized(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
    # Get the "Muted" role
    mute_role = nextcord.utils.get(interaction.guild.roles, name="Muted")

    if not mute_role:
        await interaction.response.send_message("Mute role not found!", ephemeral=True)
        return

    # Find all members with the "Muted" role
    muted_members = [member for member in interaction.guild.members if mute_role in member.roles]

    if not muted_members:
        await interaction.response.send_message("No one is currently muted.", ephemeral=True)
        return

    # Unmute each member (remove the "Muted" role)
    for member in muted_members:
        await member.remove_roles(mute_role, reason="Unmute all command issued")

    # Create an embed to confirm the action
    embed = Embed(
        title="All Sealed Users Released",
        description=f"{len(muted_members)} users have been unmuted!",
        color=nextcord.Color.green()
    )
    embed.set_footer(text=f"Unmuted by {interaction.user}")
    embed.set_image(url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZW1qZW9mMzh3Njl0ZXo5M2hzcjBpaGJucnV4Nnc2bml0NXM4dDdmNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4lu5FuhtrbaOQgKN57/giphy.webp")

    # Send confirmation message
    await interaction.response.send_message(embed=embed)


keep_alive()
client.run(DISCORD_KEY)