import datetime
from decimal import Decimal

from discord import SyncWebhook
from eveuniverse.models import EveFaction, EveRegion, EveSolarSystem
from solo.models import SingletonModel

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from allianceauth.eveonline.models import EveFaction, EveRegion, EveSolarSystem
from allianceauth.services.hooks import get_extension_logger

class System(models.Model):
    system = models.ForeignKey( EveSolarSystem,
        verbose_name=_("System"),
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

    def contest_entry_create(self, *args, **kwargs):
        entry = SystemContest(system,
            OwnerFactionID,
            OccupierFactionID,
            ContestedStatus,
            ContestedAmount,
            AdvantageFactionID1,
            AdvantageTerrainAmount1,
            AdvantageDynamicAmount1,
            AdvantageFactionID2,
            AdvantageTerrainAmount2,
            AdvantageDynamicAmount2
        )
        entry.save()

class SystemContest(models.Model)

    system = models.ForeignKey("System", related_name="contestentry")
    
    OwnerFactionID = models.ForeignKey(EveFaction,
        verbose_name=_("Owning Faction"),
        on_delete=models.CASCADE
    )

    OccupierFactionID = models.ForeignKey(EveFaction,
        verbose_name=__("Occupying Faction"),
    )

    ContestedStatus = models.TextField()

    ContestedAmount = models.FloatField()

    AdvantageFactionID1 = models.ForeignKey(EveFaction,
        verbose_name=_("Faction Advantage 1"),
        on_delete=models.CASCADE
    )

    AdvantageTerrainAmount1 = models.FloadField()

    AdvantageDynamicAmount1 = models.FloadField()

    AdvantageFactionID2 = models.foreignKey(EveFaction,
        verbose_name=_("Faction Advantage 2"),
        on_delete=models.CASCADE
    )

    AdvantageTerrainAmount2 = models.FloadField()

    AdvantageDynamicAmount2 = models.FloadField()

class Webhook(models.Model):
    name=models.CharField(_("Name"),
        url=models.URLField(_("URL")),
        max_length=200,
    )

    def __str__(self):
        return self.name

    def send_embed(self, embed):
        webhook=SyncWebhook.from_url(self.url)
        webhook.send(embed=embed, username="FW System iHub Check")

    class Meta:
        default_permissions=()

