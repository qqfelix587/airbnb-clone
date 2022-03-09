from csv import list_dialects
from django.contrib import admin
from . import models


class ProgressListFilter(admin.SimpleListFilter):
    title = "In Progress"
    parameter_name = "in_progress"

    def lookups(self, request, model_admin):
        return (
            ("True", "True"),
            ("False", "False"),
        )

    def queryset(self, request, queryset):
        now = models.Reservation.get_now_date()

        if self.value() == "True":
            return queryset.filter(check_in__lte=now, check_out__gte=now)
        elif self.value() == "False":
            return queryset.exclude(check_in__lte=now, check_out__gte=now)


class FinishedListFilter(admin.SimpleListFilter):
    title = "Is Finished"
    parameter_name = "is_finished"

    def lookups(self, request, model_admin):
        return (("True", "True"), ("False", "False"))

    def queryset(self, request, queryset):
        now = models.Reservation.get_now_date()

        if self.value() == "True":
            return queryset.filter(check_out__lt=now)
        elif self.value() == "False":
            return queryset.exclude(check_out__lt=now)


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin Definition"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status", ProgressListFilter, FinishedListFilter)


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    """BookedDay Admin Definition"""

    list_display = ("day", "reservation")
