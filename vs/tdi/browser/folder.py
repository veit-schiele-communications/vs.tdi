################################################################
################################################################
# vs.tdi
# (C) 2012, Veit Schiele communications GmbH
# Author: Andreas Jung, ZOPYX Ltd
################################################################

from Products.Five.browser import BrowserView
import lxml.html
from lxml.cssselect import CSSSelector
import plone.api

class Folder(BrowserView):

    @property
    def tabObjs(self):
        catalog = plone.api.portal.get_tool('portal_catalog')
        props = plone.api.portal.get_tool('portal_properties').vs_tdi
        not_used_for_types = props.not_used_for_types
        brains = self.context.getFolderContents(dict(sort_on='getObjPositionInParent'))
        return [b for b in brains if not b.portal_type in not_used_for_types]

    def getTabInformation(self):
        """ Return information about contents to be tabified """
        result = list()
        for brain in self.tabObjs:
            obj = brain.getObject()
            field = obj.getField('tabText')
            if field:
                tabText = field.get(obj) or obj.Title()[:30]

            result.append(dict(id=brain.getId,
                               tabText=tabText,
                               uid=obj.UID()))
        return result

    def getTabs(self):
        """ Return all relevant data for rendering all tabs
            for all referenced documents.
        """
        result = list()
        for brain in self.tabObjs:
            # render HTML view of the content object and extract the body 
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
                html = u''

            field = obj.getField('tabText')
            if field:
                tabText = field.get(obj) or obj.Title()[:30]

            result.append(dict(id=brain.getId,
                               tabText=tabText,
                               uid=obj.UID(),
                               content=html))
        return result

    def getHtml(self, uid):
        """ Return the HTML body of a references document by its UID """
        refcat = plone.api.portal.get_tool('reference_catalog')
        obj = refcat.lookupObject(uid)
        layout = obj.getLayout()
        html = getattr(obj, layout)()
        if not isinstance(html, unicode):
            html = unicode(html, 'utf-8')
        root = lxml.html.fromstring(html)
        selector = CSSSelector('#content')
        nodes = selector(root)
        if nodes:
            node = nodes[0]
            node.attrib['style'] = 'display: block'
            return lxml.html.tostring(node, encoding=unicode)
        return 'FOO'

