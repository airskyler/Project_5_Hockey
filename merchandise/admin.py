from django.contrib import admin
from merchandise.models import Merchandise, Game, SoldItem

# register these three tables to the admin site

admin.site.register([Merchandise, Game, SoldItem])



