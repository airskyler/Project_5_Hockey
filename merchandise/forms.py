__author__ = 'Jessy'

from django import forms
from merchandise.models import Merchandise, Game, SoldItem



# Linking the Merchandise, Game and SoldItem tables to be formatted for HTML display
# Must use Meta class for the ModelForm
class MerchandiseForm(forms.ModelForm):
    class Meta:
        model = Merchandise
        fields = '__all__'    # using all field


class GameForm(forms.ModelForm):
    class Meta:
        model= Game
        fields = '__all__'



class SoldItemForm(forms.ModelForm):
    class Meta:
        model = SoldItem
        fields = '__all__'



class FilterForm(forms.Form):

    # Creating a drop down list for either, Home or Away for the user choice to select
    homeVSaway = forms.ChoiceField(choices=(('H','Home'),('A','Away')),required=False,widget=forms.Select())


    # Getting all the item information value from Merchandise table
    def get_items(self):
        return tuple([(name[0], name[0]) for name in Merchandise.objects.values_list('name')])


    def get_dates(self):
        return tuple([(date[0], date[0]) for date in Game.objects.values_list('date')])


    def get_opponents(self):
        return tuple([(opponent[0], opponent[0]) for opponent in Game.objects.values_list('opponent')])



    # Creating a drop down list for the data value of item, dates and opponents for the user selection
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)  # Unpacking positional and key word arguments
        self.fields['ItemName'] = forms.ChoiceField(choices=self.get_items())
        self.fields['GameDate'] = forms.ChoiceField(choices=self.get_dates())
        self.fields['Opponent'] = forms.ChoiceField(choices=self.get_opponents())



