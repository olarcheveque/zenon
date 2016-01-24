from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from erudit.models import Journal as CoreJournal


PERMISSIONS = (

    ('permissions.journal:can_access', _('[Revue] Peut accéder à la revue')),
    ('permissions.journal:can_change', _('[Revue] Peut modifier la revue')),

    ('all:can_add_issuesubmission',
        _('[Utilisateur] Peut déposer un nouveau numéro')),
    ('all:can_access_issuesubmission',
        _('[Utilisateur] Peut accéder au dépôt de fichiers')),
    ('all:can_change_issuesubmission',
        _('[Utilisateur] Peut modifier le dépôt de fichiers')),
    ('all:can_change_journal',
        _('[Utilisateur] Peut modifier les revues')),
)


class Journal(CoreJournal):
    class Meta:
        proxy = True
        verbose_name = _('Revue')


class Rule(models.Model):
    date_creation = models.DateTimeField(
        editable=False,
        null=True,
        default=timezone.now,
        verbose_name=_("Date de création")
    )
    date_modification = models.DateTimeField(
        editable=False,
        null=True,
        default=timezone.now,
        verbose_name=_("Date de modification")
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Type'),
        blank=True,
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField(blank=True, null=True)

    user = models.ForeignKey('auth.User', blank=True, null=True)
    group = models.ForeignKey('auth.Group', blank=True, null=True)
    permission = models.CharField(choices=PERMISSIONS, max_length=100)

    class Meta:
        verbose_name = _("Règle")

    def clean(self):
        if not self.user and not self.group:
            raise ValidationError(_('Choisissez un utilisateur OU un groupe'))
        if self.user and self.group:
            raise ValidationError(_('Choisissez SOIT un utilisateur SOIT un groupe'))
        if (self.content_type or self.object_id) and self.permission.startswith('all:'):
            raise ValidationError(
                _('Impossible de changer la permission liée à un objet en particulier'))

            raise ValidationError(_('Choisissez SOIT un utilisateur SOIT un groupe'))
