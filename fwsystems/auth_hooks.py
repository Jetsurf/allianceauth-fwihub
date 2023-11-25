from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls

class FwSystemsSystemsViewer(MenuItemHook):

	def __init__(self):
		MenuItemHook.__init__(self, _("System Viewer"), "fas fa-store-alt fa-fw", "fwsystems:systemviewer", navactive=["fwsystems:systemviewer"])

	def render(self, request):
		if request.user.has_perm("fwsystems.can_view_app"):
			return MenuItemHook.render(self, request)

		return ""

@hooks.register("menu_item_hook")
def register_menu() -> FwSystemsSystemsViewer:
	return FwSystemsSystemsViewer()

@hooks.register("url_hook")
def register_urls() -> UrlHook:
	return UrlHook(urls, "fwsystems", r"^fwsystems/")

@hooks.register('discord_cogs_hook')
def register_cogs():
    return ["fwsystems.cogs.systemgrapher"]

	