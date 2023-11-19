import datetime
import json
from typing import Iterable

from eveuniverse.models import EveFaction, EveSolarSystem
from allianceauth.services.hooks import get_extension_logger
from fwsystems.models import System, SystemContest, Webhook
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required("fwsystems.can_view_app")
def systemviewer(request) -> HttpResponse:
	systems = System.objects.all()
	system_id = request.GET.get('system_id', None)
	#chart = request.GET.get("chartcontainer", None)
	try:
		system, system_fetched = EveSolarSystem.objects.get_or_create_esi(id=system_id)
	except:
		system = None

	if system_id != None:
		contest_entries = SystemContest.objects.filter(system_id=system_id)
		contest_data = []
		advantage_data = []
		title = system.name

		for entry in contest_entries:
			contest_data.append({ "x" : int(entry.created.timestamp())*1000, "y" : entry.ContestedAmount})
		#	{ "x": 1646073000000, "y": 15.00 },
			advantage_data.append({"x" : int(entry.created.timestamp())*1000, "y" : entry.AdvantageTerrainAmount1})

		render_items = {
			"systems" : systems,
			"system" : system,
			"title" : title,
			"contestAmount": contest_data,
			"advantageAmount": advantage_data,
			
			"contest_entries" : contest_entries
		}
	else:
		render_items = {
			"systems" : systems,
			"system" : system,
		}

	return render(request, "fwsystems/systemviewer.html", render_items)
