"""
File: shop.py
Author: Reagan Zierke
Date: 2025-05-03
Description: Shop commands for the bot.
This file contains commands related to the shop, such as buying and listing items.
"""



import discord
from discord.ext import commands
import aiohttp  

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    shop_group = discord.app_commands.Group(name="shop", description="Shop commands")

    def format_time(self, seconds):
        '''
        Helper function to format time in seconds to a readable format.
        '''
            
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s" 
    
    def format_error(self, error):
        '''
        Helper function to format error messages.
        '''
        
        embed = discord.Embed(
            title="Error",
            description=error,
            color=discord.Color.red()
        )
        return embed
    
    @shop_group.command(name="help", description="Shows the help menu")
    async def help(self, interaction: discord.Interaction):
        """
        Command to show the help menu.
        """
        
        embed = discord.Embed(
            title="Help Menu",
            description="List of available commands:",
            color=discord.Color.blue()
        )

        for command in self.shop_group.commands:
            embed.add_field(
                name=f"/shop {command.name}",
                value=command.description or "No description available.",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @shop_group.command(name="list", description="List all items in the shop available for purchase")
    async def list_items(self, interaction: discord.Interaction):
        """
        Command to list all items in the shop.
        """

        api_url = "http://127.0.0.1:8000/gear/shop/"
        payload = {
            "discord_id": str(interaction.user.id)}

        def format_embed(data):
            embed = discord.Embed(
                title="Shop Items",
                description="List of items available for purchase:",
                color=discord.Color.orange()
            )

            for item in data: 
                embed.add_field(
                    name=item['name'],
                    value=f"Cost: {item['cost']}",
                    inline=False
                )

            embed.set_footer(text="Use /shop item_detail <item_name> to get more info on an item.")
            return embed

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url, json=payload) as response:
                    if response.status in range(200,300):
                        data = await response.json()
                        if data and isinstance(data, list) and len(data) > 0:
                            embed = format_embed(data)
                            await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message("No items for sale at the moment.")
                    elif response.status in range(400,500):
                        error = await response.json()
                        error = error['non_field_errors'][0]
                        await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                        return 
                    else:
                        error = "Server error occurred."
                        await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                error = f"Network error: {str(e)}"
                await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                return
        
    @shop_group.command(name="item_detail", description="Get details about a specific item")
    @discord.app_commands.describe(item_name="Name of the item")
    async def item_detail(self, interaction: discord.Interaction, item_name: str):
        """
        Command to get details about a specific item.
        """

        api_url = "http://127.0.0.1:8000/gear/gear_detail/"

        payload = {
            "gear_name": item_name
        }

        def format_embed(data):
            embed = discord.Embed(
                title=data['name'],
                description=data['description'],
                color=discord.Color.orange()
            )

            embed.add_field(
                name="Cost",
                value=f"{data['cost']}",
                inline=True
            )
            if data['xp_bonus'] != 0:
                if data['xp_bonus'] % 1 == 0:
                    data['xp_bonus'] = int(data['xp_bonus'])
                embed.add_field(
                    name="XP Bonus",
                    value=f"+{data['xp_bonus']}%",
                    inline=True
                )
            if data['money_bonus'] != 0:
                if data['money_bonus'] % 1 == 0:
                    data['money_bonus'] = int(data['money_bonus'])
                embed.add_field(
                    name="Money Bonus",
                    value=f"+{data['money_bonus']}%",
                    inline=True
                )
            if data['time_bonus'] != 0:
                if data['time_bonus'] % 1 == 0:
                    data['time_bonus'] = int(data['time_bonus'])
                embed.add_field(
                    name="Time Bonus",
                    value=f"-{data['time_bonus']}%",
                    inline=True
                )

            embed.set_footer(text="Use /shop purchase <item_name> to purchase this item.")
            return embed

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url, json=payload) as response:
                    if response.status in range(200,300):
                        data = await response.json()
                        embed = format_embed(data)
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400,500):
                        error = await response.json()
                        error = error['non_field_errors'][0]
                        await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                        return
                    else:
                        error = "Server error occurred."
                        await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                error = f"Network error: {str(e)}"
                await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                return
                
    @shop_group.command(name="purchase", description="Purchase an item from the shop")
    @discord.app_commands.describe(item_name="Name of the item")
    async def purchase(self, interaction: discord.Interaction, item_name: str):
        """
        Command to purchase an item from the shop.
        """

        api_url = "http://127.0.0.1:8000/gear/purchase/"
        payload = {
            "discord_id": str(interaction.user.id),
            "gear_name": item_name
        }

        def format_embed(data):
            embed = discord.Embed(
                title="Purchase Successful",
                description=f"You have successfully purchased {data['name']}!",
                color=discord.Color.green()
            )
            return embed

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as response:
                    if response.status in range(200,300):
                        data = await response.json()
                        embed = format_embed(data)
                        await interaction.response.send_message(embed=embed)
                    elif response.status in range(400,500):
                        error = await response.json()
                        error = error['non_field_errors'][0]
                        await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                        return
                    else:
                        error = "Server error occurred."
                        await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                        return
            except aiohttp.ClientError as e:
                error = f"Network error: {str(e)}"
                await interaction.response.send_message(embed=self.format_error(error), ephemeral=True)
                return


async def setup(bot):
    '''
    Loads the Shop cog into the bot.
    '''

    await bot.add_cog(Shop(bot))