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
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from ..config import SUBSIDIARY_LANGUAGES

class StringField(ExtensionField, atapi.StringField):
    """ string field """

class All(object):
    adapts(IATContentType)
    implements(ISchemaExtender)

    fields = [StringField('tabText',
                         default=''
                         storage = atapi.AnnotationStorage(migrate=True),
                         widget=atapi.StringWidget(
                            label=_(u'label_alternative_tab_text', u'Optional tab text'),
                            ),  
                         ),  
            ] 

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


