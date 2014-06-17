from collective.referencedatagridfield._field import ReferenceDataGridField  # nopep8
from collective.referencedatagridfield._field import ReferenceDataGridWidget  # nopep8

from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types

PKG_NAME = 'collective.referencedatagridfield'


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    # Example content type initialization
    import collective.referencedatagridfield.examples  # nopep8
    import collective.referencedatagridfield.columns  # nopep8
    content_types, constructors, ftis = process_types(
        listTypes(PKG_NAME), PKG_NAME,)

    ContentInit(
        '%s Content' % PKG_NAME,
        content_types=content_types,
        permission=AddPortalContent,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
