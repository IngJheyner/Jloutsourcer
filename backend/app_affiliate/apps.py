"""
App Configuration for Affiliate module
"""
from django.apps import AppConfig


class AffiliateConfig(AppConfig):
    """Configuración de la aplicación Affiliate"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_affiliate'
    verbose_name = 'Affiliate Management'
