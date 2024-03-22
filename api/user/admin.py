from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FriendRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "name", "friends", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "friends",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email",)


admin.site.register(FriendRequest)
