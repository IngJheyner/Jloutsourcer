"""
API URLs

Rutas de la API REST para afiliados y aportes.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AffiliateViewSet, ContributionViewSet

# Router principal
router = DefaultRouter()
router.register(r'affiliates', AffiliateViewSet, basename='affiliate')

# URLs manuales para contributions anidadas
urlpatterns = [
    path('', include(router.urls)),
    path(
        'affiliates/<int:affiliate_pk>/contributions/',
        ContributionViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='affiliate-contributions-list'
    ),
]

