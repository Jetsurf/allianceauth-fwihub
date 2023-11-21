import re
from django.apps import apps
from django.conf import settings

FWSYSTEMS_ERROR_COLOR = getattr(settings, "FWSYSTEMS_ERROR_COLOR", 16711710)
FWSYSTEMS_WARNING_COLOR = getattr(settings, "FWSYSTEMS_WARNING_COLOR", 14177041)
FWSYSTEMS_INFO_COLOR = getattr(settings, "FWSYSTEMS_INFO_COLOR", 42751)
FWSYSTEMS_SUCCESS = getattr(settings, "FWSYSTEMS_SUCCESS_COLOR", 6684416)
FWSYSTEMS_LOG_ALL_SYSTEMS = getattr(settings, "FSYSTEMS_LOG_ALL_SYSTEMS", True)
FWSYSTEMS_ALERT_THRESHOLD = getattr(settings, "FWSYSTEMS_ALERT_THRESHOLD", 90)