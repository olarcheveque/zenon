from django.contrib.contenttypes.models import ContentType

import rules

from permissions.models import Rule


@rules.predicate
def is_superuser(user):
    return user.is_superuser


@rules.predicate
def is_staff(user):
    return user.is_staff


@rules.predicate
def can_access_journal(user, journal):
    ct_journal = ContentType.objects.get(app_label="erudit", model="journal")
    return Rule.objects.filter(
        content_type=ct_journal,
        user=user,
        object_id=journal.id,
        permission='permissions.journal:can_access'
    ).count()


@rules.predicate
def can_change_journal(user, journal):
    if not journal:
        return bool(Rule.objects.filter(
            user=user,
            permission='all:can_change_journal'
        ).count())
    ct_journal = ContentType.objects.get(app_label="erudit", model="journal")
    return Rule.objects.filter(
        content_type=ct_journal,
        user=user,
        object_id=journal.id,
        permission='permissions.journal:can_change'
    ).count()


@rules.predicate
def can_change_issuesubmission(user, issuesubmission):
    can_change_issue_submission = bool(Rule.objects.filter(
        user=user,
        permission='all:can_change_issuesubmission'
    ).count())
    if not issuesubmission:
        return can_change_issue_submission
    return can_change_issue_submission &\
        rules.test_rules('erudit.can_access_journal', user, issuesubmission.journal)


@rules.predicate
def can_access_issuesubmission(user):
    return bool(Rule.objects.filter(
        user=user,
        permission='all:can_access_issuesubmission'
    ).count())


@rules.predicate
def can_add_issuesubmission(user):
    has_journal_access = bool(Rule.objects.filter(
        user=user,
        permission__in=('permissions.journal:can_access', 'permissions.journal:can_change'),
    ).count())
    can_manage_issuesubmission = bool(Rule.objects.filter(
        user=user,
        permission='all:can_add_issuesubmission'
    ).count())
    return has_journal_access & can_manage_issuesubmission

rules.add_perm('erudit.access_journal',
               is_superuser | is_staff & can_access_journal)
rules.add_perm('erudit.change_journal',
               is_superuser | is_staff & can_change_journal)
rules.add_perm('editor.change_issuesubmission',
               is_superuser | is_staff & can_change_issuesubmission)
rules.add_perm('editor.add_issuesubmission',
               is_superuser | is_staff & can_add_issuesubmission)
rules.add_perm('editor.access_issuesubmission',
               is_superuser | is_staff & can_access_issuesubmission)
