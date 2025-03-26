from django.contrib import admin
from .models import Event, Member  # Import your models

# Customize Event Admin
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'venue', 'start_date', 'end_date', 'status', 'no_of_members')
    search_fields = ('name', 'venue', 'status')
    list_filter = ('status', 'start_date')

# Customize Member Admin
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'event')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('event',)


# Register Models
admin.site.register(Event, EventAdmin)
admin.site.register(Member, MemberAdmin)
