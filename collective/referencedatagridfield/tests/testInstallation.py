import unittest
from collective.referencedatagridfield.tests.base import TestCase


class TestInstallation(TestCase):
    """ Installation unit tests """
    def afterSetUp(self):
        self.skins = self.portal.portal_skins

    def test_skininstall(self):
        self.assertEqual('referencedatagridfield' in self.skins.objectIds(), True)

    def test_skinlayer(self):
        for sname, slaers in self.skins.getSkinPaths():
            self.assertEqual('referencedatagridfield' in slaers, True)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestInstallation),
        ])
