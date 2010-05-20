from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.form._named import named_template_adapter

from archetypes.referencebrowserwidget.browser.view import \
         ReferenceBrowserPopup

datagridref_popup_template = named_template_adapter(
    ViewPageTemplateFile('datagridref_popup.pt'))


class ReferenceDataGridBrowserPopup(ReferenceBrowserPopup):
    """ Extend default ReferenceBrowserPopup view with  properties,
        needed for ReferenceDataGridBrowserPopup
    """

    def __init__(self, context, request):
        super(ReferenceDataGridBrowserPopup, self).__init__(context, request)

        self.fieldTitleName = request.get('fieldTitleName','')
        self.fieldLinkName = request.get('fieldLinkName','')
        self.close_window = '1';

    def genRefBrowserUrl(self, urlbase):
        url = super(ReferenceDataGridBrowserPopup, self).genRefBrowserUrl(urlbase)
        url += "&fieldTitleName=%s&fieldLinkName=%s" % (self.fieldTitleName, self.fieldLinkName)
        return url
