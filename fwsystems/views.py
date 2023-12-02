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
from fwsystems.view_helpers import get_contest_entries_sorted

@login_required
@permission_required("auth.fwsystems_view")
def systemviewer(request) -> HttpResponse:
	systems = System.objects.all()
	system_id = request.GET.get('system_id', 0)
	num_days = request.GET.get('num_days', 7)

	try:
		system, system_fetched = EveSolarSystem.objects.get_or_create_esi(id=system_id)
	except:
		system = 0

	if int(system_id) > 0:
		render_items = get_contest_entries_sorted(system_id, num_days)
	else:
		render_items = {
			"systems" : systems,
			"system" : system,
		}

	return render(request, "fwsystems/systemviewer.html", render_items)
