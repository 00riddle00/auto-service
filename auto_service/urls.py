"""
URL configuration for auto_service project.

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
from django.contrib import admin
from django.urls import include, path

from service import views as service_views

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("accounts/", include("django.contrib.auth.urls")),
        path("accounts/register/", service_views.register, name="register"),
        path(
            "accounts/register/done/",
            service_views.register_complete,
            name="register-complete",
        ),
        path("tinymce/", include("tinymce.urls")),
        path("i18n/", include("django.conf.urls.i18n")),
        path("", include("service.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
