import datetime

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Sum
from eveuniverse.models import EveFaction, EveRegion, EveSolarSystem
from allianceauth.eveonline.models import EveFaction, EveRegion, EveSolarSystem
from allianceauth.services.hooks import get_extension_logger

from fwsystems.models import Faction, System, Webhook
from fwsystems.providers import get_fw_systems

logger = get_extension_logger(__name__)

def run_systems_check(id: int):
	faction = Faction.objects.get(id=id)

	systems = get_fw_systems()
	print(systems)