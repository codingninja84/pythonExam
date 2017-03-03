from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.success, name="success"),
    url(r'^add$', views.create_plan, name="create_plan"),
    url(r'^new-trip$', views.new_trip, name="new_trip"),
    url(r'^destination/(?P<trip_id>\d+)$', views.view, name="view"),
    url(r'^join/(?P<trip_id>\d+)$', views.join, name="join")
]
