import datetime
from decimal import Decimal

from discord import SyncWebhook
from eveuniverse.models import EveFaction, EveSolarSystem
from solo.models import SingletonModel

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from allianceauth.services.hooks import get_extension_logger

class Faction(models.Model):
	faction = models.ForeignKey( EveFaction,
		verbose_name=_("Faction"),
		on_delete=models.CASCADE
	)

	def save(self, *args, **kwargs):
		if not self.pk and Faction.objects.exists():
			raise ValidationError("Only one webhook is allowed currently")
		return super(Faction, self).save(*args, **kwargs)

class System(models.Model):
	system = models.ForeignKey( EveSolarSystem,
		verbose_name=_("System"),
		on_delete=models.CASCADE
	)

	created = models.DateTimeField(auto_now_add=True)

class SystemContest(models.Model):
	system = models.ForeignKey(EveSolarSystem,
		verbose_name=_("System"),
		on_delete=models.CASCADE
	)

	created = models.DateTimeField(auto_now_add=True)
	
	OwnerFactionID = models.ForeignKey(EveFaction,
		verbose_name=_("Owning Faction"),
		on_delete=models.CASCADE,
		related_name="owning_faction"
	)

	OccupierFactionID = models.ForeignKey(EveFaction,
		verbose_name=_("Occupying Faction"),
		on_delete=models.CASCADE,
		related_name="occupier_faction"
	)

	ContestedStatus = models.TextField()

	ContestedAmount = models.FloatField()

	AdvantageFactionID1 = models.ForeignKey(EveFaction,
		verbose_name=_("Faction Advantage 1"),
		on_delete=models.CASCADE,
		related_name="advantage_faction1"
	)

	AdvantageTerrainAmount1 = models.FloatField()

	AdvantageDynamicAmount1 = models.FloatField()

	AdvantageFactionID2 = models.ForeignKey(EveFaction,
		verbose_name=_("Faction Advantage 2"),
		on_delete=models.CASCADE,
		related_name="advantage_faction2",
		null=True
	)

	AdvantageTerrainAmount2 = models.FloatField()

	AdvantageDynamicAmount2 = models.FloatField()

class Webhook(models.Model):
	Name=models.CharField(_("Name"),
		max_length=100
	)

	URL=models.URLField(_("URL"),
		max_length=200,
	)

	enabled = models.BooleanField(default=True)

	def __str__(self):
		return self.Name

	def send_embed(self, embed):
		webhook=SyncWebhook.from_url(self.URL)
		webhook.send(embed=embed, username="FW System iHub Check")

	def save(self, *args, **kwargs):
		if not self.pk and Webhook.objects.exists():
			raise ValidationError("Only one webhook is allowed currently")
		return super(Webhook, self).save(*args, **kwargs)
