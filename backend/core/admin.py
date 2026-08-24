from django.contrib import admin

from .models import Driver, Event, Result, Session, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "base", "color")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "team", "active")
    list_filter = ("team", "active")
    search_fields = ("name", "number")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("round_number", "name", "circuit", "date", "has_sprint")
    list_filter = ("has_sprint",)
    search_fields = ("name", "circuit")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("event", "session_type", "session_number", "name")
    list_filter = ("event", "session_type")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("session", "driver", "position", "time", "status", "points")
    list_filter = ("session__event", "status")
    search_fields = ("driver__name",)
