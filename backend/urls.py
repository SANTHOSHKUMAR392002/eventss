from django.urls import path
from .views import admin_login, admin_logout, dashboard, event_create, add_event, event_list, event_update, event_delete, member_list, event_members_page

urlpatterns = [
    path("admin-login/", admin_login, name="admin-login"),
    path("admin-logout/", admin_logout, name="admin-logout"),  
    path("dashboard/", dashboard, name="dashboard"),
    path('event-create/', event_create, name='event-create'),
    path('add-event/', add_event, name='add-event'),
    path("event-list/", event_list, name="event-list"),
    path('event-update/<int:pk>/', event_update, name='event-update'),
    path('event-delete/<int:pk>/', event_delete, name='event-delete'),
    path('members/', member_list, name='member-list'),
    path('event-members/', event_members_page, name='event_members_page'),  # Page to select event and view members

]
