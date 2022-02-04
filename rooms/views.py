from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):
    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    # page_kwarg = "papa"
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """RoomDetail Definition"""

    # https://ccbv.co.uk/projects/Django/4.0/django.views.generic.detail/DetailView/
    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    room_types = models.RoomType.objects.all()
    return render(
        request,
        "rooms/search.html",
        {"city": city, "countries": countries, "room_types": room_types},
    )
