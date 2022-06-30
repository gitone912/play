from django.forms import ModelForm
from .models import rom


class modelForm(ModelForm):
    
    class Meta:
        model = rom
        fields ='__all__'
        exclude = ['host','participants']
