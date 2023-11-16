from django.contrib import admin
from allianceauth.services.hooks import get_extension_logger
from eveuniverse.models import EveFaction, EveRegion, EveSolarSystem

from fwsystems.models import System, Webhook

from .admin_helpers import list_2_html_w_tooltips

logger = get_extension_logger(__name__)

@admin.register(System)
class SystemConfigAdmin(admin.ModelAdmin):
    filter_horizontal = ["System"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "System":
            kwargs['queryset'] = System.objects.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
