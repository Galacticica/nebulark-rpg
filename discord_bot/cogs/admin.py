"""
File: admin.py
Author: Reagan Zierke
Date: 2025-04-22
Description: Developer commands for the bot.
These commands are intended for development and will not be in future deployment. 
"""


from discord.ext import commands
import aiohttp
import discord

class Admin(commands.Cog):
    def __init__(self, bot, dev_guild_id=756190406642761869):
        self.dev_guild_id = dev_guild_id
        self.bot = bot

    @commands.command(name="sync", description="Sync bot commands")
    @commands.is_owner()
    async def sync(self, ctx):
        '''
        Syncs the bot commands with Discord.
        '''

        try:
            print("Syncing commands...")
            commands_to_sync = self.bot.tree.get_commands()
            command_names = [command.name for command in commands_to_sync]
            await ctx.send(f"Commands to sync: {', '.join(command_names)}")
            
            synced = await self.bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} commands.")
        except Exception as e:
            await ctx.send(f"Error syncing commands: {e}")

    @commands.command(name="clear", description="Clear all slash commands")
    @commands.is_owner()
    async def clear(self, ctx):
        '''
        Clears all slash commands from the bot.
        '''

        try:
            print("Clearing commands...")
            commands_to_clear = self.bot.tree.get_commands()
            command_names = [command.name for command in commands_to_clear]
            await ctx.send(f"Commands to clear: {', '.join(command_names)}")

            guild = discord.Object(id=self.dev_guild_id)
            self.bot.tree.clear_commands(guild=guild)
            await self.bot.tree.sync(guild=guild)
            await ctx.send("All commands cleared for the development guild.")
        except Exception as e:
            await ctx.send(f"Error clearing commands: {e}")


    @commands.command(name="give_money", description="Give money to a user")
    @commands.is_owner()
    async def give_money(self, ctx, user: discord.User, amount: int):
        """
        Give money to a user.
        """

        if amount <= 0:
            await ctx.send("Amount must be a positive integer.")
            return

        discord_id = str(user.id)
        api_url = "http://127.0.0.1:8000/users/give_money/"
        payload = {
            "discord_id": discord_id,
            "amount": amount
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            message = data.get("message", "Something went wrong.")
                            await ctx.send(message)
                        except aiohttp.ContentTypeError:
                            text = await response.text()
                            await ctx.send(f"Unexpected response from the API: {text}")
                    elif response.status == 400:
                        try:
                            error = await response.json()
                            await ctx.send(f"Error: {error.get('error', 'Invalid request.')}")
                        except aiohttp.ContentTypeError:
                            text = await response.text()
                            await ctx.send(f"Error: {text}")
                    else:
                        await ctx.send("An unexpected error occurred. Please try again later.")
            except aiohttp.ClientError as e:
                await ctx.send(f"Network error: {str(e)}", ephemeral=True)

    @commands.command(name="give_xp", description="Give XP to a user")
    @commands.is_owner()
    async def give_xp(self, ctx, user: discord.User, amount: int):
        """
        Give xp to a user.
        """

        if amount <= 0:
            await ctx.send("Amount must be a positive integer.")
            return

        discord_id = str(user.id)
        api_url = "http://127.0.0.1:8000/users/give_xp/"
        payload = {
            "discord_id": discord_id,
            "amount": amount
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            message = data.get("message", "Something went wrong.")
                            await ctx.send(message)
                        except aiohttp.ContentTypeError:
                            text = await response.text()
                            await ctx.send(f"Unexpected response from the API: {text}")
                    elif response.status == 400:
                        try:
                            error = await response.json()
                            await ctx.send(f"Error: {error.get('error', 'Invalid request.')}")
                        except aiohttp.ContentTypeError:
                            text = await response.text()
                            await ctx.send(f"Error: {text}")
                    else:
                        await ctx.send("An unexpected error occurred. Please try again later.")
            except aiohttp.ClientError as e:
                await ctx.send(f"Network error: {str(e)}", ephemeral=True)
    
    @commands.command(name="delete_user", description="Delete a user via the API")
    @commands.is_owner()
    async def delete_user(self, ctx):
        """
        Command to delete a user via the API.
        """

        discord_id = str(ctx.author.id)
        api_url = "http://127.0.0.1:8000/users/delete_user/"
        payload = {
            "discord_id": discord_id
        }
        await ctx.send("Deleting user...")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.delete(api_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        message = data.get("message", "User successfully deleted.")
                        await ctx.send(message)
                    elif response.status == 404:
                        error = await response.json()
                        await ctx.send(f"Error: {error.get('error', 'User not found.')}")
                    elif response.status == 400:
                        error = await response.json()
                        await ctx.send(f"Error: {error.get('error', 'Invalid request.')}")
                    else:
                        await ctx.send("An unexpected error occurred. Please try again later.")
            except aiohttp.ClientError as e:
                await ctx.send(f"Network error: {str(e)}", ephemeral=True)


    @commands.command(name="faq", description="faq")
    @commands.is_owner()
    async def faq(self, ctx):
        """
        Command to display the FAQ.
        """

        faq_embed = discord.Embed(
            title="FAQ",
            description="Frequently Asked Questions",
            color=discord.Color.blue()
        )

        faq_embed.add_field(
            name="How do I get started?",
            value="To get started, use the `/help` command to see the different categories of commands.",
            inline=False
        )
        faq_embed.add_field(
            name="How do I report a bug?",
            value="To report a bug, use the `/report_issue` command.",
            inline=False
        )

        faq_embed.add_field(
            name="How do I view my stats?",
            value="To view your stats, use the `/user profile` command.",
            inline=False
        )

        faq_embed.add_field(
            name="How do I get money?",
            value="You can earn money by completing adventures or gambling.",
            inline=False
        )

        faq_embed.add_field(
            name="How do I go on an adventure?",
            value="To go on an adventure, use the `/adventure start` command.",
            inline=False
        )

        faq_embed.add_field(
            name="How do I get gear?",
            value="You can get gear by purchasing it from the shop using `/shop purchase` command. To see what is available, use the `/shop list` command.",
            inline=False
        )

        faq_embed.add_field(
            name="How do I get levels?",
            value="You can get levels by completing adventures and earning XP. You can level up by using the `/user level_up` command.",
            inline=False
        )

        faq_embed.add_field(
            name="How do I gamble?",
            value="You can gamble by using the `/gamble {game}` command.",
            inline=False
        )
        
         


        await ctx.send(embed=faq_embed)

async def setup(bot):
    '''
    Load the Admin cog.
    '''

    await bot.add_cog(Admin(bot))