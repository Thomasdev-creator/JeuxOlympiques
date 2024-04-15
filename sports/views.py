from django.shortcuts import render, get_object_or_404
from .models import Sports


def all_sports(request):
    sports = Sports.objects.all()
    return render(request, 'sports/sports.html', {"sports": sports})


def sport_detail(request, slug):
    sport = get_object_or_404(Sports, slug=slug)
    return render(request, 'sports/sport_detail.html', {'sport': sport})
