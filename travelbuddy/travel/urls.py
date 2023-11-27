"""
URL configuration for travelbuddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', include(('apps.accounts.urls', 'account'), namespace='account')),  # Removed the 'r'^' as it's not required
    path('travel/', include(('apps.destinations.urls', 'travel'), namespace='travel')),  # Removed the 'r'^' as it's not required
    path('logout/', LogoutView.as_view(), name='logout'),  # Removed the 'r'^' as it's not required
    path('admin/', admin.site.urls),  # Removed the 'r'^' as it's not required
]

if settings.DEBUG:  # If it is in debug mode
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Concatenate the static URLs correctly
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Concatenate the static URLs correctly

