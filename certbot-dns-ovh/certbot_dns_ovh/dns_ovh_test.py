"""Tests for certbot_dns_ovh.dns_ovh."""

import os
import unittest

import mock
from requests.exceptions import HTTPError

from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.tests import util as test_util

ENDPOINT = 'ovh-eu'
APPLICATION_KEY = 'foo'
APPLICATION_SECRET = 'bar'
CONSUMER_KEY = 'spam'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconAuthenticatorTest):

    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_ovh.dns_ovh import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        credentials = {
            "ovh_endpoint": ENDPOINT,
            "ovh_application_key": APPLICATION_KEY,
            "ovh_application_secret": APPLICATION_SECRET,
            "ovh_consumer_key": CONSUMER_KEY,
        }
        dns_test_common.write(credentials, path)

        self.configure(Authenticator(self.config, "ovh"), {"credentials": path})

        self.mock_client = mock.MagicMock()
        # _get_ovh_client | pylint: disable=protected-access
        self.auth._get_ovh_client = mock.MagicMock(return_value=self.mock_client)


class OVHLexiconClientTest(unittest.TestCase, dns_test_common_lexicon.BaseLexiconClientTest):

    def domain_not_found(self, domain):
        return Exception('Domain {0} not found'.format(domain))

    def login_error(self, domain):
        return HTTPError('403 Client Error: Forbidden for url: https://eu.api.ovh.com/1.0/...')

    def setUp(self):
        from certbot_dns_ovh.dns_ovh import _OVHLexiconClient

        self.client = _OVHLexiconClient(
            ENDPOINT, APPLICATION_KEY, APPLICATION_SECRET, CONSUMER_KEY, 0
        )

        self.provider_mock = mock.MagicMock()
        self.client.provider = self.provider_mock


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
