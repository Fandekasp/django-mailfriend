from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
try:
    from django.core.validators import email_re
except ImportError:
    from django.forms.fields import email_re

from mailfriend.models import MailedItem
from mailfriend.utils import generic_object_get, split

MAX = getattr(settings, 'MAILFRIEND_MAX_ADDRESSES', 3)

class MailedItemForm(forms.ModelForm):
    class Meta:
        model = MailedItem
        exclude = ('mailed_by','date_mailed')
    
    def __init__(self, *args, **kwargs):
        super(MailedItemForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()
    
    def check_generic_object(self):
        """
        Check that the generic object exists.
        
        If it doesn't, we bail early
        """
        ct_pk = int(self.data['content_type'])
        obj_pk = int(self.data['object_id'])
        return generic_object_get(ct_pk, obj_pk)
        
    def clean_mailed_to(self):
        to = split(self.cleaned_data['mailed_to'])
        if len(to) > MAX:
            raise forms.ValidationError(_(u'You can only send up to %s addresses at a time' % MAX))
        for address in to:
            if not email_re.match(address):
                raise forms.ValidationError(_(u'Invalid e-mail address "%s"') % address)
        return self.cleaned_data['mailed_to']