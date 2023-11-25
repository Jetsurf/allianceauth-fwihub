import logging

from discord import Embed, User, option
from discord.ext import commands

from django.conf import settings
logger = logging.getLogger(__name__)

class SystemGrapher(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(name="graph")
	async def graph_system(self, ctx):
		await ctx.respond("testing for now!")

def setup(bot):
	bot.add_cog(SystemGrapher(bot))
