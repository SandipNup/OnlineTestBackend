import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.serializers import ValidationError

import uuid

class Base64ImageField(serializers.Field):
  '''
  For image , send base64 string as json
  '''

  def to_internal_value(self, data):

    try:
      format, imgstr = data.split(';base64,')
      ext = format.split('/')[-1]

      data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4())+'.'+ext) # You can save this as file instance.

      print(data)

    except:
      raise ValidationError('Error in data')
      
    return data
