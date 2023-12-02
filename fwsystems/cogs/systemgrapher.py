import logging
import io
import time

from discord import Embed, User, Option, File
from discord.ext import commands
from datetime import datetime, timezone, timedelta

from fwsystems.models import System, SystemContest, Webhook

from eveuniverse.models import EveFaction, EveSolarSystem

from fwsystems.view_helpers import get_contest_entries_sorted

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from django.conf import settings
logger = logging.getLogger(__name__)

class SystemGrapher(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(name="graph", description="Display graph of contest and advantage for a system")
	async def graph_system(self, ctx, system_name: Option(str, "System Name to pull data"), days: Option(int, "Number of days to disaply", default=3)):
		#try:
		system_id = EveSolarSystem.objects.filter(name=system_name)[0].id
		#except:
		#	await ctx.respond(f"Could not find system {system_name}")
		#	return

		await ctx.defer()
		fileio = self.create_graph(system_id, days)
		await ctx.respond(file=fileio)

	def create_graph(self, system_id, days):
		system, system_fetched = EveSolarSystem.objects.get_or_create_esi(id=system_id)
		data = get_contest_entries_sorted(system_id, days, retDateTime=True)

		fig, ax = plt.subplots(figsize=(8, 3.8), layout='constrained')

		ax2 = ax.twinx()
		ax.set_xlabel('Date/Time (UTC/EVE)')
		ax.set_ylabel('Contested %')
		ax.set_title(f"{system.name} - {data['contest_entries'][len(data['contest_entries'])-1].OccupierFactionID.name} Occupied - Last {days} days")
		ax2.set_ylabel('Advantage %')
		ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter('{0:.0%}'.format))
		ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter('{:0.0f}%'.format))
		ax.xaxis.set_major_locator(mdates.DayLocator())
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

		for label in ax.get_xticklabels(which='major'):
			label.set(rotation=60, horizontalalignment='right')

		ax.xaxis.set_minor_locator(mdates.HourLocator((0, 6, 12, 18)))

		for label in ax.get_xticklabels(which='minor'):
			label.set(rotation=60, horizontalalignment='right')

		ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
		ax.grid(visible=True, axis='x', which='major', color='black')
		ax.grid(visible=True, axis='x', which='minor', color='black')
		ax2.plot(data['timeData'], data['advantageAmount1'], color=data['color1'], label=f"{data['faction1'].split(' ')[0]} Adv")
		ax2.plot(data['timeData'], data['advantageAmount2'], color=data['color2'], label=f"{data['faction2'].split(' ')[0]} Adv")
		ax.plot(data['timeData'], data['contestAmount'], color=data['colorcontest'], label="Contested %")
		ax.yaxis.label.set_color('black')
		ax2.yaxis.label.set_color('black')
		ax2.axhline(0, color='red', alpha=0.5, linestyle='--')
		#ax.legend(ncol=1)
		ax.legend(ncol=1, bbox_to_anchor=(0,0), loc="lower left", bbox_transform=fig.transFigure)
		ax2.legend(ncol=2, bbox_to_anchor=(1,0), loc="lower right", bbox_transform=fig.transFigure)
		ax.set_xmargin(0)
		ax2.set_xmargin(0)
		ax2.set_ylim(ymin=min(data['advantageAmount2']), ymax=max(data['advantageAmount1']))

		buf = io.BytesIO()
		plt.savefig(buf, format='png')#, transparent=True)
		buf.seek(0)
		calltime = int(time.time())

		return File(fp = buf, filename = f"{system.name}-{str(calltime)}.png", description = f"{system.name}-{str(calltime)}.png")

def setup(bot):
	bot.add_cog(SystemGrapher(bot))
