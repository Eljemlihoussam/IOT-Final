from django.urls import path
from . import views, api

urlpatterns = [
    path("api/", api.Dlist, name="json"),
    path("api/post/", api.Dhtviews.as_view(), name="json"),
    path("latest/", views.latest_json, name="latest_json"),
    path("", views.dashboard, name="dashboard"),
    path("graph_temp/", views.graph_temp, name="graph_temp"),
    path("graph_hum/", views.graph_hum, name="graph_hum"),
    path("incidents/", views.incidents, name="incidents"),
]