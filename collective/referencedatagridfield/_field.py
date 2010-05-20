#from Products.Archetypes import atapi
import re
import logging
import urlparse
from urllib import quote
from types import ListType, TupleType

from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.validation import validation #validators import baseValidators
from Products.Archetypes.Field import encode, ReferenceField
from Products.Archetypes.Registry import registerField, registerWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.DataGridField.Column import Column
from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.DataGridWidget import DataGridWidget

from collective.referencedatagridfield.columns import BlockColumn
from collective.referencedatagridfield.columns import HiddenColumn
from collective.referencedatagridfield.columns import StyledColumn

# Logger object
#logger = logging.getLogger('ReferenceDataGridField')
#logger.debug("ReferenceDataGrid loading")

class ReferenceDataGridWidget(DataGridWidget, ReferenceBrowserWidget):
    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update(DataGridWidget._properties.copy())
    _properties.update({
        'macro': "referencedatagridwidget",
        'helper_css': ('datagridwidget.css','referencedatagridwidget.css'),
        'helper_js': ('referencebrowser.js', 'datagridwidget.js', 'referencedatagridwidget.js'),
        'force_close_on_insert': True,
        'popup_name': 'datagridref_popup',
        'columns': {
            'title': StyledColumn("Title", trigger_key="default_title",
                                  blur_handler="triggerTitleClass",
                                  focus_handler="triggerOnFocusStyles",
                                  class_no=None,
                                  class_changed="changed-title-field",
                                  class_not_changed="not-changed-title-field"),
            'link': BlockColumn("Link", column_on_class="hidden-field",
                                columns=['link','uid'], read_only=True),
            'uid': HiddenColumn("UID", visible=False)},
        })

isURL = validation.validatorFor('isURL')

class ReferenceDataGridField(DataGridField, ReferenceField):
    _properties = ReferenceField._properties.copy()
    _properties.update(DataGridField._properties.copy())
    _properties.update({
        'columns': ('title', 'link', 'uid'),
        'widget': ReferenceDataGridWidget,
        'multiValued' : True,
        })

    security = ClassSecurityInfo()

    security.declarePrivate('isRemoteURL')
    def isRemoteURL(self, url):
        return isURL(url) == 1 and True or False

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """
        The passed in object should be a records object, or a sequence of dictionaries
        About link data:
          * interpretations:
            * if data not starts with standard protocol names (http://, ftp://) than
              *uid* field data will be used as reference
          * record removed if:
            * no data;
            * data contains UID of not existent object
        About title:
          * if there is UID of existent object and record has same title to the original
            object - title will not be saved.
        """
        catalog = getToolByName(instance, "uid_catalog")

        if value is None:
            value = ()

        if not isinstance(value, (ListType, TupleType)):
            value = value,

        result = []
        for row in value:
            data = {"title":"", "link":"", "uid":""}

            uid = str(row.get("uid", "")).strip()
            link = str(row.get("link", "")).strip()
            title = str(row.get('title', ""))

            if not title == "":
                data["title"] = title

            if link == "":
                continue
            elif self.isRemoteURL(link):
                data["link"] = urlparse.urlunparse(urlparse.urlparse(link))
            else:
                if uid == '':
                    continue

                brains = catalog(UID=uid)
                if len(brains) == 0:
                    continue
                # Found objects with pointed UID
                brain = brains[0]
                data["uid"] = uid
                # Fix title for uid
                if data['title'] == getattr(brain, "Title", ""):
                    data['title'] = ""
            result.append(data)

        DataGridField.set(self, instance, result, **kwargs)

        uids = [r['uid'] for r in result if r['uid']!=""]
        ReferenceField.set(self, instance, uids, **kwargs)
        
    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        """ Return DataGridField value

        Value is a list object of rows.
        Row id dictionary object with standard 'link', 'uid' and 'title' keys
        plus extra informal *url* and *url_title* keys
        """
        purl = getToolByName(instance, "portal_url")
        # use portal_catalog to hide protected object for the logged in user.
        catalog = getToolByName(instance, "portal_catalog")

        result = []
        uids = {}
        rows = DataGridField.get(self, instance, **kwargs)
        for row in rows:
            uid = row.get("uid","")
            link = row.get("link","")
            title = row.get("title","")
            result.append({
                # DataGridField row data
                "uid": uid, "link": link, "title": title,
                # View data
                "url": "", "default_title": None})
            data = result[-1]
            # Process remote URL and collect UIDs
            if link:
                data["url"] = quote(link, safe='?$#@/:=+;$,&%')
                data["default_title"] = link
                # if title not set for remote url - set it equals to url
                if not data["title"]:
                    data["title"] = data["default_title"]
            else:
                uids[uid] = data
        # Process UIDs
        if uids:
            brains = catalog(UID=uids.keys())
            for b in brains:
                data = uids[b.UID]
                data["url"] = b.getURL()
                data["link"] = b.getPath()
                data["default_title"] = self._brains_title_or_id(b, instance)
                # If title not set - get it from the brain
                if not data["title"]:
                    data["title"] = data["default_title"]
            # Remove records with links to unexistent objects
            del_uids = set(uids.keys()) - set([b.UID for b in brains])
            result = filter(lambda r: not r["uid"] in del_uids, result)

        return result


registerWidget(
    ReferenceDataGridWidget,
    title='DataGrid Reference',
    used_for=('collective.referencedatagridfield.ReferenceDataGridField',)
    )

registerField(
    ReferenceDataGridField,
    title="DataGrid Reference Field",
    description=("Reference DataGrid field.")
    )
