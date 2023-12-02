from eveuniverse.models import EveFaction, EveSolarSystem

from fwsystems.models import System, SystemContest, Webhook

from datetime import datetime, timezone, timedelta

def get_contest_entries_sorted(system_id, days, retDateTime=False):
		systems = System.objects.all()
		contest_entries = SystemContest.objects.filter(system_id=system_id, created__range=(datetime.now() - timedelta(days=days), datetime.now()))
		
		time_data = []
		contest_data = []
		advantage_data1 = []
		advantage_data2 = []
		faction1 = contest_entries[len(contest_entries) - 1].AdvantageFactionID1.name
		faction2 = contest_entries[len(contest_entries) - 1].AdvantageFactionID2.name
		system, system_fetched = EveSolarSystem.objects.get_or_create_esi(id=system_id)
		title = system.name

		if contest_entries[0].AdvantageFactionID1.id == 500001:
			color1 = "blue"
			color2 = "green"
			colorcontest = "orange"
		elif contest_entries[0].AdvantageFactionID1.id == 500002:
			color1 = "red"
			color2 = "orange"
			colorcontest = "purple"
		elif contest_entries[0].AdvantageFactionID1.id == 500003:
			color1 = "orage"
			color2 = "red"
			colorcontest = "purple"
		elif contest_entries[0].AdvantageFactionID1.id == 500004:
			color1 = "green"
			color2 = "blue"
			colorcontest = "orange"
		else:
			color1 = "purple"
			color2 = "orange"
			colorcontest = "red"

		for entry in contest_entries:
			if retDateTime:
				time_data.append(entry.created)
			else:
				time_data.append(entry.created.strftime("%m-%d %H:%M"))

			contest_data.append(entry.ContestedAmount)
			netAdvantage = (entry.AdvantageTerrainAmount1 + entry.AdvantageDynamicAmount1) - (entry.AdvantageTerrainAmount2 + entry.AdvantageDynamicAmount2)
			if netAdvantage > 0:
				advantage_data1.append(netAdvantage)
				advantage_data2.append(0)
			else:
				advantage_data1.append(0)
				advantage_data2.append(netAdvantage)

		if contest_entries[len(contest_entries) - 1].OccupierFactionID.id != contest_entries[len(contest_entries) - 1].AdvantageFactionID1.id:
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

		data = {
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
		
		return data