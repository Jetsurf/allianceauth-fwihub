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

class Faction(models.Model):
    faction = models.ForeignKey( EveFaction,
        verbose_name=_("Faction"),
        on_delete=models.CASCADE
    )
    systems = sodels.ForeignKey( EveSolarSystem
        verbose_name=_("Watched Systems"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class System(models.Model):
    system = models.ForeignKey( EveSolarSystem,
        verbose_name=_("System")
        on_delete=models.CASCADE
    )
    vp = models.IntegerField(_("Victory Points")
        help_text="Victory Points for a System",
        default=0,
    )
    threshold = models.IntegerField(_("System Threshold")
        help_text="Victory Points Threshold",
        default=0
    )
    noti_sent = models.DateTimeField(
        verbose_name=_("Notification last sent"),
        null=True,
        Blank=True,
        help_text="Last time a notification was sent for a system",
        editable=False
    )

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
