import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager

from Products.Archetypes.tests.utils import makeContent

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

# install site
ptc.setupPloneSite(extension_profiles=[
        'collective.referencedatagridfield:default',
        'collective.referencedatagridfield:examples'
        ])

import collective.referencedatagridfield

class MixIn(object):
    """ Mixin for setting up the necessary bits for testing the
        collective.referencedatagridfield
    """

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.referencedatagridfield)
            ztc.installPackage('collective.referencedatagridfield')
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def createDemo(self, wfaction=None):
        # Create tested content
        sm = getSecurityManager()
        self.loginAsPortalOwner()
        content = {
            "demo": {"type":'ReferenceDataGridDemoType', "title": 'RDGF Demo'},
            "doc": {"type":'Document', "title": 'Test Document'},
            "doc2": {"type":'Document', "title": 'Test Document 2'},
            }
        try:
            wf = self.portal.portal_workflow
            for cid, data in content.items():
                makeContent(self.portal, portal_type=data['type'], id=cid)
                obj = getattr(self.portal, cid)
                obj.setTitle(data['title'])
                obj.reindexObject()
                if wfaction:
                    wf.doActionFor(obj, wfaction)
                setattr(self, cid, obj)
        finally:
            setSecurityManager(sm)

class TestCase(MixIn, ptc.PloneTestCase):
    """ Base TestCase for collective.referencedatagridfield """

class FunctionalTestCase(MixIn, ptc.FunctionalTestCase):
    """ Base TestCase for collective.referencedatagridfield """

