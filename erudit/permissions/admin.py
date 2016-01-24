from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import ugettext_lazy as _

from .models import Rule, Journal
from .forms import RuleForm


class RuleInline(GenericTabularInline):
    model = Rule
    extra = 0

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        """
        Filter permissions according context model
        """
        if db_field.name == 'permission':
            app_label = self.parent_model._meta.app_label.lower()
            klass = self.parent_model.__name__.lower()
            prefix = "{}.{}:".format(app_label, klass)
            choices = db_field.choices
            choices = [item for item in choices if item[0].startswith(prefix)]
            kwargs['choices'] = choices
        return db_field.formfield(**kwargs)


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm
    list_display = (
        'id',
        'user',
        'group',
        'permission',
        'content_type',
        '_content_object',
        'date_modification',
        'date_creation',

    )
    list_filter = ('content_type', )

    def _content_object(self, obj):
        if not obj.content_object:
            return
        else:
            return str(obj.content_object)
    _content_object.short_description = _("Objet")
    _content_object.allow_tags = True


class JournalAdmin(admin.ModelAdmin):
    inlines = (RuleInline, )
    fields = ('name', )
    readonly_fields = ('name', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, pk=None):
        return False


admin.site.register(Journal, JournalAdmin)
admin.site.register(Rule, RuleAdmin)
