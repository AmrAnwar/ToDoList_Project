from .test_main import TestMain


class TestUnicode(TestMain):
    def setUp(self):
        super(TestUnicode, self).setUp()
        self.client.login(username='tester', password='password')

    def test_unicode(self):
        self.assertEqual(unicode(self.list), "list List TEST")
        self.assertEqual(unicode(self.task), "task Task TEST")
        self.assertEqual(unicode(self.sublist), "sublist SubList TEST")
        self.assertEqual(unicode(self.user.userprofile), "tester")