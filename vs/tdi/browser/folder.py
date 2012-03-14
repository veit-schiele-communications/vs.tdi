################################################################
# vs.tdi
# (C) 2012, Veit Schiele communications GmbH
# Author: Andreas Jung, ZOPYX Ltd
################################################################

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
import lxml.html
from lxml.cssselect import CSSSelector

class Folder(BrowserView):

    def getTabs(self):

        catalog = getToolByName(self.context, 'portal_catalog')
        props = getToolByName(self.context, 'portal_properties').vs_tdi

        brains = self.context.getFolderContents(dict(portal_type=props.used_for_types, 
                                                     sort_on='getObjPositionInParent'))
        result = list()
        for i, brain in enumerate(brains):

            # render HTML view of the content object and extract the body 
            # fix this :-)
            obj = brain.getObject()
            layout = obj.getLayout()
            html = getattr(obj, layout)()

            if not isinstance(html, unicode):
                html = unicode(html, 'utf-8')

            root = lxml.html.fromstring(html)
            selector = CSSSelector('#content')
            nodes = selector(root)
            if nodes:
                html = lxml.html.tostring(nodes[0], encoding=unicode)
            else:
                html = 'nothing found'

            result.append(dict(id=brain.getId,
                               tabText=brain.Title[:20],
                               content=html))
        return result
