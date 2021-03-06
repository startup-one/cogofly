# -*- coding: utf-8 -*-
from openid import message
from openid import oidutil
from openid.extensions import sreg

import urllib.request
import urllib.parse
import urllib.error
import unittest


def mkGetArgTest(ns, key, expected=None):
    def test(self):
        a_default = object()
        self.assertEqual(self.msg.getArg(ns, key), expected)
        if expected is None:
            self.assertEqual(self.msg.getArg(ns, key, a_default), a_default)
            self.assertRaises(KeyError, self.msg.getArg, ns, key,
                              message.no_default)
        else:
            self.assertEqual(self.msg.getArg(ns, key, a_default), expected)
            self.assertEqual(
                self.msg.getArg(ns, key, message.no_default), expected)

    return test


class EmptyMessageTest(unittest.TestCase):
    def setUp(self):
        self.msg = message.Message()

    def test_toPostArgs(self):
        self.assertEqual(self.msg.toPostArgs(), {})

    def test_toArgs(self):
        self.assertEqual(self.msg.toArgs(), {})

    def test_toKVForm(self):
        self.assertEqual(self.msg.toKVForm(), b'')

    def test_toURLEncoded(self):
        self.assertEqual(self.msg.toURLEncoded(), '')

    def test_toURL(self):
        base_url = 'http://base.url/'
        self.assertEqual(self.msg.toURL(base_url), base_url)

    def test_getOpenID(self):
        self.assertEqual(self.msg.getOpenIDNamespace(), None)

    def test_getKeyOpenID(self):
        # Could reasonably return None instead of raising an
        # exception. I'm not sure which one is more right, since this
        # case should only happen when you're building a message from
        # scratch and so have no default namespace.
        self.assertRaises(message.UndefinedOpenIDNamespace, self.msg.getKey,
                          message.OPENID_NS, 'foo')

    def test_getKeyBARE(self):
        self.assertEqual(self.msg.getKey(message.BARE_NS, 'foo'), 'foo')

    def test_getKeyNS1(self):
        self.assertEqual(self.msg.getKey(message.OPENID1_NS, 'foo'), None)

    def test_getKeyNS2(self):
        self.assertEqual(self.msg.getKey(message.OPENID2_NS, 'foo'), None)

    def test_getKeyNS3(self):
        self.assertEqual(
            self.msg.getKey('urn:nothing-significant', 'foo'), None)

    def test_hasKey(self):
        # Could reasonably return False instead of raising an
        # exception. I'm not sure which one is more right, since this
        # case should only happen when you're building a message from
        # scratch and so have no default namespace.
        self.assertRaises(message.UndefinedOpenIDNamespace, self.msg.hasKey,
                          message.OPENID_NS, 'foo')

    def test_hasKeyBARE(self):
        self.assertEqual(self.msg.hasKey(message.BARE_NS, 'foo'), False)

    def test_hasKeyNS1(self):
        self.assertEqual(self.msg.hasKey(message.OPENID1_NS, 'foo'), False)

    def test_hasKeyNS2(self):
        self.assertEqual(self.msg.hasKey(message.OPENID2_NS, 'foo'), False)

    def test_hasKeyNS3(self):
        self.assertEqual(
            self.msg.hasKey('urn:nothing-significant', 'foo'), False)

    def test_getAliasedArgSuccess(self):
        msg = message.Message.fromPostArgs({
            'openid.ns.test': 'urn://foo',
            'openid.test.flub': 'bogus'
        })
        actual_uri = msg.getAliasedArg('ns.test', message.no_default)
        self.assertEqual("urn://foo", actual_uri)

    def test_getAliasedArgFailure(self):
        msg = message.Message.fromPostArgs({'openid.test.flub': 'bogus'})
        self.assertRaises(KeyError, msg.getAliasedArg, 'ns.test',
                          message.no_default)

    def test_getArg(self):
        # Could reasonably return None instead of raising an
        # exception. I'm not sure which one is more right, since this
        # case should only happen when you're building a message from
        # scratch and so have no default namespace.
        self.assertRaises(message.UndefinedOpenIDNamespace, self.msg.getArg,
                          message.OPENID_NS, 'foo')

    test_getArgBARE = mkGetArgTest(message.BARE_NS, 'foo')
    test_getArgNS1 = mkGetArgTest(message.OPENID1_NS, 'foo')
    test_getArgNS2 = mkGetArgTest(message.OPENID2_NS, 'foo')
    test_getArgNS3 = mkGetArgTest('urn:nothing-significant', 'foo')

    def test_getArgs(self):
        # Could reasonably return {} instead of raising an
        # exception. I'm not sure which one is more right, since this
        # case should only happen when you're building a message from
        # scratch and so have no default namespace.
        self.assertRaises(message.UndefinedOpenIDNamespace, self.msg.getArgs,
                          message.OPENID_NS)

    def test_getArgsBARE(self):
        self.assertEqual(self.msg.getArgs(message.BARE_NS), {})

    def test_getArgsNS1(self):
        self.assertEqual(self.msg.getArgs(message.OPENID1_NS), {})

    def test_getArgsNS2(self):
        self.assertEqual(self.msg.getArgs(message.OPENID2_NS), {})

    def test_getArgsNS3(self):
        self.assertEqual(self.msg.getArgs('urn:nothing-significant'), {})

    def test_updateArgs(self):
        self.assertRaises(message.UndefinedOpenIDNamespace,
                          self.msg.updateArgs, message.OPENID_NS,
                          {'does not': 'matter'})

    def _test_updateArgsNS(self, ns):
        update_args = {
            'Camper van Beethoven': 'David Lowery',
            'Magnolia Electric Co.': 'Jason Molina',
        }

        self.assertEqual(self.msg.getArgs(ns), {})
        self.msg.updateArgs(ns, update_args)
        self.assertEqual(self.msg.getArgs(ns), update_args)

    def test_updateArgsBARE(self):
        self._test_updateArgsNS(message.BARE_NS)

    def test_updateArgsNS1(self):
        self._test_updateArgsNS(message.OPENID1_NS)

    def test_updateArgsNS2(self):
        self._test_updateArgsNS(message.OPENID2_NS)

    def test_updateArgsNS3(self):
        self._test_updateArgsNS('urn:nothing-significant')

    def test_setArg(self):
        self.assertRaises(message.UndefinedOpenIDNamespace, self.msg.setArg,
                          message.OPENID_NS, 'does not', 'matter')

    def _test_setArgNS(self, ns):
        key = 'Camper van Beethoven'
        value = 'David Lowery'
        self.assertEqual(self.msg.getArg(ns, key), None)
        self.msg.setArg(ns, key, value)
        self.assertEqual(self.msg.getArg(ns, key), value)

    def test_setArgBARE(self):
        self._test_setArgNS(message.BARE_NS)

    def test_setArgNS1(self):
        self._test_setArgNS(message.OPENID1_NS)

    def test_setArgNS2(self):
        self._test_setArgNS(message.OPENID2_NS)

    def test_setArgNS3(self):
        self._test_setArgNS('urn:nothing-significant')

    def test_setArgToNone(self):
        self.assertRaises(AssertionError, self.msg.setArg, message.OPENID1_NS,
                          'op_endpoint', None)

    def test_delArg(self):
        # Could reasonably raise KeyError instead of raising
        # UndefinedOpenIDNamespace. I'm not sure which one is more
        # right, since this case should only happen when you're
        # building a message from scratch and so have no default
        # namespace.
        self.assertRaises(message.UndefinedOpenIDNamespace, self.msg.delArg,
                          message.OPENID_NS, 'key')

    def _test_delArgNS(self, ns):
        key = 'Camper van Beethoven'
        self.assertRaises(KeyError, self.msg.delArg, ns, key)

    def test_delArgBARE(self):
        self._test_delArgNS(message.BARE_NS)

    def test_delArgNS1(self):
        self._test_delArgNS(message.OPENID1_NS)

    def test_delArgNS2(self):
        self._test_delArgNS(message.OPENID2_NS)

    def test_delArgNS3(self):
        self._test_delArgNS('urn:nothing-significant')

    def test_isOpenID1(self):
        self.assertFalse(self.msg.isOpenID1())

    def test_isOpenID2(self):
        self.assertFalse(self.msg.isOpenID2())


