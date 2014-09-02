try:
    import simplejson as json
except ImportError:
    import json
from zope.interface import implements
from collective.googleanalytics.bbb import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from collective.googleanalytics.interfaces.tracking import IAnalyticsTrackingPlugin
from collective.googleanalytics.config import FILE_EXTENSION_CHOICES
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from Products.PloneFormGen.interfaces import IPloneFormGenThanksPage

class AnalyticsBaseTrackingPlugin(object):
    """
    Base plugin for tracking information in Google Analytics.
    """
    
    implements(IAnalyticsTrackingPlugin)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def relative_url(self):
        """
        Returns the relative URL of the request.
        """
        
        relative_url = self.request.ACTUAL_URL.replace(self.request.SERVER_URL, '').strip()
        if relative_url.endswith('/') and len(relative_url) > 1:
            return relative_url[:-1]
        return relative_url

class AnalyticsExternalLinkPlugin(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track external links.
    """
    
    __call__ = ViewPageTemplateFile('external.pt')
    
class AnalyticsEmailLinkPlugin(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track e-mail links.
    """

    __call__ = ViewPageTemplateFile('email.pt')
    
class AnalyticsDownloadPlugin(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track file downloads.
    """

    __call__ = ViewPageTemplateFile('download.pt')
    
    file_extensions = json.dumps(FILE_EXTENSION_CHOICES)
    
class AnalyticsCommentPlugin(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track posting of comments.
    """

    __call__ = ViewPageTemplateFile('comment.pt')
    
class AnalyticsUserTypePlugin(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track user type as a custom variable.
    """

    __call__ = ViewPageTemplateFile('usertype.pt')
    
    def user_type(self):
        """
        Returns Member if the user is logged or Visitor otherwise.
        """
        
        membership = getToolByName(self.context, 'portal_membership')
        if membership.isAnonymousUser():
            return 'Visitor'
        return 'Member'

class AnalyticsPageLoadTimePlugin(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track page load time.
    """

    __call__ = ViewPageTemplateFile('pageloadtime.pt')

class PFGAnalyticsPlugin(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track form views, submissions and errors.
    """

    __call__ = ViewPageTemplateFile('ploneformgen.pt')

    def form_status(self):
        """
        Returns the status of the form, which can be None (not a form),
        'form' (viewing the form), 'thank-you' (form succesfully submitted),
        or 'error' (form has validation errors).
        """

        if IPloneFormGenForm.providedBy(self.context):
            if 'form_submit' in self.request.form.keys():
                return 'error'
            return 'form'
        elif IPloneFormGenThanksPage.providedBy(self.context):
            return 'thank-you'
        return None
