import unittest

import pypihole


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
        counts = pypihole.counts_query(self.test_log, include=['unifi'])
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
