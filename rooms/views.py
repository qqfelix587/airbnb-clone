from django.views.generic import ListView, DetailView
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

    model = models.Room
