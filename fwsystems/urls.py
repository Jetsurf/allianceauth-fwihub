from django.urls import path

from . import views

app_name = "fwsystems"

urlpatterns = [
	path('', views.systemviewer, name="index"),
	path('systemviewer', views.systemviewer, name="systemviewer"),
]