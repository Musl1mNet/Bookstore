from django.conf import settings
from django.db import models
from django.utils.translation import get_language

languages = set([row[0] for row in settings.LANGUAGES])

def _get_i18n_property(field_name):
    @property
    def field_translation(self):
        return getattr(self, f"{field_name}_{get_language()}")

    return field_translation
def i18n(cls):
    if not issubclass(cls, models.Model):
        return cls
    for field in list(cls.__dict__.keys()):
        if len(field) < 4:
            continue
        if not (field[-3] == "_" and field[-2:] in languages):
            continue
        field_name, field_suffix = field[0:-3], field[-2:]
        if hasattr(cls, field_name):
            continue
        setattr(cls, field_name, _get_i18n_property(field_name))
    return cls