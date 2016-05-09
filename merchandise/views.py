from django.shortcuts import render
from merchandise.forms import MerchandiseForm, GameForm, SoldItemForm, FilterForm
from merchandise.models import Game, Merchandise, SoldItem
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import FloatField, IntegerField
from django.db.models import Sum, F, Max, Min

# For this Project 5, I got help from my classmate Boyd and Mason from the Learning Center for coding
# These are the view that display each page,


# Displaying all three tables in one main page
def MainPage(request):
    """
    Show all three database table and allow for sorting by ascending or descending order, for date sorting it sorts by
    date. Price sort by numbers and Team name is sorted by Alphabetically.

     See URL.py and check the code of 'url(r'^$',merch_views.MainPage, name='MainPage'), '

     See test.py  for class called 'class TestMainPageView(TestCase):' and method the test with this class.
     It has a method to test sorting, deleting all object types, test malicious user input


    :param request HTTP request:
    :return rendered template with context:
    """
    if request.method == "GET":

        # 'T' is made to use for ascending sort order
        # 't' is made to use for descending sort order
        # Every objects have a ascending and descending URL parameter

        game_query_dict = {'T': 'opponent', 't': '-opponent', 'GD': 'date', 'gd': '-date', 'HA': 'homeVSaway', 'ha': '-homeVSaway'}
        merchandise_query_dict = {'IN': 'name', 'in': '-name', 'P': 'price', 'p': '-price'}
        soldItem_query_dict = {'I': 'merch__name', 'i':'-merch__name', 'O': 'game__opponent', 'o': '-game__opponent', 'G': 'game__date',
                               'g': '-game__date', 'H': 'game__homeVSaway', 'h': '-game__homeVSaway', 'N': 'numberSold', 'n': '-numberSold'}


        # Setting the starting sorting order to ascending for every fields of the database
        TORt, GDORgd, HAORha, INORin, PORp, IORi, OORo, GORg, HORh, NORn = 'T', 'GD', 'HA', 'IN', 'P','I', 'O', 'G', 'H', 'N'

        Games = Game.objects.all()
        ItemsForSale = Merchandise.objects.all()
        ItemSold = SoldItem.objects.all()

        # Looking for 'Q' for the URL query parameter
        Query = request.GET.get("Q")
        if Query:

            game_limiter = game_query_dict.get(Query)

            if game_limiter:
                TORt = {'t':'T', 'T':'t'}
                GDORgd = {'GD': 'gd', 'gd': 'GD'}
                HAORha = {'HA': 'ha', 'ha': 'HA'}

                # order by either ascending or descending for opponent,date and homeVSaway
                Games = Games.order_by(game_limiter)

                # Sort by opposite, next time you click the up or down sort button
                TORt = TORt.get(Query) or 'T'
                GDORgd = GDORgd.get(Query) or 'GD'
                HAORha = HAORha.get(Query) or 'HA'


            merchandise_limiter = merchandise_query_dict.get(Query)

            if merchandise_limiter:

                INORin = {'IN': 'in', 'in': 'IN'}
                PORp = {'P': 'p', 'p': 'P'}

                ItemsForSale = ItemsForSale.order_by(merchandise_limiter)
                INORin = INORin.get(Query) or 'IN'
                PORp = PORp.get(Query) or 'P'


            soldItem_limiter = soldItem_query_dict.get(Query)

            if soldItem_limiter:

                IORi = {'I': 'i', 'i': 'I'}
                OORo = {'O': 'o', 'o': 'O'}
                GORg = {'G': 'g', 'g': 'G'}
                HORh = {'H': 'h', 'h': 'H'}
                NORn = {'N': 'n', 'n': 'N'}

                ItemSold = ItemSold.order_by(soldItem_limiter)
                IORi = IORi.get(Query) or 'I'
                OORo = OORo.get(Query) or 'O'
                GORg = GORg.get(Query) or 'G'
                HORh = HORh.get(Query) or 'H'
                NORn = NORn.get(Query) or 'N'



        # template out the HTML and return it
        return render(request, 'Hockey_webPage.html',{'games': Games, 'items': ItemsForSale,
        'SoldItems': ItemSold, 'form': FilterForm, 'TORt': TORt, 'GDORgd': GDORgd, 'HAORha': HAORha, 'INORin': INORin, 'PORp': PORp,
        'IORi': IORi, 'OORo': OORo, 'GORg': GORg, 'HORh': HORh, 'NORn': NORn})

    # Deleting the game, merchandise and sold item data from database by using the database id
    elif request.method == 'POST':
        game_ids = [int(i) for i in request.POST.getlist('gid[]')]
        merch_ids = [int(i) for i in request.POST.getlist('mid[]')]
        sold_ids = [int(i) for i in request.POST.getlist('sid[]')]

        if game_ids:
            Game.objects.filter(id__in=game_ids).delete()
        if merch_ids:
            Merchandise.objects.filter(id__in=merch_ids).delete()
        if sold_ids:
            SoldItem.objects.filter(id__in=sold_ids).delete()

        return HttpResponse('Success!')



