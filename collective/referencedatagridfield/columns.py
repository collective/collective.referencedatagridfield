from plone.memoize.view import memoize

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column

class HiddenColumn(Column):
    """ Column with non-changeable text
    
    Useful with DataGridField.fixed_row property in some use cases.
    """
    security = ClassSecurityInfo()

    def __init__(self, label, default=None, label_msgid=None, visible=True):
        """ Create a column
        
            @param hide Hide column from displaying
        """
        Column.__init__(self, label, default, label_msgid)
        self.visible = visible

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "referencedatagrid_hidden_cell"

# Initializes class security
InitializeClass(HiddenColumn)

class BlockColumn(Column):
    """ Column with possibility to block the cell data from changing,
        based on the value of the row data.
    """
    security = ClassSecurityInfo()

    def __init__(self, label, default=None, label_msgid=None,
                 column_on_class=None, column_off_class=None,
                 columns=[], invert=False, read_only=None):
        """ Create a column, with adding class attribute depend on value presence for the cell.
        
            @param column_on_class set class, which will be added to the <input> tag if columns has value
            @param column_off_class set class, which will be added to the <input> tag if columns not has value
            @param columns list of columns names, which values will be checked for set class attribute
            @param invert - invert the adding class logic
            @param read_only - check-on/off readOnly attribute for the <input> tag
        """
        Column.__init__(self, label, default, label_msgid)
        self.column_on_class = column_on_class
        self.column_off_class = column_off_class
        self.columns = columns
        self.invert = invert
        self.read_only = read_only

    def passCondition(self, row_data):
        """ Return calculated class attribute."""
        res = sum([1 for c in self.columns if row_data.get(c,0)])
        return res == len(self.columns) and not self.invert
    
    security.declarePublic('getAttributesData')
    def getAttributesData(self, row_data):
        """ Return calculated class attribute."""
        res = {'style_class': None, 'read_only': None}
        isPassCondition = self.passCondition(row_data)
        if self.column_on_class or self.column_off_class:
           res['style_class'] = isPassCondition and self.column_on_class or self.column_off_class
        if self.read_only:
           res['read_only'] = isPassCondition and True or False

        return res
    
    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "referencedatagrid_block_cell"

# Initializes class security
InitializeClass(BlockColumn)

class StyledColumn(Column):
    """ Column with styling based on events."""
    security = ClassSecurityInfo()

    def __init__(self, label, default=None, label_msgid=None,
                 trigger_key=None, blur_handler="", focus_handler="",
                 class_no="", class_changed="", class_not_changed=""):
        """ Create a column
        
            @param trigger_key
        """
        Column.__init__(self, label, default, label_msgid)
        self.trigger = trigger_key
        self.blur_handler = blur_handler and blur_handler + "(event)" or ""
        self.focus_handler = focus_handler and focus_handler + "(event)" or ""
        self.class_no = class_no
        self.class_not_changed = class_not_changed
        self.class_changed = class_changed

    security.declarePublic("getAttributes")
    def getAttributes(self, column_id, rows):
        default = None
        blur_handler = None
        focus_handler = None
        sclass = self.class_no

        if rows.has_key(self.trigger) \
           and rows.has_key(column_id):
            focus_handler = self.focus_handler
            blur_handler = self.blur_handler
            current = rows[column_id]
            default = rows[self.trigger]
            # if default is not epty string - than it is same to original value
            if current == default:
                sclass = self.class_not_changed
            else:
                sclass = self.class_changed

        return {'class': sclass,
                'onblur': blur_handler,
                'onfocus': focus_handler,
                'default': default}

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "referencedatagrid_styled_cell"

# Initializes class security
InitializeClass(StyledColumn)

