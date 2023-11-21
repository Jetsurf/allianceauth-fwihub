import datetime
import random
from typing import Union

from discord import Embed
from eveuniverse.models import EveFaction, EveSolarSystem

from fwsystems.models import System, SystemContest, Webhook
from fwsystems.app_settings import ( FWSYSTEMS_WARNING_COLOR )

def create_contest_embed(systems: list):
	embed = Embed()
	embed.timestamp = datetime.datetime.now()
	embed.set_footer(icon_url="", text=f"FW Systems Check")

	embed.title = f"Systems - Close to Vulnerable"
	embed.colour = FWSYSTEMS_WARNING_COLOR
	for sys in systems:
		advFact = sys.AdvantageFactionID1
		netAdvantage = (sys.AdvantageTerrainAmount1 + sys.AdvantageDynamicAmount1) - (sys.AdvantageTerrainAmount2 + sys.AdvantageDynamicAmount2)
		if netAdvantage < 0:
			advFact = sys.AdvantageFactionID2

		if netAdvantage < 0:
			embed.add_field(name=f"{sys.system.name}", value=f"{round(sys.ContestedAmount * 100, 2)}%\nAdv - {abs(netAdvantage)}% - {advFact.name}", inline=True)
		else:
			embed.add_field(name=f"{sys.system.name}", value=f"{round(sys.ContestedAmount * 100, 2)}%\nAdv - {abs(netAdvantage)}%", inline=True)
	return embed