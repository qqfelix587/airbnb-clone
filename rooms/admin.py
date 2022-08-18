from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):
    # foreign key 덕에 다른 model을 control할 수 있음.
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""


    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "Spaces",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                )
            },
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )
    list_display = (
        "name",
        "host",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )
    raw_id_fields = ("host",)
    search_fields = ["city", "^host__username"]
    # Prefix	Lookup
    # ^	startswith
    # =	iexact
    # @	search

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )
    ordering = ("name", "price")

    def count_amenities(self, obj):
        return obj.amenities.count()

    # count_amenities.short_description = "amenities"
    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # return f'<img source="{obj.file.url}'
        # 위와 같이 실행시 동작하지 않음 -> django가 자동으로 해당 html을 배제 -> security
        # obj.file 안에는 height, width 등 다양한 property가 존재
        print(obj.file.url)
        return mark_safe(f'<img width=50px src="{obj.file.url}"')

    get_thumbnail.short_description = "Thumbnail"
