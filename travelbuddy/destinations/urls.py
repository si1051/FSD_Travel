from django.urls import include, path
from .views import UpdateDestinationView
from .views import (
    HomeView,
    AddDestinationFormView,
    DestinationDetailSlugView,
)

urlpatterns = [
    path('dashboard', HomeView.as_view(), name='home'),
    path('destination/add', AddDestinationFormView.as_view(), name='add_trip'),
    # path('destination/update/', UpdateDestinationView.as_view(), name='destination_update'),
    path('destination/update/', UpdateDestinationView, name='destination_update'),
    path('destination/<slug:slug>/', DestinationDetailSlugView.as_view(), name='detail'),
]
