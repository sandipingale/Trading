from django.forms import ModelForm
from .models import Shares

class SharesForm(ModelForm):
    class Meta:
        model = Shares
        exclude = ['user']



