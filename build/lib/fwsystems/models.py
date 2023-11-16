import datetime
from decimal import Decimal

from discord import SyncWebhook
from eveuniverse.models import EveFaction, EveSolarSystem
from solo.models import SingletonModel

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from allianceauth.services.hooks import get_extension_logger

class System(models.Model):
    system = models.ForeignKey( EveSolarSystem,
        verbose_name=_("System"),
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

class SystemContest(models.Model):

    System = models.ForeignKey("System",
        verbose_name="System Name",
        related_name="system_name",
        on_delete=models.CASCADE,
    )
    
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
        related_name="advantage_faction2"
    )

    AdvantageTerrainAmount2 = models.FloatField()

    AdvantageDynamicAmount2 = models.FloatField()

class Webhook(models.Model):
    name=models.URLField(_("URL"),
        max_length=200,
    )

    def __str__(self):
        return self.name

    def send_embed(self, embed):
        webhook=SyncWebhook.from_url(self.url)
        webhook.send(embed=embed, username="FW System iHub Check")

    class Meta:
        default_permissions=()

