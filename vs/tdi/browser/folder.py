from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class Folder(BrowserView):

    def getTabs(self):

        props = getToolByName(self.context, 'portal_properties').vs_tdi
        catalog = getToolByName(self.context, 'portal_catalog')

        result = list()
        brains = self.context.getFolderContents(dict(portal_type=props.used_for_types, 
                                                     sort_on='getObjPositionInParent'))
        for i, brain in enumerate(brains):
            result.append(dict(id=brain.getId,
                               tabText=brain.Title[:20],
                               content='hello world' + str(i)))
        return result
