from collective.referencedatagridfield._field import ReferenceDataGridField
from collective.referencedatagridfield._field import ReferenceDataGridWidget

from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types

PKG_NAME = 'collective.referencedatagridfield'

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    # Example content type initialization
    import collective.referencedatagridfield.examples
    import collective.referencedatagridfield.columns
    content_types, constructors, ftis = process_types(listTypes(PKG_NAME), PKG_NAME,)

    ContentInit(
        '%s Content' % PKG_NAME,
        content_types = content_types,
        permission = AddPortalContent,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)
