from django.shortcuts import render
from merchandise.forms import MerchandiseForm, GameForm, SoldItemForm, FilterForm
from merchandise.models import Game, Merchandise, SoldItem
from django.shortcuts import redirect
from django.db.models import FloatField, IntegerField
from django.db.models import Sum, F, Max, Min


# These are the view that display each page,


# Displaying all three tables in one main page
def MainPage(request):
    return render(request, 'Hockey_webPage.html',{'games': Game.objects.all(), 'items': Merchandise.objects.all(),
    'SoldItems': SoldItem.objects.all(), 'form': FilterForm})



# Display TotalSalePage
# Getting total sales of all items with Sum method
def TotalSalePage(request):
    return render(request, 'Total_Sale_webPage.html',SoldItem.objects.all().aggregate
                           (total_sales=Sum(F('merch__price')*F('numberSold'),output_field=FloatField())))




# Display BestSalePage
# First... get the best item sold amount and get the item name for displaying
def BestSalePage(request):

    BestSoldItem = SoldItem.objects.all().aggregate(best_sales=Max(F('numberSold'),output_field=IntegerField())).get('best_sales')

    return render(request, 'Best_Item_webPage.html',{'best_sales':BestSoldItem, 'items':SoldItem.objects.filter(numberSold=BestSoldItem)})




def LeastSoldPage(request):

    LeastSoldItem = SoldItem.objects.all().aggregate(least_sales=Min(F('numberSold'),output_field=IntegerField())).get('least_sales')

    return render(request, 'Least_Sold_webPage.html', {'least_sales':LeastSoldItem,'items':SoldItem.objects.filter(numberSold=LeastSoldItem)})




def GamePage(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            return render(request, 'Form_webPage.html',{'form': form})

    else:
        return render(request, 'Form_webPage.html',{'form': GameForm,'action':'/newgame/'})



def SoldItemPage(request):
    if request.method == 'POST':
        form = SoldItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            return render(request, 'Form_webPage.html',{'form': form})

    else:
        return render(request, 'Form_webPage.html',{'form': SoldItemForm,'action':'/solditem/'})





def NewItemPage(request):
    if request.method == 'POST': # if I clicked the submit button
        form = MerchandiseForm(request.POST)  # look at the form and see if the data type  is valid for to save it
        if form.is_valid():
            form.save()
            return redirect(to='/') # go to home page (local host 8000)
        else:
            return render(request, 'Form_webPage.html',{'form': form}) # display the error on the form when the data type is invalid


# if you click the link for a new item on the home page, display this form (/newitem/)
    else:
        return render(request, 'Form_webPage.html',{'form': MerchandiseForm,'action':'/newitem/'})







