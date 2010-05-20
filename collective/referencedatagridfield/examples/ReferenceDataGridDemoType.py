from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.ATContentTypes.content.base import ATCTContent


from collective.referencedatagridfield import PKG_NAME
from collective.referencedatagridfield import ReferenceDataGridField
from collective.referencedatagridfield import ReferenceDataGridWidget

class ReferenceDataGridDemoType(ATCTContent):
    """ Simple ReferenceDataGridField demo."""
    security = ClassSecurityInfo()
    schema = BaseSchema + Schema((

        ReferenceDataGridField('demo_rdgf',
            schemata='default',
            relationship="demo_relation",
            widget = ReferenceDataGridWidget(
                label = "Reference DataGrid Field(s)",
                visible = {'edit' : 'visible', 'view' : 'visible'}
            )
        ),
    ))

    meta_type = portal_type = archetype_name = 'ReferenceDataGridDemoType'

registerType(ReferenceDataGridDemoType, PKG_NAME)