# Display TotalSalePage
# Getting total sales by filtering either Item Name, Game Date or Opponent.
def TotalSalePage(request):

    # Getting the user data from the drop down list and check to see if the data is valid in the FilterForm
    form=FilterForm(request.GET)
    if form.is_valid():

        # Wrapping how the ORM  refer to the field name and how form refers to field name
        filter_attributes = (('merch__name','ItemName'),( 'game__date', 'GameDate'), ( 'game__opponent', 'Opponent'))

        # Only get the fields that has values in the request.GET dictionary
        resulting_form_attributes = [f for f in filter_attributes if request.GET.get(f[1])]

        # Creating empty dictionary for accumulating ORM fields with form values
        filter_dict = dict()


        for rfa in resulting_form_attributes:

            # It is getting the value of the select field and setting that as a value with key being the ORM field
            filter_dict[rfa[0]]=request.GET.get(rfa[1])

            # Unpack the filter dict and filter on the values
            # If total sales is none... display as zero
        return render(request, 'Total_Sale_webPage.html',{"total_sales": SoldItem.objects.filter(**filter_dict).aggregate
                           (total_sales=Sum(F('merch__price')*F('numberSold'),output_field=FloatField())).get("total_sales")or 0})

    # Display the main web page
    else:
        return render(request, 'Hockey_webPage.html',{'games': Game.objects.all(), 'items': Merchandise.objects.all(),
        'SoldItems': SoldItem.objects.all(), 'form': form})





# Display BestSalePage
# Getting the best sales item by filter choice of Item Name, Game Date and Opponent
def BestSalePage(request):

    """
    Getting the filter attributes from the drop down list of the item name, game date and game opponent.
    And from those attributes, calculate the best sale item one with most sold item

    :param request HTTP request:
    :return rendered HTML template:
    """
    form=FilterForm(request.GET)
    if form.is_valid():

        filter_attributes = (('merch__name', 'ItemName'), ('game__date', 'GameDate'), ('game__opponent', 'Opponent'))
        resulting_form_attributes = [f for f in filter_attributes if request.GET.get(f[1])]
        filter_dict = dict()
        for rfa in resulting_form_attributes:
            filter_dict[rfa[0]]=request.GET.get(rfa[1])

        BestSoldItem = SoldItem.objects.filter(**filter_dict).aggregate(best_sales=Max(F('numberSold'),output_field=IntegerField())).get('best_sales')or 0

        return render(request, 'Best_Item_webPage.html',{'best_sales':BestSoldItem, 'items':SoldItem.objects.filter(numberSold=BestSoldItem, **filter_dict)})


    else:
         return render(request, 'Hockey_webPage.html',{'games': Game.objects.all(), 'items': Merchandise.objects.all(),
        'SoldItems': SoldItem.objects.all(), 'form': form})





def LeastSoldPage(request):

    """
    Getting the filter attributes from the drop down list of the item name, game date and game opponent.
    And from those attributes, calculate the least sold item one with least sold item

    :param request HTTP request:
    :return rendered HTML template:
    """


    form=FilterForm(request.GET)
    if form.is_valid():

        filter_attributes = (('merch__name', 'ItemName'), ('game__date', 'GameDate'), ('game__opponent', 'Opponent'))
        resulting_form_attributes = [f for f in filter_attributes if request.GET.get(f[1])]
        filter_dict = dict()
        for rfa in resulting_form_attributes:
            filter_dict[rfa[0]]=request.GET.get(rfa[1])

        LeastSoldItem = SoldItem.objects.filter(**filter_dict).aggregate(least_sales=Min(F('numberSold'),output_field=IntegerField())).get('least_sales')or 0

        return render(request, 'Least_Sold_webPage.html', {'least_sales':LeastSoldItem,'items':SoldItem.objects.filter(numberSold=LeastSoldItem, **filter_dict)})

    else:
         return render(request, 'Hockey_webPage.html',{'games': Game.objects.all(), 'items': Merchandise.objects.all(),
        'SoldItems': SoldItem.objects.all(), 'form': form})





def GamePage(request):

    """
    New game form page uses Form_webPage.html template and GameForm model form

    :param request HTTP request:
    :return rendered HTML template or redirect:
    """

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid(): # If the user input data is valid then save the data to database
            form.save()
            return redirect(to='/')  # Redirect to the MainPage
        else:
            return render(request, 'Form_webPage.html',{'form': form}) # Re-render the template with form now with errors

    else:

        # If the request is a GET request, then return a form in the render template
        return render(request, 'Form_webPage.html',{'form': GameForm,'action':'/newgame/'})



def SoldItemPage(request):

    """
    Sold Item form page uses Form_webPage.html template and SoldItemForm model form

    :param request HTTP request:
    :return rendered HTML template or redirect:
    """
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

    """
    New item form page uses Form_webPage.html template and MerchandiseForm model form

    :param request HTTP request:
    :return rendered HTML template or redirect:
    """
    if request.method == 'POST':  # if I clicked the submit button
        form = MerchandiseForm(request.POST)  # look at the form and see if the data type  is valid for to save it
        if form.is_valid():
            form.save()
            return redirect(to='/')  # go to home page (local host 8000)
        else:
            return render(request, 'Form_webPage.html',{'form': form}) # display the error on the form when the data type is invalid


# if you click the link for a new item on the home page, display this form (/newitem/)
    else:
        return render(request, 'Form_webPage.html',{'form': MerchandiseForm,'action':'/newitem/'})







