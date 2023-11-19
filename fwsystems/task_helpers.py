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
		embed.add_field(name=f"{sys.system.name}", value=f"{str(round(sys.ContestedAmount * 100, 2))}%", inline=True)

	return embed