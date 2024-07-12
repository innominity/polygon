from django.contrib import admin
from .models import RemoteApp, RemoteAppFileConfigType, RemoteAppTask, RemoteAppTaskFileConfig


class RemoteAppAdmin(admin.ModelAdmin):
    list_display = ["guid", "name", "description", "slug", "date_created"]
    list_display_links = ["guid", "name", "slug"]
    search_fields = ["guid", "name", "slug"]

admin.site.register(RemoteApp, RemoteAppAdmin)

class RemoteAppFileConfigTypeAdmin(admin.ModelAdmin):
    list_display = []
    list_display_links = []
    search_fields = []

admin.site.register(RemoteAppFileConfigType, RemoteAppFileConfigTypeAdmin)

class RemoteAppTaskAdmin(admin.ModelAdmin):
    list_display = []
    list_display_links = []
    search_fields = []

admin.site.register(RemoteAppTask, RemoteAppTaskAdmin)

class RemoteAppTaskFileConfigAdmin(admin.ModelAdmin):
    list_display = []
    list_display_links = []
    search_fields = []

admin.site.register(RemoteAppTaskFileConfig, RemoteAppTaskFileConfigAdmin)