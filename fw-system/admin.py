from django.contrib import admin
from allianceauth.services.hooks import get_extension_logger
from eveuniverse.models import EveFaction, EveRegion, EveSolarSystem

from fwsystems.models import System, Faction, Webhook

from .admin_helpers import list_2_html_w_tooltips

logger = get_extension_logger(__name__)

@admin.register(Faction)
class FactionConfigAdmin(admin.ModelAdmin):
        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == "faction":
                kwargs["queryset"] = EveFaction.objects.filter(eve_faction__id__in=[500001:500004], published=1)

        @admin.action(description="Fetch systems for faction")
        def run_systems_check(modeladmin, request, queryset):