class OpenID1MessageTest(unittest.TestCase):
    def setUp(self):
        self.msg = message.Message.fromPostArgs({
            'openid.mode': 'error',
            'openid.error': 'unit test'
        })

    def test_toPostArgs(self):
        self.assertEqual(self.msg.toPostArgs(),
                         {'openid.mode': 'error',
                          'openid.error': 'unit test'})

    def test_toArgs(self):
        self.assertEqual(self.msg.toArgs(),
                         {'mode': 'error',
                          'error': 'unit test'})

    def test_toKVForm(self):
        self.assertEqual(self.msg.toKVForm(), b'error:unit test\nmode:error\n')

    def test_toURLEncoded(self):
        self.assertEqual(self.msg.toURLEncoded(),
                         'openid.error=unit+test&openid.mode=error')

    def test_toURL(self):
        base_url = 'http://base.url/'
        actual = self.msg.toURL(base_url)
        actual_base = actual[:len(base_url)]
        self.assertEqual(actual_base, base_url)
        self.assertEqual(actual[len(base_url)], '?')
        query = actual[len(base_url) + 1:]
        parsed = urllib.parse.parse_qs(query)
        self.assertEqual(
            parsed, {'openid.mode': ['error'],
                     'openid.error': ['unit test']})

    def test_getOpenID(self):
        self.assertEqual(self.msg.getOpenIDNamespace(), message.OPENID1_NS)

    def test_getKeyOpenID(self):
        self.assertEqual(
            self.msg.getKey(message.OPENID_NS, 'mode'), 'openid.mode')

    def test_getKeyBARE(self):
        self.assertEqual(self.msg.getKey(message.BARE_NS, 'mode'), 'mode')

    def test_getKeyNS1(self):
        self.assertEqual(
            self.msg.getKey(message.OPENID1_NS, 'mode'), 'openid.mode')

    def test_getKeyNS2(self):
        self.assertEqual(self.msg.getKey(message.OPENID2_NS, 'mode'), None)

    def test_getKeyNS3(self):
        self.assertEqual(
            self.msg.getKey('urn:nothing-significant', 'mode'), None)

    def test_hasKey(self):
        self.assertEqual(self.msg.hasKey(message.OPENID_NS, 'mode'), True)

    def test_hasKeyBARE(self):
        self.assertEqual(self.msg.hasKey(message.BARE_NS, 'mode'), False)

    def test_hasKeyNS1(self):
        self.assertEqual(self.msg.hasKey(message.OPENID1_NS, 'mode'), True)

    def test_hasKeyNS2(self):
        self.assertEqual(self.msg.hasKey(message.OPENID2_NS, 'mode'), False)

    def test_hasKeyNS3(self):
        self.assertEqual(
            self.msg.hasKey('urn:nothing-significant', 'mode'), False)

    test_getArgNSBARE = mkGetArgTest(message.BARE_NS, 'mode')
    test_getArgNS = mkGetArgTest(message.OPENID_NS, 'mode', 'error')
    test_getArgNS1 = mkGetArgTest(message.OPENID1_NS, 'mode', 'error')
    test_getArgNS2 = mkGetArgTest(message.OPENID2_NS, 'mode')
    test_getArgNS3 = mkGetArgTest('urn:nothing-significant', 'mode')

    def test_getArgs(self):
        self.assertEqual(
            self.msg.getArgs(message.OPENID_NS), {
                'mode': 'error',
                'error': 'unit test',
            })

    def test_getArgsBARE(self):
        self.assertEqual(self.msg.getArgs(message.BARE_NS), {})

    def test_getArgsNS1(self):
        self.assertEqual(
            self.msg.getArgs(message.OPENID1_NS), {
                'mode': 'error',
                'error': 'unit test',
            })

    def test_getArgsNS2(self):
        self.assertEqual(self.msg.getArgs(message.OPENID2_NS), {})

    def test_getArgsNS3(self):
        self.assertEqual(self.msg.getArgs('urn:nothing-significant'), {})

    def _test_updateArgsNS(self, ns, before=None):
        if before is None:
            before = {}
        update_args = {
            'Camper van Beethoven': 'David Lowery',
            'Magnolia Electric Co.': 'Jason Molina',
        }

        self.assertEqual(self.msg.getArgs(ns), before)
        self.msg.updateArgs(ns, update_args)
        after = dict(before)
        after.update(update_args)
        self.assertEqual(self.msg.getArgs(ns), after)

    def test_updateArgs(self):
        self._test_updateArgsNS(
            message.OPENID_NS, before={'mode': 'error',
                                       'error': 'unit test'})

    def test_updateArgsBARE(self):
        self._test_updateArgsNS(message.BARE_NS)

    def test_updateArgsNS1(self):
        self._test_updateArgsNS(
            message.OPENID1_NS, before={'mode': 'error',
                                        'error': 'unit test'})

    def test_updateArgsNS2(self):
        self._test_updateArgsNS(message.OPENID2_NS)

    def test_updateArgsNS3(self):
        self._test_updateArgsNS('urn:nothing-significant')

    def _test_setArgNS(self, ns):
        key = 'Camper van Beethoven'
        value = 'David Lowery'
        self.assertEqual(self.msg.getArg(ns, key), None)
        self.msg.setArg(ns, key, value)
        self.assertEqual(self.msg.getArg(ns, key), value)

    def test_setArg(self):
        self._test_setArgNS(message.OPENID_NS)

    def test_setArgBARE(self):
        self._test_setArgNS(message.BARE_NS)

    def test_setArgNS1(self):
        self._test_setArgNS(message.OPENID1_NS)

    def test_setArgNS2(self):
        self._test_setArgNS(message.OPENID2_NS)

    def test_setArgNS3(self):
        self._test_setArgNS('urn:nothing-significant')

    def _test_delArgNS(self, ns):
        key = 'Camper van Beethoven'
        value = 'David Lowery'

        self.assertRaises(KeyError, self.msg.delArg, ns, key)
        self.msg.setArg(ns, key, value)
        self.assertEqual(self.msg.getArg(ns, key), value)
        self.msg.delArg(ns, key)
        self.assertEqual(self.msg.getArg(ns, key), None)

    def test_delArg(self):
        self._test_delArgNS(message.OPENID_NS)

    def test_delArgBARE(self):
        self._test_delArgNS(message.BARE_NS)

    def test_delArgNS1(self):
        self._test_delArgNS(message.OPENID1_NS)

    def test_delArgNS2(self):
        self._test_delArgNS(message.OPENID2_NS)

    def test_delArgNS3(self):
        self._test_delArgNS('urn:nothing-significant')

    def test_isOpenID1(self):
        self.assertTrue(self.msg.isOpenID1())

    def test_isOpenID2(self):
        self.assertFalse(self.msg.isOpenID2())


