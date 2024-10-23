from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BasesConfig(AppConfig):
    name = "superclub.bases"
    verbose_name = _("Bases")
