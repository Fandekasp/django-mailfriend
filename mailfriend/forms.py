from django import forms
from django.core.validators import email_re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mailfriend.models import MailedItem
from mailfriend.utils import generic_object_get, split

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
        for address in split(self.cleaned_data['mailed_to']):
            if not email_re.match(address):
                raise ValidationError(_(u'Invalid e-mail address "%s"') % address)
        return self.cleaned_data['mailed_to']