class OpenID1ExplicitMessageTest(unittest.TestCase):
    def setUp(self):
        self.msg = message.Message.fromPostArgs({
            'openid.mode': 'error',
            'openid.error': 'unit test',
            'openid.ns': message.OPENID1_NS
        })

    def test_toPostArgs(self):
        self.assertEqual(self.msg.toPostArgs(), {
            'openid.mode': 'error',
            'openid.error': 'unit test',
            'openid.ns': message.OPENID1_NS,
        })

    def test_toArgs(self):
        self.assertEqual(self.msg.toArgs(), {
            'mode': 'error',
            'error': 'unit test',
            'ns': message.OPENID1_NS,
        })

    def test_toKVForm(self):
        self.assertEqual(self.msg.toKVForm(),
                         bytes(
                             'error:unit test\nmode:error\nns:%s\n' %
                             message.OPENID1_NS,
                             encoding="utf-8"))

    def test_toURLEncoded(self):
        self.assertEqual(
            self.msg.toURLEncoded(),
            'openid.error=unit+test&openid.mode=error&openid.ns=http%3A%2F%2Fopenid.net%2Fsignon%2F1.0'
        )

    def test_toURL(self):
        base_url = 'http://base.url/'
        actual = self.msg.toURL(base_url)
        actual_base = actual[:len(base_url)]
        self.assertEqual(actual_base, base_url)
        self.assertEqual(actual[len(base_url)], '?')
        query = actual[len(base_url) + 1:]
        parsed = urllib.parse.parse_qs(query)
        self.assertEqual(parsed, {
            'openid.mode': ['error'],
            'openid.error': ['unit test'],
            'openid.ns': [message.OPENID1_NS]
        })

    def test_isOpenID1(self):
        self.assertTrue(self.msg.isOpenID1())


