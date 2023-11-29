import logging
import io
import time

from discord import Embed, User, Option, File
from discord.ext import commands
from datetime import datetime, timezone

from fwsystems.models import System, SystemContest, Webhook

from eveuniverse.models import EveFaction, EveSolarSystem

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from django.conf import settings
logger = logging.getLogger(__name__)

class SystemGrapher(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(name="graph", description="Display graph of contest and advantage for a system")
	async def graph_system(self, ctx, system_name: Option(str, "System Name to pull data")):
		try:
			system_id = EveSolarSystem.objects.filter(name=system_name)[0].id
		except:
			await ctx.respond(f"Could not find system {system_name}")
			return

		await ctx.defer()
		fileio = self.create_graph(system_id)
		await ctx.respond(file=fileio)

	def create_graph(self, system_id):
		
		contest_entries = SystemContest.objects.filter(system_id=system_id)
		time_data = []
		contest_data = []
		advantage_data1 = []
		advantage_data2 = []
		faction1 = contest_entries[0].AdvantageFactionID1.name
		faction2 = contest_entries[0].AdvantageFactionID2.name
		system, system_fetched = EveSolarSystem.objects.get_or_create_esi(id=system_id)

		if contest_entries[0].AdvantageFactionID1.id == 500001:
			color1 = "blue"
			color2 = "green"
			colorcontest = "orange"
		elif contest_entries[0].AdvantageFactionID1.id == 500002:
			color1 = "red"
			color2 = "yellow"
			colorcontest = "purple"
		elif contest_entries[0].AdvantageFactionID1.id == 500003:
			color1 = "yellow"
			color2 = "red"
			colorcontest = "purple"
		elif contest_entries[0].AdvantageFactionID1.id == 500004:
			color1 = "green"
			color2 = "blue"
			colorcontest = "orange"
		else:
			color1 = "purple"
			color2 = "orange"
			colorcontest = "red"

		for entry in contest_entries:
			time_data.append(entry.created)
			contest_data.append(entry.ContestedAmount)
			netAdvantage = (entry.AdvantageTerrainAmount1 + entry.AdvantageDynamicAmount1) - (entry.AdvantageTerrainAmount2 + entry.AdvantageDynamicAmount2)
			if netAdvantage > 0:
				advantage_data1.append(netAdvantage)
				advantage_data2.append(0)
			else:
				advantage_data1.append(0)
				advantage_data2.append(netAdvantage)

		#xdates = datetime.replace(contest_entries[len(contest_entries) - 1].created, tzinfo=timezone.utc)

		if contest_entries[len(contest_entries) - 1].OccupierFactionID != contest_entries[len(contest_entries) - 1].AdvantageFactionID1:
			temp = advantage_data1
			advantage_data1 = advantage_data2
			advantage_data2 = temp
			advantage_data1 = [ -x for x in advantage_data1 ]
			advantage_data2 = [ -x for x in advantage_data2 ]
			temp = color1
			color1 = color2
			color2 = temp
			temp = faction1
			faction1 = faction2
			faction2 = temp

		fig, ax = plt.subplots(figsize=(8, 3.8), layout='constrained')

		ax2 = ax.twinx()
		ax.plot(time_data, contest_data, color=colorcontest)
		ax.set_xlabel('Date/Time (UTC)')
		#ax.xaxis_date(tz='UTC')
		ax.set_ylabel('Contested %')
		ax.set_title(f"{system.name} - {contest_entries[len(contest_entries)-1].OccupierFactionID.name} Occupied")
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
		# ax.grid(visible=True, axis='y', color='black')
		ax.grid(visible=True, axis='x', which='major', color='black')
		ax.grid(visible=True, axis='x', which='minor', color='black')
		ax2.plot(time_data, advantage_data1, color=color1, label=f"{faction1} Advantage")
		ax2.plot(time_data, advantage_data2, color=color2, label=f"{faction2} Advantage")
		ax.yaxis.label.set_color('black')
		ax2.yaxis.label.set_color('black')
		ax2.axhline(0, color='red', alpha=0.5, linestyle='--')
		ax.set_xmargin(0)
		ax2.set_xmargin(0)
		#yabs_max = abs(max(ax2.get_ylim(), key=abs))
		#if ax2.get_ylim()[0] < -yabs_max + 30 and ax2.get_ylim()[1] > yabs_max - 30:
		ax2.set_ylim(ymin=min(advantage_data2), ymax=max(advantage_data1))

		buf = io.BytesIO()
		plt.savefig(buf, format='png')#, transparent=True)
		buf.seek(0)
		calltime = int(time.time())

		return File(fp = buf, filename = f"{system.name}-{str(calltime)}.png", description = f"{system.name}-{str(calltime)}.png")

def setup(bot):
	bot.add_cog(SystemGrapher(bot))
