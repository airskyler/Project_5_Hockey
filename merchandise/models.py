from __future__ import unicode_literals
from django.db import models



# This is creating Merchandise table, with name field with data type text and
# price field with float data type

class Merchandise(models.Model):

    name = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name + ' :   ' + '$' +str(self.price)




# Creating Game table
# The date field is just using date data type and no time value
class Game(models.Model):
    opponent = models.TextField()
    date = models.DateField()
    homeVSaway = models.CharField(choices=(('H','Home'),('A','Away')),max_length=1)


# This code is necessary to display a merchandise objects in the forms.py in the model form
    def __str__(self):
        return self.opponent + ':' + self.homeVSaway + ':' + str(self.date)



# Creating a SoldItem table
# merch field is a reference of the Merchandise table
# game field is a reference of the Game table
class SoldItem(models.Model):
    merch = models.ForeignKey(Merchandise)
    game = models.ForeignKey(Game)
    numberSold = models.IntegerField()












