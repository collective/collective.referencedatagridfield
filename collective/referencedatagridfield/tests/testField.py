import unittest
from types import ListType, TupleType, DictionaryType
from Products.Archetypes.tests.utils import makeContent

from collective.referencedatagridfield.tests.base import TestCase

from collective.referencedatagridfield import ReferenceDataGridWidget


class TestField(TestCase):
    """ ReferenceDataGridField unit tests """

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.createDemo()
        self.refcat = self.portal.reference_catalog
        self.field = self.demo.getField('demo_rdgf')

    def testColumnProperties(self):
        self.assertEqual(hasattr(self.field, "columns"), True)
        for column in ['title', 'link', 'uid']:
            self.assertEqual(column in self.field.columns, True)

    def testWidget(self):
        self.assertEqual(type(self.field.widget), ReferenceDataGridWidget)

    def testGetInitial(self):
        # If no data set - emty list must be returned
        field_data = self.field.get(self.demo)
        self.assertEqual(type(field_data), ListType)
        self.assertEqual(len(field_data), 0)

    def testGet(self):
        data = [{"uid": self.doc.UID(), "link": "http://test.link", "title": "test"},]
        # if data set:
        # result is list with dictionary items, as in DataGridField
        self.field.set(self.demo, data)

        field_data = self.field.get(self.demo)
        self.assertEqual(type(field_data), ListType)
        self.assertEqual(len(field_data), 1)

        # items in list is Dictionary
        item_data = field_data[0]
        self.assertEqual(type(item_data), DictionaryType)
        # Dictionary contains uid, link, title keys
        self.assertEqual(item_data.has_key("uid"), True)
        self.assertEqual(item_data.has_key("link"), True)
        self.assertEqual(item_data.has_key("title"), True)

    def getData(self, key, index=0):
        data = self.field.get(self.demo)
        return data and data[index].get(key, None) or None

    def getRefsCount(self):
        return len(self.refcat.getReferences(self.demo, self.field.relationship))

    def testSetUID(self):
        # link always must present in the data
        row = {"uid": "", "link": "/"}
        data = [row,]
        # If set unexistent UID - UID - not set
        row['uid'] = "123"
        self.field.set(self.demo, data)
        self.assertEqual(self.getData("uid"), None)
        # No references to the object
        self.assertEqual(self.getRefsCount(), 0)

        # If link is not remote url and passed uid of existent object  - uid is saved
        row["uid"] = self.doc.UID()
        self.field.set(self.demo, data)
        self.assertEqual(self.getData("uid"), self.doc.UID())
        # Also reference added to the object catalog
        self.assertEqual(self.getRefsCount(), 1)

    def testSetTitleForLink(self):
        row = {"link": "http://google.com"}
        data = [row,]
        # If there is title data with external link - it is stored in the field
        row["title"] = "google"
        self.field.set(self.demo, data)
        self.assertEqual(self.getData("title"), "google")

        # If No title specified for the external link title will be  equals to link
        row["title"] = ""
        self.field.set(self.demo, data)
        self.assertEqual(self.getData("title"), "http://google.com")
        
        self.assertEqual(self.getRefsCount(), 0)
        
    def testSetTitleForUID(self):
        row = {"uid": self.doc.UID(), "link": "/"}
        data = [row,]
        # If there is title data with correct uid - it is stored in the field
        row["title"] = "Custom Title"
        self.field.set(self.demo, data)
        self.assertEqual(self.getData("title"), "Custom Title")

        # If No title specified with correct portal UID object - 
        # title will be get from the object
        row["title"] = ""
        self.field.set(self.demo, data)
        self.assertEqual(self.getData("title"), "Test Document")

    def testNoLink(self):
        # Link is key data for the field.
        # If no link present in the data - no data will be saved
        # even with correct uid.
        data = [{"uid": self.doc.UID(), "title": "Title"},]
        self.field.set(self.demo, data)
        self.assertEqual(self.field.get(self.demo), [])
        # If a external link present in the data - it will be saved    
        data = [{"link": "http://google.com"},]
        self.field.set(self.demo, data)
        self.assertEqual(self.getData("link"), "http://google.com")
       

class TestFieldBugs(TestCase):
    """ ReferenceDataGridField unit tests for bugs """

    def afterSetUp(self):
        self.loginAsPortalOwner()
        # minimal demo content creation
        self.demo = makeContent(self.portal, portal_type="ReferenceDataGridDemoType", id="demo")
        self.field = self.demo.getField('demo_rdgf')

    def testGetNotInitializedField(self):
        self.field.getStorage().unset('demo_rdgf', self.demo)
        try:
            data = self.field.get(self.demo)
        except KeyError, e:
            self.fail(str(e) + " on getting data from not initialized field")

    def testDelLinkedObject(self):
        doc = makeContent(self.portal, portal_type="Document", id="doc")
        data = {"uid": doc.UID(), "link": doc.absolute_url(1)}
        self.field.set(self.demo, data)

        res = self.field.get(self.demo)
        self.assertEqual(res[0]["uid"], doc.UID())

        self.portal.manage_delObjects(ids=["doc",])
        try:
            res = self.field.get(self.demo)
        except AttributeError, e:
            self.fail(str(e) + " on getting data when linked object was delited")
        self.assertEqual(len(res), 0, "Not removed data with link to deleted object")

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestField),
        unittest.makeSuite(TestFieldBugs),
        ])
