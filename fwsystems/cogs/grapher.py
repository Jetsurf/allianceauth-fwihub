from discord import Embed, User, option
from discord.ext import commands

from django.conf import settings
logger = logging.getLogger(__name__)

class SystemGrapher(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(name="graph", guild_ids=[int(settings.DISCORD_GUILD_ID)])
	async def graph_system(self, ctx):
		ctx.respond("testing for now!")

	def setup(bot):
    	bot.add_cog(SystemGrapher(bot))