import re
from django.apps import apps
from django.conf import settings

FWSYSTEMS_UPDATE_SYSTEMS = getattr(settings, "FWSYSTEMS_UPDATE_SYSTEMS", 3)
FWSYSTEMS_ERROR_COLOR = getattr(settings, "FWSYSTEMS_ERROR_COLOR", 16711710)
FWSYSTEMS_WARNING_COLOR = getattr(settings, "FWSYSTEMS_WARNING_COLOR", 14177041)
FWSYSTEMS_INFO_COLOR = getattr(settings, "FWSYSTEMS_INFO_COLOR", 42751)
FWSYSTEMS_SUCCESS = getattr(settings, "FWSYSTEMS_SUCCESS_COLOR", 6684416)
