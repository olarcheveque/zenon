from django.test import TestCase

from erudit.factories import JournalFactory, BasketFactory
from erudit.models import Journal

from ..factories import OrganizationPolicyFactory, IndividualAccountFactory
from ..models import IndividualAccountJournal


class OrganizationPolicyTestCase(TestCase):

    def test_total_accounts(self):
        policy = OrganizationPolicyFactory()
        IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        self.assertEqual(policy.total_accounts, 2)

    def test_date_activation(self):
        policy = OrganizationPolicyFactory()
        self.assertIsNone(policy.date_activation)

        IndividualAccountFactory(organization_policy=policy)
        self.assertIsNotNone(policy.date_activation)

        first_date_activation = policy.date_activation
        IndividualAccountFactory(organization_policy=policy)
        self.assertEqual(policy.date_activation, first_date_activation)


class IndividualAccountTestCase(TestCase):

    def test_crypt_password(self):
        password = '123qwe'
        salt = 'nawak'
        php_script_result = 'H8HdFUyxvh8/ZxQ5SuF9E0W3SZ5uYXdhaw=='
        account = IndividualAccountFactory()
        self.assertEqual(account.sha1(password, salt), php_script_result)

    def test_default_password(self):
        account = IndividualAccountFactory()
        self.assertIsNotNone(account.password)

    def test_update_password(self):
        password = '123qwe'
        account = IndividualAccountFactory()
        old_password = account.password
        account.password = password
        account.save()
        self.assertNotEqual(account.password, password)
        self.assertNotEqual(account.password, old_password)

    def test_no_update_password(self):
        account = IndividualAccountFactory()
        password = account.password
        account.save()
        self.assertEqual(account.password, password)


class IndividualAccountJournalTestCase(TestCase):

    def test_run_command_twice(self):
        policy = OrganizationPolicyFactory()
        IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        JournalFactory.create_batch(10)
        policy.access_full = True
        policy.save()
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 20)
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 20)

    def test_removed_account(self):
        policy = OrganizationPolicyFactory()
        dude_to_delete = IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        JournalFactory.create_batch(10)
        policy.access_full = True
        policy.save()
        policy.generate_flat_access()
        dude_to_delete.delete()
        self.assertEqual(IndividualAccountJournal.objects.count(), 10)

    def test_removed_journal(self):
        policy = OrganizationPolicyFactory()
        IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        JournalFactory.create_batch(10)
        policy.access_full = True
        policy.save()
        policy.generate_flat_access()
        Journal.objects.first().delete()
        self.assertEqual(IndividualAccountJournal.objects.count(), 18)


class IndividualAccountJournalFullAccessTestCase(TestCase):

    def test_add_full_access(self):
        policy = OrganizationPolicyFactory()
        IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        JournalFactory.create_batch(10)
        policy.access_full = True
        policy.save()
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 20)


class IndividualAccountJournalBasketTestCase(TestCase):

    def test_link_baskets(self):
        policy = OrganizationPolicyFactory()
        IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        basket1 = BasketFactory()
        basket1.journals = JournalFactory.create_batch(2)
        basket1.save()
        basket2 = BasketFactory()
        basket2.journals = JournalFactory.create_batch(3)
        basket2.save()
        policy.access_basket = [basket1, basket2, ]
        policy.save()
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 10)

    def test_remove_journal_from_baskets(self):
        policy = OrganizationPolicyFactory()
        IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        basket1 = BasketFactory()
        basket1.journals = JournalFactory.create_batch(2)
        basket1.save()
        basket2 = BasketFactory()
        basket2.journals = JournalFactory.create_batch(3)
        basket2.save()
        policy.access_basket = [basket1, basket2, ]
        policy.save()
        policy.generate_flat_access()
        basket1.journals = []
        basket1.save()
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 6)

    def test_remove_account(self):
        policy = OrganizationPolicyFactory()
        dude_to_delete = IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        basket1 = BasketFactory()
        basket1.journals = JournalFactory.create_batch(2)
        basket1.save()
        basket2 = BasketFactory()
        basket2.journals = JournalFactory.create_batch(3)
        basket2.save()
        policy.access_basket = [basket1, basket2, ]
        policy.save()
        policy.generate_flat_access()
        dude_to_delete.delete()
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 5)


class IndividualAccountJournalCustomTestCase(TestCase):

    def test_link_journals(self):
        policy = OrganizationPolicyFactory()
        policy.access_journal = JournalFactory.create_batch(2)
        policy.save()
        IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 4)

    def test_remove_account(self):
        policy = OrganizationPolicyFactory()
        policy.access_journal = JournalFactory.create_batch(2)
        policy.save()
        dude_to_delete = IndividualAccountFactory(organization_policy=policy)
        IndividualAccountFactory(organization_policy=policy)
        policy.generate_flat_access()
        dude_to_delete.delete()
        policy.generate_flat_access()
        self.assertEqual(IndividualAccountJournal.objects.count(), 2)