import os
from allianceauth import __version__ as aa__version__
from allianceauth.services.hooks import get_extension_logger
from esi.clients import EsiClientProvider
from . import __version__ as mm__version__

logger = get_extension_logger(__name__)
SWAGGER_SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')
esi = EsiClientProvider(spec_file=SWAGGER_SPEC, app_info_text=(f"allianceauth v{aa__version__} & aa-fw-system-checks v{mm__version__}"))

def get_fw_systems():
	result = esi.client.Fw.get_fw_systems().results()
	return result
