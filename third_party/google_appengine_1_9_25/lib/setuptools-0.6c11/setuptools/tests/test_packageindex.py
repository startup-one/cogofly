"""Package Index Tests
"""
# More would be better!


import os, shutil, tempfile, unittest, six.moves.urllib.request, six.moves.urllib.error, six.moves.urllib.parse
import pkg_resources
import setuptools.package_index

class TestPackageIndex(unittest.TestCase):

    def test_bad_urls(self):
        index = setuptools.package_index.PackageIndex()
        url = 'http://127.0.0.1/nonesuch/test_package_index'
        try:
            v = index.open_url(url)
        except Exception as v:
            self.assertTrue(url in str(v))
        else:
            self.assertTrue(isinstance(v,six.moves.urllib.error.HTTPError))

    def test_url_ok(self):
        index = setuptools.package_index.PackageIndex(
            hosts=('www.example.com',)
        )
        url = 'file:///tmp/test_package_index'
        self.assertTrue(index.url_ok(url, True))

