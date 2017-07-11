import unittest

import pypihole


class TestPyPiholeInternals(unittest.TestCase):
    def setUp(self):
        self.filter_test_string = 'Pihole blocks the ads, pypihole helps ' \
                                  'to analyze Pihole'

    def test__query_filter_no_filter(self):
        res = pypihole.pypihole._query_filter(self.filter_test_string)
        print(res)
        self.assertTrue(res)

    def test__query_filter_include(self):
        # one include, match
        res = pypihole.pypihole._query_filter(self.filter_test_string,
                                              include=[self.filter_test_string])
        self.assertTrue(res)

        # one include, not a match
        res = pypihole.pypihole._query_filter(self.filter_test_string,
                                              include=['not going to happen'])
        self.assertFalse(res)

        # two includes, first will hit
        res = pypihole.pypihole._query_filter(self.filter_test_string,
                                              include=[self.filter_test_string,
                                                       'pick me, pick me'])
        self.assertTrue(res)

    def test__query_filter_exclude(self):
        # exclude match
        res = pypihole.pypihole._query_filter(self.filter_test_string,
                                              exclude=[self.filter_test_string])
        self.assertFalse(res)

        # exclude doesn't match
        res = pypihole.pypihole._query_filter(self.filter_test_string,
                                              exclude=['something else'])
        self.assertTrue(res)

        # two excludes, second matches
        res = pypihole.pypihole._query_filter(self.filter_test_string,
                                              exclude=['something else',
                                                       self.filter_test_string])
        self.assertFalse(res)

    def test__query_filter_include_and_exclude(self):
        res = pypihole.pypihole._query_filter(self.filter_test_string,
                                              exclude=[self.filter_test_string])
        self.assertFalse(res)


class TestPyPihole(unittest.TestCase):
    def setUp(self):
        self.test_log = pypihole.parse_log('test.log')

    def test_parse_log(self):
        # TODO: Write better tests for this
        result = pypihole.parse_log('test.log')
        self.assertEqual(len(result), 5)

    def test_counts_query_unfiltered(self):
        counts = pypihole.counts_query(self.test_log)
        self.assertEqual(counts['unifi'], 2)
        self.assertEqual(counts['openvpn'], 2)
        self.assertEqual(counts['docs.google.com'], 1)

    def test_counts_query_include(self):
        counts = pypihole.counts_query(self.test_log, ['unifi'])
        self.assertEqual(counts['unifi'], 2)
        self.assertEqual(counts['openvpn'], 0)

    def test_counts_query_exclude(self):
        counts = pypihole.counts_query(self.test_log, exclude=['openvpn'])
        self.assertEqual(counts['unifi'], 2)
        self.assertEqual(counts['openvpn'], 0)
        self.assertEqual(counts['docs.google.com'], 1)

    def test_counts_query_include_and_exclude(self):
        counts = pypihole.counts_query(self.test_log,
                                       include=['unifi', 'docs.google.com'],
                                       exclude=['openvpn'])
        self.assertEqual(counts['unifi'], 2)
        self.assertEqual(counts['openvpn'], 0)
        self.assertEqual(counts['docs.google.com'], 1)

    def test_counts_client_unfiltered(self):
        counts = pypihole.counts_client(self.test_log)
        self.assertEqual(counts['192.168.1.11'], 2)
        self.assertEqual(counts['192.168.1.12'], 2)
        self.assertEqual(counts['192.168.1.13'], 1)

    def test_counts_client_include(self):
        counts = pypihole.counts_client(self.test_log, include=['192.168.1.11'])
        self.assertEqual(counts['192.168.1.11'], 2)
        self.assertEqual(counts['192.168.1.12'], 0)
        self.assertEqual(counts['192.168.1.13'], 0)

    def test_counts_client_exclude(self):
        counts = pypihole.counts_client(self.test_log, exclude=['192.168.1.11'])
        self.assertEqual(counts['192.168.1.11'], 0)
        self.assertEqual(counts['192.168.1.12'], 2)
        self.assertEqual(counts['192.168.1.13'], 1)

    def test_counts_client_include_and_exclude(self):
        counts = pypihole.counts_client(self.test_log, include=['192.168.1.11'],
                                        exclude=['192.168.1.12'])
        self.assertEqual(counts['192.168.1.11'], 2)
        self.assertEqual(counts['192.168.1.12'], 0)
        self.assertEqual(counts['192.168.1.13'], 0)
