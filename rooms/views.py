from django.shortcuts import render
from django.core.paginator import Paginator

# https://docs.djangoproject.com/en/4.0/ref/paginator/
from . import models


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5, allow_empty_first_page=True)
    rooms = paginator.page(page)
    # print(vars(rooms.paginator))
    return render(
        request,
        "rooms/home.html",
        context={"page": rooms},
    )
