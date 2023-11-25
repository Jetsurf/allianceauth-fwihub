from datetime import datetime

from allianceauth import hooks
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Sum
from eveuniverse.models import EveFaction, EveSolarSystem
from allianceauth.services.hooks import get_extension_logger

from fwsystems.models import System, SystemContest, Webhook
from fwsystems.providers import get_warzone
from fwsystems.task_helpers import create_contest_embed

from fwsystems.app_settings import ( FWSYSTEMS_LOG_ALL_SYSTEMS, FWSYSTEMS_ALERT_THRESHOLD )

from django.contrib.auth.models import User
from django.apps import apps

logger = get_extension_logger(__name__)

@shared_task
def update_fw_esi():
	systems = System.objects.all()
	data = get_warzone()

	if not FWSYSTEMS_LOG_ALL_SYSTEMS:
		for system in systems:	
			entry = next((item for item in data if item['solarsystemID'] == system.system.id))

			if entry['contetedStatus'] is "Uncontested":
				continue

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
	else:
		for entry in data:
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

@shared_task
def send_fw_notifications():
	systems = System.objects.all()
	highContest = []

	for sys in systems:
		entry = SystemContest.objects.filter(system_id=sys.system_id).latest("created")

		if entry.ContestedAmount * 100 > FWSYSTEMS_ALERT_THRESHOLD:
				highContest.append(entry)

	if len(highContest) > 0:
		hook = Webhook.objects.all()[0]
		if hook.enabled:
			hook.send_embed(create_contest_embed(highContest))
