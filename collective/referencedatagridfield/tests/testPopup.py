import re
import unittest

from zope.publisher.browser import TestRequest
from zope.formlib.namedtemplate import INamedTemplate
from zope.component import queryAdapter, queryMultiAdapter

from Products.Five import BrowserView

from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

from collective.referencedatagridfield import ReferenceDataGridWidget
from collective.referencedatagridfield.tests.base import TestCase
from collective.referencedatagridfield.tests.base import FunctionalTestCase


class TestPopupRegistrations(TestCase):
    """Test popup related adapters registration."""

    def afterSetUp(self):
        self.req = TestRequest()

    def test_CustomNamedTemplate(self):
        view = BrowserView(self.portal, self.req)
        custom_named_template = queryAdapter(view, INamedTemplate, name="datagridref_popup")
        self.assertNotEqual(custom_named_template, None)
        
    def test_RefDataGridBrowser_popup(self):
        popup_page = queryMultiAdapter((object(), self.req), name="refdatagridbrowser_popup")
        self.assertNotEqual(popup_page, None)

    def test_WidgetBindToNamedTemplate(self):
        rdgw_props = ReferenceDataGridWidget._properties
        self.assertEqual(rdgw_props.get("popup_name", ""), "datagridref_popup")


class TestPopupRelatedStaff(FunctionalTestCase):
    """Test pupup related staff in edit mode of ReferenceDataGridWidget."""

    def testAddReferenceButton(self):
        self.loginAsPortalOwner()
        # Prepare testing data and data for functional test
        self.createDemo()
        self.demo.edit(demo_rdgf=[{"link": "http://google.com"}])
        html = self.publish("/%s/edit" % self.demo.absolute_url(1),
                            portal_owner+':'+default_password).getBody()
        # Get Add... button
        rebutt = re.compile("<input\s+[^>]*type=\"button\"\s*[^>]*>", re.S)
        add_button = filter(lambda k:not "_new" in k, rebutt.findall(html))[0]
        src = re.search("src=\"([^\"]*)\"", add_button).groups()[0]
        # src url must points to refdatagridbrowser_popup view
        url = self.demo.absolute_url() + '/refdatagridbrowser_popup?'
        self.assertEqual(src.startswith(url), True)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestPopupRegistrations),
        unittest.makeSuite(TestPopupRelatedStaff),
        ])
