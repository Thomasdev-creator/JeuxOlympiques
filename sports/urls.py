from django.urls import path

from sports.views import all_sports, sport_detail

app_name = 'sports'

urlpatterns = [
    path('all-sports/', all_sports, name='all-sports'),
    path('sport-detail/<str:slug>/', sport_detail, name='sport-detail'),
]