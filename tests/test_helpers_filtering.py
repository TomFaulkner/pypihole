import unittest

from pypihole.helpers.filtering import ie_filter


class Test_ie_filter(unittest.TestCase):
    def setUp(self):
        self.filter_test_string = 'Pihole blocks the ads, pypihole helps ' \
                                  'to analyze Pihole'

    def test_ie_filter_no_filter(self):
        res = ie_filter(self.filter_test_string)
        self.assertTrue(res)

    def test_ie_filter_include(self):
        # one include, match
        res = ie_filter(self.filter_test_string,
                                      include=[self.filter_test_string])
        self.assertTrue(res)

        # one include, not a match
        res = ie_filter(self.filter_test_string,
                                      include=['not going to happen'])
        self.assertFalse(res)

        # two includes, first will hit
        res = ie_filter(self.filter_test_string,
                                      include=[self.filter_test_string,
                                               'pick me, pick me'])
        self.assertTrue(res)

    def test_ie_filter_exclude(self):
        # exclude match
        res = ie_filter(self.filter_test_string,
                                      exclude=[self.filter_test_string])
        self.assertFalse(res)

        # exclude doesn't match
        res = ie_filter(self.filter_test_string,
                                      exclude=['something else'])
        self.assertTrue(res)

        # two excludes, second matches
        res = ie_filter(self.filter_test_string,
                                      exclude=['something else',
                                               self.filter_test_string])
        self.assertFalse(res)

    def test_ie_filter_include_and_exclude(self):
        res = ie_filter(self.filter_test_string,
                                      exclude=[self.filter_test_string])
        self.assertFalse(res)

    def test_ie_filter_include_regex(self):
        res = ie_filter(
            self.filter_test_string,
            include_regex=[r'hole'])
        self.assertTrue(res)

        # two matches
        res = ie_filter(
            self.filter_test_string,
            include_regex=[r'hole', 'blocks'])
        self.assertTrue(res)

        # what happens if first string isn't a match?
        res = ie_filter(
            self.filter_test_string,
            include_regex=['nah bro', 'hole', 'blocks'])
        self.assertTrue(res)

    def test_ie_filter_exclude_regex(self):
        res = ie_filter(
            self.filter_test_string,
            exclude_regex=[r'hole'])
        self.assertFalse(res)

        # two matches
        res = ie_filter(
            self.filter_test_string,
            exclude_regex=[r'hole', 'blocks'])
        self.assertFalse(res)

        # what happens if first string isn't a match?
        res = ie_filter(
            self.filter_test_string,
            exclude_regex=['nah bro', 'hole', 'blocks'])
        self.assertFalse(res)

    def test_ie_filter_include_regex_and_exclude_regex(self):
        res = ie_filter(
            self.filter_test_string,
            include_regex=['hole'],
            exclude_regex=['pi'])
        self.assertFalse(res)

        # two matches
        res = ie_filter(
            self.filter_test_string,
            include_regex=['hole'],
            exclude_regex=['pi', 'blocks'])
        self.assertFalse(res)

        # what happens if first string isn't a match?
        res = ie_filter(
            self.filter_test_string,
            include_regex=['pi'],
            exclude_regex=['nah bro', 'hole', 'blocks'])
        self.assertFalse(res)

    def test_ie_filter_include_and_include_regex(self):
        res = ie_filter(
            self.filter_test_string,
            include=self.filter_test_string,
            include_regex=['hole'])
        self.assertTrue(res)

    def test_ie_filter_include_and_exclude_regex(self):
        res = ie_filter(
            self.filter_test_string,
            include=self.filter_test_string,
            exclude_regex=['hole'])
        self.assertFalse(res)

        res = ie_filter(
            self.filter_test_string,
            include=self.filter_test_string,
            exclude_regex=['nah bro'])
        self.assertTrue(res)

    def test_ie_filter_exclude_and_include_regex(self):
        res = ie_filter(
            self.filter_test_string,
            exclude=self.filter_test_string,
            include_regex=['hole'])
        self.assertFalse(res)

        res = ie_filter(
            self.filter_test_string,
            exclude='google.com',
            include_regex=['hole'])
        self.assertTrue(res)