class OpenID2MessageTest(unittest.TestCase):
    def setUp(self):
        self.msg = message.Message.fromPostArgs({
            'openid.mode': 'error',
            'openid.error': 'unit test',
            'openid.ns': message.OPENID2_NS
        })
        self.msg.setArg(message.BARE_NS, "xey", "value")

    def test_toPostArgs(self):
        self.assertEqual(self.msg.toPostArgs(), {
            'openid.mode': 'error',
            'openid.error': 'unit test',
            'openid.ns': message.OPENID2_NS,
            'xey': 'value',
        })

    def test_toPostArgs_bug_with_utf8_encoded_values(self):
        msg = message.Message.fromPostArgs({
            'openid.mode': 'error',
            'openid.error': 'unit test',
            'openid.ns': message.OPENID2_NS
        })
        msg.setArg(message.BARE_NS, 'ünicöde_key', 'ünicöde_välüe')
        self.assertEqual(msg.toPostArgs(), {
            'openid.mode': 'error',
            'openid.error': 'unit test',
            'openid.ns': message.OPENID2_NS,
            'ünicöde_key': 'ünicöde_välüe',
        })

    def test_toArgs(self):
        # This method can't tolerate BARE_NS.
        self.msg.delArg(message.BARE_NS, "xey")
        self.assertEqual(self.msg.toArgs(), {
            'mode': 'error',
            'error': 'unit test',
            'ns': message.OPENID2_NS,
        })

    def test_toKVForm(self):
        # Can't tolerate BARE_NS in kvform
        self.msg.delArg(message.BARE_NS, "xey")
        self.assertEqual(self.msg.toKVForm(),
                         bytes(
                             'error:unit test\nmode:error\nns:%s\n' %
                             message.OPENID2_NS,
                             encoding="utf-8"))

    def _test_urlencoded(self, s):
        expected = ('openid.error=unit+test&openid.mode=error&'
                    'openid.ns=%s&xey=value' %
                    (urllib.parse.quote(message.OPENID2_NS, ''), ))
        self.assertEqual(s, expected)

    def test_toURLEncoded(self):
        self._test_urlencoded(self.msg.toURLEncoded())

    def test_toURL(self):
        base_url = 'http://base.url/'
        actual = self.msg.toURL(base_url)
        actual_base = actual[:len(base_url)]
        self.assertEqual(actual_base, base_url)
        self.assertEqual(actual[len(base_url)], '?')
        query = actual[len(base_url) + 1:]
        self._test_urlencoded(query)

    def test_getOpenID(self):
        self.assertEqual(self.msg.getOpenIDNamespace(), message.OPENID2_NS)

    def test_getKeyOpenID(self):
        self.assertEqual(
            self.msg.getKey(message.OPENID_NS, 'mode'), 'openid.mode')

    def test_getKeyBARE(self):
        self.assertEqual(self.msg.getKey(message.BARE_NS, 'mode'), 'mode')

    def test_getKeyNS1(self):
        self.assertEqual(self.msg.getKey(message.OPENID1_NS, 'mode'), None)

    def test_getKeyNS2(self):
        self.assertEqual(
            self.msg.getKey(message.OPENID2_NS, 'mode'), 'openid.mode')

    def test_getKeyNS3(self):
        self.assertEqual(
            self.msg.getKey('urn:nothing-significant', 'mode'), None)

    def test_hasKeyOpenID(self):
        self.assertEqual(self.msg.hasKey(message.OPENID_NS, 'mode'), True)

    def test_hasKeyBARE(self):
        self.assertEqual(self.msg.hasKey(message.BARE_NS, 'mode'), False)

    def test_hasKeyNS1(self):
        self.assertEqual(self.msg.hasKey(message.OPENID1_NS, 'mode'), False)

    def test_hasKeyNS2(self):
        self.assertEqual(self.msg.hasKey(message.OPENID2_NS, 'mode'), True)

    def test_hasKeyNS3(self):
        self.assertEqual(
            self.msg.hasKey('urn:nothing-significant', 'mode'), False)

    test_getArgBARE = mkGetArgTest(message.BARE_NS, 'mode')
    test_getArgNS = mkGetArgTest(message.OPENID_NS, 'mode', 'error')
    test_getArgNS1 = mkGetArgTest(message.OPENID1_NS, 'mode')
    test_getArgNS2 = mkGetArgTest(message.OPENID2_NS, 'mode', 'error')
    test_getArgNS3 = mkGetArgTest('urn:nothing-significant', 'mode')

    def test_getArgsOpenID(self):
        self.assertEqual(
            self.msg.getArgs(message.OPENID_NS), {
                'mode': 'error',
                'error': 'unit test',
            })

    def test_getArgsBARE(self):
        self.assertEqual(self.msg.getArgs(message.BARE_NS), {'xey': 'value'})

    def test_getArgsNS1(self):
        self.assertEqual(self.msg.getArgs(message.OPENID1_NS), {})

    def test_getArgsNS2(self):
        self.assertEqual(
            self.msg.getArgs(message.OPENID2_NS), {
                'mode': 'error',
                'error': 'unit test',
            })

    def test_getArgsNS3(self):
        self.assertEqual(self.msg.getArgs('urn:nothing-significant'), {})

    def _test_updateArgsNS(self, ns, before=None):
        if before is None:
            before = {}
        update_args = {
            'Camper van Beethoven': 'David Lowery',
            'Magnolia Electric Co.': 'Jason Molina',
        }

        self.assertEqual(self.msg.getArgs(ns), before)
        self.msg.updateArgs(ns, update_args)
        after = dict(before)
        after.update(update_args)
        self.assertEqual(self.msg.getArgs(ns), after)

    def test_updateArgsOpenID(self):
        self._test_updateArgsNS(
            message.OPENID_NS, before={'mode': 'error',
                                       'error': 'unit test'})

    def test_updateArgsBARE(self):
        self._test_updateArgsNS(message.BARE_NS, before={'xey': 'value'})

    def test_updateArgsNS1(self):
        self._test_updateArgsNS(message.OPENID1_NS)

    def test_updateArgsNS2(self):
        self._test_updateArgsNS(
            message.OPENID2_NS, before={'mode': 'error',
                                        'error': 'unit test'})

    def test_updateArgsNS3(self):
        self._test_updateArgsNS('urn:nothing-significant')

    def _test_setArgNS(self, ns):
        key = 'Camper van Beethoven'
        value = 'David Lowery'
        self.assertEqual(self.msg.getArg(ns, key), None)
        self.msg.setArg(ns, key, value)
        self.assertEqual(self.msg.getArg(ns, key), value)

    def test_setArgOpenID(self):
        self._test_setArgNS(message.OPENID_NS)

    def test_setArgBARE(self):
        self._test_setArgNS(message.BARE_NS)

    def test_setArgNS1(self):
        self._test_setArgNS(message.OPENID1_NS)

    def test_setArgNS2(self):
        self._test_setArgNS(message.OPENID2_NS)

    def test_setArgNS3(self):
        self._test_setArgNS('urn:nothing-significant')

    def test_badAlias(self):
        """Make sure dotted aliases and OpenID protocol fields are not
        allowed as namespace aliases."""

        for f in message.OPENID_PROTOCOL_FIELDS + ['dotted.alias']:
            args = {'openid.ns.%s' % f: 'blah', 'openid.%s.foo' % f: 'test'}

            # .fromPostArgs covers .fromPostArgs, .fromOpenIDArgs,
            # ._fromOpenIDArgs, and .fromOpenIDArgs (since it calls
            # .fromPostArgs).
            self.assertRaises(AssertionError, self.msg.fromPostArgs, args)

    def test_mysterious_missing_namespace_bug(self):
        """A failing test for bug #112"""
        openid_args = {
            'assoc_handle':
            '{{HMAC-SHA256}{1211477242.29743}{v5cadg==}',
            'claimed_id':
            'http://nerdbank.org/OPAffirmative/AffirmativeIdentityWithSregNoAssoc.aspx',
            'ns.sreg':
            'http://openid.net/extensions/sreg/1.1',
            'response_nonce':
            '2008-05-22T17:27:22ZUoW5.\\NV',
            'signed':
            'return_to,identity,claimed_id,op_endpoint,response_nonce,ns.sreg,sreg.email,sreg.nickname,assoc_handle',
            'sig':
            'e3eGZ10+TNRZitgq5kQlk5KmTKzFaCRI8OrRoXyoFa4=',
            'mode':
            'check_authentication',
            'op_endpoint':
            'http://nerdbank.org/OPAffirmative/ProviderNoAssoc.aspx',
            'sreg.nickname':
            'Andy',
            'return_to':
            'http://localhost.localdomain:8001/process?janrain_nonce=2008-05-22T17%3A27%3A21ZnxHULd',
            'invalidate_handle':
            '{{HMAC-SHA1}{1211477241.92242}{H0akXw==}',
            'identity':
            'http://nerdbank.org/OPAffirmative/AffirmativeIdentityWithSregNoAssoc.aspx',
            'sreg.email':
            'a@b.com'
        }
        m = message.Message.fromOpenIDArgs(openid_args)

        self.assertTrue(('http://openid.net/extensions/sreg/1.1',
                         'sreg') in list(m.namespaces.items()))
        missing = []
        if isinstance(openid_args['signed'], bytes):
            oid_args_signed = openid_args['signed'].decode("utf-8")
        else:
            oid_args_signed = openid_args['signed']
        for k in oid_args_signed.split(','):
            if ("openid." + k) not in m.toPostArgs():
                missing.append(k)
        self.assertEqual([], missing, missing)
        self.assertEqual(openid_args, m.toArgs())
        self.assertTrue(m.isOpenID1())

    def test_112B(self):
        args = {
            'openid.assoc_handle':
            'fa1f5ff0-cde4-11dc-a183-3714bfd55ca8',
            'openid.claimed_id':
            'http://binkley.lan/user/test01',
            'openid.identity':
            'http://test01.binkley.lan/',
            'openid.mode':
            'id_res',
            'openid.ns':
            'http://specs.openid.net/auth/2.0',
            'openid.ns.pape':
            'http://specs.openid.net/extensions/pape/1.0',
            'openid.op_endpoint':
            'http://binkley.lan/server',
            'openid.pape.auth_policies':
            'none',
            'openid.pape.auth_time':
            '2008-01-28T20:42:36Z',
            'openid.pape.nist_auth_level':
            '0',
            'openid.response_nonce':
            '2008-01-28T21:07:04Z99Q=',
            'openid.return_to':
            'http://binkley.lan:8001/process?janrain_nonce=2008-01-28T21%3A07%3A02Z0tMIKx',
            'openid.sig':
            'YJlWH4U6SroB1HoPkmEKx9AyGGg=',
            'openid.signed':
            'assoc_handle,identity,response_nonce,return_to,claimed_id,op_endpoint,pape.auth_time,ns.pape,pape.nist_auth_level,pape.auth_policies'
        }
        m = message.Message.fromPostArgs(args)
        missing = []
        if isinstance(args['openid.signed'], bytes):
            oid_args_signed = args['openid.signed'].decode("utf-8")
        else:
            oid_args_signed = args['openid.signed']
        for k in oid_args_signed.split(','):
            if ("openid." + k) not in m.toPostArgs():
                missing.append(k)
        self.assertEqual([], missing, missing)
        self.assertEqual(args, m.toPostArgs())
        self.assertTrue(m.isOpenID2())

    def test_implicit_sreg_ns(self):
        openid_args = {'sreg.email': 'a@b.com'}
        m = message.Message.fromOpenIDArgs(openid_args)
        self.assertTrue((sreg.ns_uri, 'sreg') in list(m.namespaces.items()))
        self.assertEqual('a@b.com', m.getArg(sreg.ns_uri, 'email'))
        self.assertEqual(openid_args, m.toArgs())
        self.assertTrue(m.isOpenID1())

    def _test_delArgNS(self, ns):
        key = 'Camper van Beethoven'
        value = 'David Lowery'

        self.assertRaises(KeyError, self.msg.delArg, ns, key)
        self.msg.setArg(ns, key, value)
        self.assertEqual(self.msg.getArg(ns, key), value)
        self.msg.delArg(ns, key)
        self.assertEqual(self.msg.getArg(ns, key), None)

    def test_delArgOpenID(self):
        self._test_delArgNS(message.OPENID_NS)

    def test_delArgBARE(self):
        self._test_delArgNS(message.BARE_NS)

    def test_delArgNS1(self):
        self._test_delArgNS(message.OPENID1_NS)

    def test_delArgNS2(self):
        self._test_delArgNS(message.OPENID2_NS)

    def test_delArgNS3(self):
        self._test_delArgNS('urn:nothing-significant')

    def test_overwriteExtensionArg(self):
        ns = 'urn:unittest_extension'
        key = 'mykey'
        value_1 = 'value_1'
        value_2 = 'value_2'

        self.msg.setArg(ns, key, value_1)
        self.assertTrue(self.msg.getArg(ns, key) == value_1)
        self.msg.setArg(ns, key, value_2)
        self.assertTrue(self.msg.getArg(ns, key) == value_2)

    def test_argList(self):
        self.assertRaises(TypeError, self.msg.fromPostArgs, {'arg': [1, 2, 3]})

    def test_isOpenID1(self):
        self.assertFalse(self.msg.isOpenID1())

    def test_isOpenID2(self):
        self.assertTrue(self.msg.isOpenID2())


