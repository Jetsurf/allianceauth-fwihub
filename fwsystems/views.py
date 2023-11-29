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
@permission_required("auth.fwsystems_view")
def systemviewer(request) -> HttpResponse:
	systems = System.objects.all()
	system_id = request.GET.get('system_id', 0)
	#chart = request.GET.get("chartcontainer", None)
	try:
		system, system_fetched = EveSolarSystem.objects.get_or_create_esi(id=system_id)
	except:
		system = 0

	if int(system_id) > 0:
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
			color2 = "rgb(51, 153, 255)"
			colorcontest = "orange"
		elif contest_entries[0].AdvantageFactionID1.id == 500001:
			color1 = "rgb(51, 153, 255)"
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
		else:
			color1 = "purple"
			color2 = "orange"
			colorcontest = "red"

		for entry in contest_entries:
			time_data.append(entry.created.strftime("%m-%d %H:%M"))
			contest_data.append(round(entry.ContestedAmount * 100, 2))
			netAdvantage = (entry.AdvantageTerrainAmount1 + entry.AdvantageDynamicAmount1) - (entry.AdvantageTerrainAmount2 + entry.AdvantageDynamicAmount2)
			if netAdvantage > 0:
				advantage_data1.append(netAdvantage)
				advantage_data2.append(0)
			else:
				advantage_data1.append(0)
				advantage_data2.append(netAdvantage)

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

		render_items = {
			"systems" : systems,
			"system" : system,
			"title" : title,
			"owner" : contest_entries[len(contest_entries)-1].OccupierFactionID.name,
			"contestAmount": contest_data,
			"advantageAmount1" : advantage_data1 ,
			"advantageAmount2" : advantage_data2,
			"color1" : color1,
			"color2" : color2,
			"colorcontest" : colorcontest,
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
