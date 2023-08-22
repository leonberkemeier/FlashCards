from django import forms
from django import forms

from . models import Card

class CardForm(forms.ModelForm):
    # title = forms.CharFFileield(required=False)
    front = forms.FileField(required=False)
    back = forms.FileField()
    # side = forms.IntegerField()

    class Meta:
        model = Card
        fields = ('title','front','back')