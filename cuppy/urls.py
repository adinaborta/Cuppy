"""cuppy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework import routers
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from cuppy.cuppy import views


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"plant_requirement", views.RequirementViewSet)
router.register(r"plants", views.PlantViewSet)
router.register(r"sensors", views.SensorActuatorViewSet)
router.register(r"central", views.CentralClientViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Cuppy API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ihorvalds@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("sensor_control/", views.StartStopSensors.as_view(), name="sensors"),
    path(
        "central_control/", views.StartStopCentralSubscriber.as_view(), name="central"
    ),
    path("actuator_control/", views.StartStopActuators.as_view(), name="actuator"),
    path("initialize_custom/", views.InitializePlantCustom.as_view(), name="initialize_custom"),
    path("initialize/", views.InitializePlant.as_view(), name="initialize"),

    path("", include(router.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
