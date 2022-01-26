from django.views.generic import ListView
from django.http import Http404

# from django.urls import reverse
from django.shortcuts import render
from . import models


class HomeView(ListView):
    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    # page_kwarg = "papa"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})

    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        raise Http404()
        # templates 폴더 내 404.html을 찾아서 보여줌.
