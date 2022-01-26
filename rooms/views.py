from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage

# https://docs.djangoproject.com/en/4.0/ref/paginator/
from . import models


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5, allow_empty_first_page=True)
    try:
        rooms = paginator.page(page)
        return render(
            request,
            "rooms/home.html",
            context={"page": rooms},
        )
    except EmptyPage:  # Exception으로 쓸 경우 모든 경우
        return redirect("/")

    # print(vars(rooms.paginator))
