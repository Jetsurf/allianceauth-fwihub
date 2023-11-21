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
		time_data = []
		contest_data = []
		advantage_data1 = []
		advantage_data2 = []
		faction1 = contest_entries[0].AdvantageFactionID1.name
		faction2 = contest_entries[0].AdvantageFactionID2.name
		title = system.name

		if contest_entries[0].AdvantageFactionID1.id == 500004:
			color1 = "green"
			color2 = "blue"
		elif contest_entries[0].AdvantageFactionID1.id == 500001:
			color1 = "blue"
			color2 = "green"
		elif contest_entries[0].AdvantageFactionID1.id == 500002:
			color1 = "red"
			color2 = "yellow"
		elif contest_entries[0].AdvantageFactionID1.id == 500003:
			color1 = "yellow"
			color2 = "red"
		else:
			color1 = "purple"
			color2 = "orange"

		for entry in contest_entries:
			time_data.append(entry.created.strftime("%m-%d %H:%M"))
			contest_data.append(round(entry.ContestedAmount * 100, 2))
			netAdvantage = (entry.AdvantageTerrainAmount1 + entry.AdvantageDynamicAmount1) - (entry.AdvantageTerrainAmount2 + entry.AdvantageDynamicAmount2)
			if netAdvantage > 0:
				advantage_data1.append(abs(netAdvantage))
				advantage_data2.append(0)
			else:
				advantage_data1.append(0)
				advantage_data2.append(abs(netAdvantage))

		render_items = {
			"systems" : systems,
			"system" : system,
			"title" : title,
			"contestAmount": contest_data,
			"advantageAmount1" : advantage_data1,
			"advantageAmount2" : advantage_data2,
			"color1" : color1,
			"color2" : color2,
			"faction1" : faction1,
			"faction2" : faction2,
			"timeData" : time_data,
			"contest_entries" : contest_entries
		}
	else:
		render_items = {
			"systems" : systems,
			"system" : system,
		}

	return render(request, "fwsystems/systemviewer.html", render_items)
