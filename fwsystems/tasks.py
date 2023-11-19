import datetime

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Sum
from eveuniverse.models import EveFaction, EveSolarSystem
from allianceauth.services.hooks import get_extension_logger

from fwsystems.models import System, SystemContest, Webhook
from fwsystems.providers import get_warzone
from fwsystems.task_helpers import create_contest_embed

logger = get_extension_logger(__name__)

@shared_task
def update_fw_esi():
	systems = System.objects.all()
	data = get_warzone()
	highContest = []

	for system in systems:
		entry = next((item for item in data if item['solarsystemID'] == system.system.id))

		sys_entry = SystemContest(
			system_id=entry['solarsystemID'],
			OwnerFactionID = EveFaction.objects.update_or_create_esi(id=entry['ownerFaction'])[0],
			OccupierFactionID = EveFaction.objects.update_or_create_esi(id=entry['occupierFaction'])[0],
			ContestedStatus = entry['contestedStatus'],
			ContestedAmount = entry['contestedAmount'],
			AdvantageFactionID1 = EveFaction.objects.update_or_create_esi(id=entry['advantage'][0]['factionID'])[0],
           	AdvantageTerrainAmount1 = entry['advantage'][0]['terrainAmount'],
           	AdvantageDynamicAmount1 = entry['advantage'][0]['dynamicAmount'],
           	AdvantageFactionID2 = EveFaction.objects.update_or_create_esi(id=entry['advantage'][1]['factionID'])[0] if len(entry['advantage']) > 1 else None,
           	AdvantageTerrainAmount2 = entry['advantage'][1]['terrainAmount'] if len(entry['advantage']) > 1 else 0,
           	AdvantageDynamicAmount2 = entry['advantage'][1]['dynamicAmount'] if len(entry['advantage']) > 1 else 0
		)

		sys_entry.save()

		if entry['contestedAmount'] * 100 > 80:
			highContest.append(sys_entry)

	if len(highContest) > 0:
		hook = Webhook.objects.all()[0]
		if hook.enabled:
			hook.send_embed(create_contest_embed(highContest))
		
		