"""hockeyInventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from merchandise import views as merch_views


# Creating URL for each web page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',merch_views.MainPage, name='MainPage'),
    url(r'^newgame/',merch_views.GamePage, name='GamePage'),
    url(r'^newitem/',merch_views.NewItemPage, name='NewItem'),
    url(r'^solditem/',merch_views.SoldItemPage, name='SoldItem'),
    url(r'^totalsale/',merch_views.TotalSalePage, name='TotalSale'),
    url(r'^bestsale/',merch_views.BestSalePage, name='BestSale'),
    url(r'^leastsale/',merch_views.LeastSoldPage, name='LeastSale'),
    url(r'^itemdescription/',merch_views.ItemDescription, name='ItemDescription'),
]
