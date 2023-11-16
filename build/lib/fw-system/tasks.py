import datetime

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Sum
from eveuniverse.models import EveFaction, EveRegion, EveSolarSystem
from allianceauth.eveonline.models import EveFaction, EveRegion, EveSolarSystem
from allianceauth.services.hooks import get_extension_logger

from fwsystems.models import System, Webhook
from fwsystems.providers import get_fw_systems

logger = get_extension_logger(__name__)

@shared_task
def update_fw_esi():
	systems = System.objects.all()
	response = requests.get(self.API_URL)
	data = get_warzone()
	for system in systems:
		entry = next((item for item in data if item['solarsystemID'] == system.system.id))

		system.contest_entry_create(system.system.id,
			OwnerFactionID = entry['ownerFaction'],
			OccupierFactionID = entry['occupierFaction'],
			ContestedStatus = entry['contestedStatus'],
			ContestedAmount = entry['contestedAmount'],
			AdvantageFactionID1 = entry['advantage'][0]['factionID'],
           	AdvantageTerrainAmount1 = entry['advantage'][0]['terrainAmount'],
           	AdvantageDynamicAmount1 = entry['advantage'][0]['dynamicAmount'],
           	AdvantageFactionID2 = entry['advantage'][1]['factionID'] if len(entry['advantage']) > 1 else None,
           	AdvantageTerrainAmount2 = entry['advantage'][1]['terrainAmount'] if len(entry['advantage']) > 1 else 0,
           	AdvantageDynamicAmount2 = entry['advantage'][1]['dynamicAmount'] if len(entry['advantage']) > 1 else 0
		)