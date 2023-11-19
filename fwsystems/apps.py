from django.apps import AppConfig
from . import __version__

class FWSystemsConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = "fwsystems"
	verbose_name=f"AA FW Systems Check v{__version__}"