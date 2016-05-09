from __future__ import unicode_literals
from django.db import models




class Merchandise(models.Model):
    """This is creating Merchandise table, with name field with data type text and
        price field with float data type"""

    name = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name + ' :   ' + '$' +str(self.price)

    class Meta:
        app_label = 'merchandise'




class Game(models.Model):
    """Creating Game table,
    The date field is just using date data type and no time value"""
    opponent = models.TextField()
    date = models.DateField()
    homeVSaway = models.CharField(choices=(('H','Home'),('A','Away')),max_length=1)



# This code is necessary to display a merchandise objects in the forms.py in the model form
    def __str__(self):
        return self.opponent + ':' + self.homeVSaway + ':' + str(self.date)

    class Meta:
        app_label = 'merchandise'




class SoldItem(models.Model):
    """ Creating a SoldItem table,
        merch field is a reference of the Merchandise table,
        game field is a reference of the Game table"""
    merch = models.ForeignKey(Merchandise)
    game = models.ForeignKey(Game)
    numberSold = models.IntegerField()

    class Meta:
        app_label = 'merchandise'










