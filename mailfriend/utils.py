import re
from django.contrib.contenttypes.models import ContentType

def generic_object_get(ct_pk, obj_pk):
    """
    Get an object based on its content type and primary key
    
    Raises an exception if it does not exist.
    """
    content_type = ContentType.objects.get(pk=ct_pk)
    obj = content_type.get_object_for_this_type(pk=obj_pk)
    return content_type, obj

def split(s):
    """
    Splits a string by commas, semicolon and spaces and then strips each fragment.
    Used for multiple email address parsing
    """
    return [x.strip() for x in re.split(',|;|\s', s) if x]