class MessageTest(unittest.TestCase):
    def setUp(self):
        self.postargs = {
            'openid.ns': message.OPENID2_NS,
            'openid.mode': 'checkid_setup',
            'openid.identity': 'http://bogus.example.invalid:port/',
            'openid.assoc_handle': 'FLUB',
            'openid.return_to': 'Neverland',
        }

        self.action_url = 'scheme://host:port/path?query'

        self.form_tag_attrs = {
            'company': 'janrain',
            'class': 'fancyCSS',
        }

        self.submit_text = 'GO!'

        ### Expected data regardless of input

        self.required_form_attrs = {
            'accept-charset': 'UTF-8',
            'enctype': 'application/x-www-form-urlencoded',
            'method': 'post',
        }

    def _checkForm(self, html, message_, action_url, form_tag_attrs,
                   submit_text):
        E = oidutil.importElementTree()

        # Build element tree from HTML source
        input_tree = E.ElementTree(E.fromstring(html))

        # Get root element
        form = input_tree.getroot()

        # Check required form attributes
        for k, v in list(self.required_form_attrs.items()):
            assert form.attrib[k] == v, \
                   "Expected '%s' for required form attribute '%s', got '%s'" % \
                   (v, k, form.attrib[k])

        # Check extra form attributes
        for k, v in list(form_tag_attrs.items()):

            # Skip attributes that already passed the required
            # attribute check, since they should be ignored by the
            # form generation code.
            if k in self.required_form_attrs:
                continue

            assert form.attrib[k] == v, \
                   "Form attribute '%s' should be '%s', found '%s'" % \
                   (k, v, form.attrib[k])

        # Check hidden fields against post args
        hiddens = [e for e in form \
                   if e.tag.upper() == 'INPUT' and \
                   e.attrib['type'].upper() == 'HIDDEN']

        # For each post arg, make sure there is a hidden with that
        # value.  Make sure there are no other hiddens.
        for name, value in list(message_.toPostArgs().items()):
            for e in hiddens:
                if e.attrib['name'] == name:
                    # value will be bytes
                    if isinstance(e.attrib['value'], bytes):
                        value = value.encode("utf-8")
                    assert e.attrib['value'] == value, \
                           "Expected value of hidden input '%s' to be '%s', got '%s'" % \
                           (e.attrib['name'], value, e.attrib['value'])
                    break
            else:
                self.fail("Post arg '%s' not found in form" % (name, ))

        for e in hiddens:
            assert e.attrib['name'] in list(message_.toPostArgs().keys()), \
                   "Form element for '%s' not in " + \
                   "original message" % (e.attrib['name'])

        # Check action URL
        assert form.attrib['action'] == action_url, \
               "Expected form 'action' to be '%s', got '%s'" % \
               (action_url, form.attrib['action'])

        # Check submit text
        submits = [e for e in form \
                   if e.tag.upper() == 'INPUT' and \
                   e.attrib['type'].upper() == 'SUBMIT']

        assert len(submits) == 1, \
               "Expected only one 'input' with type = 'submit', got %d" % \
               (len(submits),)

        assert submits[0].attrib['value'] == submit_text, \
               "Expected submit value to be '%s', got '%s'" % \
               (submit_text, submits[0].attrib['value'])

    def test_toFormMarkup(self):
        m = message.Message.fromPostArgs(self.postargs)
        html = m.toFormMarkup(self.action_url, self.form_tag_attrs,
                              self.submit_text)
        self._checkForm(html, m, self.action_url, self.form_tag_attrs,
                        self.submit_text)

    def test_toFormMarkup_bug_with_utf8_values(self):
        postargs = {
            'openid.ns': message.OPENID2_NS,
            'openid.mode': 'checkid_setup',
            'openid.identity': 'http://bogus.example.invalid:port/',
            'openid.assoc_handle': 'FLUB',
            'openid.return_to': 'Neverland',
            'ünicöde_key': 'ünicöde_välüe',
        }
        m = message.Message.fromPostArgs(postargs)
        # Calling m.toFormMarkup with lxml used for ElementTree will throw
        # a ValueError.
        html = m.toFormMarkup(self.action_url, self.form_tag_attrs,
                              self.submit_text)
        # Using the (c)ElementTree from stdlib will result in the UTF-8
        # encoded strings to be converted to XML character references,
        # "ünicöde_key" becomes "&#195;&#188;nic&#195;&#182;de_key" and
        # "ünicöde_välüe" becomes "&#195;&#188;nic&#195;&#182;de_v&#195;&#164;l&#195;&#188;e"
        self.assertFalse(
            '&#195;&#188;nic&#195;&#182;de_key' in html,
            'UTF-8 bytes should not convert to XML character references')
        self.assertFalse(
            '&#195;&#188;nic&#195;&#182;de_v&#195;&#164;l&#195;&#188;e' in
            html, 'UTF-8 bytes should not convert to XML character references')

    def test_overrideMethod(self):
        """Be sure that caller cannot change form method to GET."""
        m = message.Message.fromPostArgs(self.postargs)

        tag_attrs = dict(self.form_tag_attrs)
        tag_attrs['method'] = 'GET'

        html = m.toFormMarkup(self.action_url, self.form_tag_attrs,
                              self.submit_text)
        self._checkForm(html, m, self.action_url, self.form_tag_attrs,
                        self.submit_text)

    def test_overrideRequired(self):
        """Be sure that caller CANNOT change the form charset for
        encoding type."""
        m = message.Message.fromPostArgs(self.postargs)

        tag_attrs = dict(self.form_tag_attrs)
        tag_attrs['accept-charset'] = 'UCS4'
        tag_attrs['enctype'] = 'invalid/x-broken'

        html = m.toFormMarkup(self.action_url, tag_attrs, self.submit_text)
        self._checkForm(html, m, self.action_url, tag_attrs, self.submit_text)

    def test_setOpenIDNamespace_invalid(self):
        m = message.Message()
        invalid_things = [
            # Empty string is not okay here.
            '',
            # Good guess!  But wrong.
            'http://openid.net/signon/2.0',
            # What?
            'http://specs%\\\r2Eopenid.net/auth/2.0',
            # Too much escapings!
            'http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0',
            # This is a Type URI, not a openid.ns value.
            'http://specs.openid.net/auth/2.0/signon',
        ]

        for x in invalid_things:
            self.assertRaises(message.InvalidOpenIDNamespace,
                              m.setOpenIDNamespace, x, False)

    def test_isOpenID1(self):
        v1_namespaces = [
            # Yes, there are two of them.
            'http://openid.net/signon/1.1',
            'http://openid.net/signon/1.0',
        ]

        for ns in v1_namespaces:
            m = message.Message(ns)
            self.assertTrue(m.isOpenID1(),
                            "%r not recognized as OpenID 1" % (ns, ))
            self.assertEqual(ns, m.getOpenIDNamespace())
            self.assertTrue(
                m.namespaces.isImplicit(ns),
                m.namespaces.getNamespaceURI(message.NULL_NAMESPACE))

    def test_isOpenID2(self):
        ns = 'http://specs.openid.net/auth/2.0'
        m = message.Message(ns)
        self.assertTrue(m.isOpenID2())
        self.assertFalse(m.namespaces.isImplicit(message.NULL_NAMESPACE))
        self.assertEqual(ns, m.getOpenIDNamespace())

    def test_setOpenIDNamespace_explicit(self):
        m = message.Message()
        m.setOpenIDNamespace(message.THE_OTHER_OPENID1_NS, False)
        self.assertFalse(m.namespaces.isImplicit(message.THE_OTHER_OPENID1_NS))

    def test_setOpenIDNamespace_implicit(self):
        m = message.Message()
        m.setOpenIDNamespace(message.THE_OTHER_OPENID1_NS, True)
        self.assertTrue(m.namespaces.isImplicit(message.THE_OTHER_OPENID1_NS))

    def test_explicitOpenID11NSSerialzation(self):
        m = message.Message()
        m.setOpenIDNamespace(message.THE_OTHER_OPENID1_NS, implicit=False)

        post_args = m.toPostArgs()
        self.assertEqual(post_args, {
            'openid.ns': message.THE_OTHER_OPENID1_NS,
        })

    def test_fromPostArgs_ns11(self):
        # An example of the stuff that some Drupal installations send us,
        # which includes openid.ns but is 1.1.
        query = {
            'openid.assoc_handle': '',
            'openid.claimed_id': 'http://foobar.invalid/',
            'openid.identity': 'http://foobar.myopenid.com',
            'openid.mode': 'checkid_setup',
            'openid.ns': 'http://openid.net/signon/1.1',
            'openid.ns.sreg': 'http://openid.net/extensions/sreg/1.1',
            'openid.return_to': 'http://drupal.invalid/return_to',
            'openid.sreg.required': 'nickname,email',
            'openid.trust_root': 'http://drupal.invalid',
        }
        m = message.Message.fromPostArgs(query)
        self.assertTrue(m.isOpenID1())


class NamespaceMapTest(unittest.TestCase):
    def test_onealias(self):
        nsm = message.NamespaceMap()
        uri = 'http://example.com/foo'
        alias = "foo"
        nsm.addAlias(uri, alias)
        self.assertTrue(nsm.getNamespaceURI(alias) == uri)
        self.assertTrue(nsm.getAlias(uri) == alias)

    def test_iteration(self):
        nsm = message.NamespaceMap()
        uripat = 'http://example.com/foo%r'

        nsm.add(uripat % 0)
        for n in range(1, 23):
            self.assertTrue(uripat % (n - 1) in nsm)
            self.assertTrue(nsm.isDefined(uripat % (n - 1)))
            nsm.add(uripat % n)

        for (uri, alias) in list(nsm.items()):
            self.assertTrue(uri[22:] == alias[3:])

        i = 0
        it = nsm.iterAliases()
        try:
            while True:
                next(it)
                i += 1
        except StopIteration:
            self.assertTrue(i == 23)

        i = 0
        it = nsm.iterNamespaceURIs()
        try:
            while True:
                next(it)
                i += 1
        except StopIteration:
            self.assertTrue(i == 23)


if __name__ == '__main__':
    unittest.main()
