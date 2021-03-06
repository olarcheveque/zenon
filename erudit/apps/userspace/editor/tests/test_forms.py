from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from core.permissions.models import Rule
from core.userspace.factories import UserFactory
from erudit.factories import JournalFactory

from ..forms import IssueSubmissionForm


class IssueSubmissionTestCase(TestCase):

    def authorize_user_on_journal(self, user, journal):
        ct = ContentType.objects.get(
            app_label="erudit", model="journal")
        Rule.objects.create(content_type=ct,
                            user=user,
                            object_id=journal.id,
                            permission="editor.manage_issuesubmission")

    def test_journal_filter(self):
        user = UserFactory()
        data = {'user': user}

        journal_in = JournalFactory()
        journal_in.members.add(user)
        journal_in.save()
        self.authorize_user_on_journal(user, journal_in)

        journal_not_in = JournalFactory()
        form = IssueSubmissionForm(**data)
        choices = [c[0] for c in form.fields['journal'].choices]
        self.assertTrue(journal_in.id in choices)
        self.assertFalse(journal_not_in.id in choices)

    def test_contact_filter(self):
        user = UserFactory()
        user2 = UserFactory()
        data = {'user': user}

        journal_in = JournalFactory()
        journal_in.members.add(user)
        journal_in.save()

        journal_not_in = JournalFactory()
        journal_not_in.members.add(user2)
        journal_not_in.save()

        form = IssueSubmissionForm(**data)
        choices = [c[0] for c in form.fields['contact'].choices]
        self.assertTrue(user.id in choices)
        self.assertFalse(user2.id in choices)

    def test_journal_contact_invalid(self):
        user = UserFactory()
        user2 = UserFactory()
        data = {'user': user}

        journal_in1 = JournalFactory()
        journal_in1.members.add(user)
        journal_in1.save()
        self.authorize_user_on_journal(user, journal_in1)

        journal_in2 = JournalFactory()
        journal_in2.members.add(user)
        journal_in2.members.add(user2)
        journal_in2.save()
        self.authorize_user_on_journal(user, journal_in2)

        form = IssueSubmissionForm(**data)
        choices = [c[0] for c in form.fields['contact'].choices]
        self.assertTrue(user.id in choices)
        self.assertTrue(user2.id in choices)

        data.update({'data': {
            'journal': journal_in1.id,
            'contact': user2.id,
            'year': '2016',
            'number': '123', }
        })
        form = IssueSubmissionForm(**data)
        self.assertFalse(form.is_valid())
