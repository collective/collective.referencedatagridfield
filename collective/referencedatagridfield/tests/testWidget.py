import re
import unittest

from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

from collective.referencedatagridfield.tests.base import TestCase
from collective.referencedatagridfield.tests.base import FunctionalTestCase
from collective.referencedatagridfield import ReferenceDataGridWidget


class TestWidgetView(FunctionalTestCase):
    """ ReferenceDataGridWidget unit tests """

    def afterSetUp(self):
        self.loginAsPortalOwner()
        # Prevent section links
        sp = self.portal.portal_properties.site_properties
        sp._updateProperty("disable_nonfolderish_sections", True)
        # Prepare testing data and data for functional test
        self.createDemo(wfaction="publish")
        self.demo_path = "/" + self.demo.absolute_url(1)
        self.basic_auth = ':'.join((portal_owner,default_password))
        # Regexp for getting links
        self.relink = re.compile("<a\s+[^>]*?href=\"(.*?)\"[^>]*?>\s*(.*?)\s*</a>",
                                 re.I|re.S|re.M)

    def test_LinkDefaultTitle(self):
        self.demo.edit(demo_rdgf=[{"link": "http://google.com"}])
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))
        
        self.assertEqual(links.has_key("http://google.com"), True)
        self.assertEqual("http://google.com" in links["http://google.com"], True)
 
    def test_LinkCustomTitle(self):
        self.demo.edit(demo_rdgf=[{"link": "http://google.com", "title": "Google"}])
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))
        
        self.assertEqual(links.has_key("http://google.com"), True)
        self.assertEqual("Google" in links["http://google.com"], True)
 
    def test_UIDDefaultTitle(self):
        data = [{"uid": self.doc.UID(), "link": self.doc.absolute_url(1)}]
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))

        doc_url = self.doc.absolute_url()
        doc_title = self.doc.Title()
        self.assertEqual(links.has_key(doc_url), True)
        self.assertEqual(doc_title in links[doc_url], True)

    def test_UIDCustomTitle(self):
        data = [{"uid": self.doc.UID(), "link": self.doc.absolute_url(1),
                 "title": "Custom Title"},]
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = dict(self.relink.findall(html))

        doc_url = self.doc.absolute_url()
        self.assertEqual(links.has_key(doc_url), True)
        self.assertEqual("Custom Title" in links[doc_url], True)

    def test_LinksOrder(self):
        relink = re.compile("<a\s+[^>]*?href=\"(.*?)\"[^>]*?>", re.I|re.S)
        data = [{"link": "http://google.com"},
                {"uid": self.doc.UID(), "link": self.doc.absolute_url(1)}]
        # First check in one order
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = relink.findall(html)
        idx1 = links.index("http://google.com")
        idx2 = links.index(self.doc.absolute_url())
        self.assertEqual( idx1 < idx2, True)
        # Now reverse rows order
        data.reverse()
        self.demo.edit(demo_rdgf=data)
        html = self.publish(self.demo_path, self.basic_auth).getBody()
        links = relink.findall(html)
        idx1 = links.index("http://google.com")
        idx2 = links.index(self.doc.absolute_url())
        self.assertEqual( idx1 > idx2, True)
        

class TestWidgetEditPresence(FunctionalTestCase):
    """ Test presence of columns and button
        in edit mode of ReferenceDataGridWidget.
    """

    def afterSetUp(self):
        self.loginAsPortalOwner()
        # Prepare test data
        self.createDemo()
        self.demo.edit(demo_rdgf=[{"link": "http://google.com"}])
        # Prepare html for test edit form
        edit_path = "/%s/edit" % self.demo.absolute_url(1)
        basic_auth = ':'.join((portal_owner,default_password))
        self.html = self.publish(edit_path, basic_auth).getBody()

    def test_columnsPresence(self):
        # Get ReferenceDataGridField field inputs without hidden template row for add new data
        reinput = re.compile("<input\s+([^>]*?name=\"demo_rdgf\.(.*?):records\"[^>]*?)>", re.I|re.S)
        inputs = dict([(v,k) for k,v in reinput.findall(self.html) if not "demo_rdgf_new" in k])
        # Title and Link columns is visible
        self.assertEqual('type="text"' in inputs["title"], True)
        self.assertEqual('type="text"' in inputs["link"], True)
        # UID column is hidden
        self.assertEqual('type="hidden"' in inputs["uid"], True)

    def test_addButtonPresence(self):
        # Button for adding reference also must present
        rebutt = re.compile("<input\s+[^>]*type=\"button\"\s*[^>]*>", re.I|re.S)
        buttons = filter(lambda k:not "_new" in k, rebutt.findall(self.html))
        # Add... button must present
        self.assertEqual('value="Add..."' in buttons[0], True)


class TestWidgetResources(TestCase):
    """Tests of widget resources."""

    def afterSetUp(self):
        self.widget_props = ReferenceDataGridWidget._properties
        self.rdgw_skin_ids = self.portal.portal_skins.referencedatagridfield.objectIds()

    def test_helperJS(self):
        helper_js = self.widget_props.get("helper_js", "")
        self.assertEqual("referencedatagridwidget.js" in helper_js, True)
        self.assertEqual("referencedatagridwidget.js" in self.rdgw_skin_ids, True)

    def test_helperCSS(self):
        helper_css = self.widget_props.get("helper_css", "")
        self.assertEqual("referencedatagridwidget.css" in helper_css, True)
        self.assertEqual("referencedatagridwidget.css" in self.rdgw_skin_ids, True)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestWidgetView),
        unittest.makeSuite(TestWidgetResources),
        unittest.makeSuite(TestWidgetEditPresence),
        ])
