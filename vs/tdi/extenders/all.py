################################################################
# vs.tdi
# (C) 2012, Veit Schiele communications GmbH
# Author: Andreas Jung, ZOPYX Ltd
################################################################

from zope.interface import implements
from zope.component import adapts 
from Products.Archetypes import atapi
from Products.ATContentTypes.interfaces import IATContentType, IATFile
from Products.ATContentTypes import ATCTMessageFactory as _
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

import plone.api


class StringField(ExtensionField, atapi.StringField):
    """ String field """


class All(object):
    adapts(IATContentType)
    implements(ISchemaExtender)

    fields = [StringField('tabText',
                         default='',
                         storage = atapi.AnnotationStorage(migrate=True),
                         widget=atapi.StringWidget(
                            size=20,
                            maxlength=20,
                            label=_(u'label_alternative_tab_text', u'Optional tab text'),
                         )
                    )
            ] 

    def __init__(self, context):
        self.context = context

    def getFields(self):
        qi = plone.api.portal.get_tool('portal_quickinstaller')
        try:
            pp = plone.api.portal.get_tool('portal_properties')
            not_used_for_types = pp.vs_tdi.not_used_for_types
        except AttributeError:
            not_used_for_types = ()
        installedProducts = qi.listInstalledProducts()
        ids = [p['id'] for p in qi.listInstalledProducts()]
        if self.context.portal_type in not_used_for_types:
            return ()
        if not 'vs.tdi' in ids:
            return ()
        return self.fields


