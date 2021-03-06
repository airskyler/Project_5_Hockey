from django.test import TestCase, Client
from merchandise.models import Merchandise, Game, SoldItem
from django.core.urlresolvers import reverse



class TestMainPageView(TestCase):

    def setUp(self):
        """ creating objects here to use these objects for testing the method main page"""

        self.Red_wings = Game.objects.create(opponent='Red Wings', date='2016-01-18', homeVSaway='H')
        self.Canadiens = Game.objects.create(opponent='Canadiens', date='2015-11-27', homeVSaway='A')
        self.Oilers = Game.objects.create(opponent='Oilers', date='2015-10-18', homeVSaway='A')



        self.Jersey = Merchandise.objects.create(name='Jersey', price=20.0)
        self.Poster = Merchandise.objects.create(name='Poster', price=10.5)
        self.Shot_Glass = Merchandise.objects.create(name='Shot Glass', price= 7.77)
        self.Cup = Merchandise.objects.create(name='Cup', price=1.50)
        self.Ice = Merchandise.objects.create(name='Ice', price=5.07)


        self.soldJersey = SoldItem.objects.create(merch=self.Jersey, game=self.Red_wings, numberSold=108)
        self.soldPoster = SoldItem.objects.create(merch=self.Poster, game=self.Canadiens, numberSold=7)
        self.soldShotGlass = SoldItem.objects.create(merch=self.Shot_Glass, game=self.Oilers, numberSold=24)
        self.soldCup = SoldItem.objects.create(merch=self.Cup, game=self.Red_wings, numberSold=5)
        self.soldIce = SoldItem.objects.create(merch=self.Ice, game=self.Oilers, numberSold=70)


    def test_NoParameters(self):
        """test for game opponent in game context with default sorting"""

        client = Client() # helper class for making request thru Django web frame work for testing
        response = client.get(reverse('MainPage')) # get a response from a MainPage method
        games = response.context.get('games') # getting the context of game data

        # testing that these team are in the game table
        self.assertIn(self.Canadiens, games, "Canadiens are in the games in the context passed to the template")
        self.assertIn(self.Oilers, games, "Oilers are in the games in the context passed to the template")
        self.assertIn(self.Red_wings, games, "Red Wings are in the games in the context passed to the template")

        # TODO test whether Merchandise objects and SoldItem objects are in the context.



    def test_delete_each_type(self):
        """Test that each type of object Merchandise, Games, and SoldItems can be deleted by posting the array of
        id's to MainPage"""

        client = Client()

        # 'gid[]' is game id array for deleting one or more games at same time

        # Giving Canadians game id to the backend (server) to delete
        response1 = client.post(reverse('MainPage'),{'gid[]':[self.Canadiens.id]})
        self.assertEqual(response1.status_code, 200, "Posting is working.")

        # the code of (reverse('MainPage')) is getting the URL path for the MainPage name
        # 'client.get' is a code fake URL request for testing
        response2 = client.get(reverse('MainPage'))
        games = response2.context.get('games')

        # testing if there is 2 team left in the game table
        self.assertTrue(len(games)==2, "Now there are only two Games, we have deleted the Canadiens")

        # testing No Canadians team are in the game table
        self.assertNotIn(self.Canadiens, games, "No Canadiens")


        # sending the id's for Ice and Jersey to the backend for deleting
        # 'client.post' code is sending the id's for the merchandise to the MainPage view, which deletes them
        # from the merchandise table
        response3 = client.post(reverse('MainPage'), {'mid[]': [self.Ice.id, self.Jersey.id]})
        self.assertEqual(response3.status_code, 200, "Posting still working")

        response4 = client.get(reverse('MainPage'))
        merchandise = response4.context.get('items')
        self.assertNotIn(self.Ice, merchandise, "No more Ice.")
        self.assertNotIn(self.Jersey, merchandise, "The jersey is gone.")
        self.assertIn(self.Cup, merchandise, "The cup is still there.")

        # have to be careful since SoldItems depend on Games and Merchandise, we have gotten rid of some SoldItems
        # From a quick scan only 2 SoldItems are left, we'll get rid of both of them

        preSoldItems = response4.context.get('SoldItems')
        self.assertEqual(len(preSoldItems), 2, "There are only two SoldItems now")

        client.post(reverse('MainPage'), {'sid[]': [self.soldCup.id, self.soldShotGlass.id]})
        postSoldItems = client.get(reverse('MainPage')).context.get('SoldItems')
        self.assertTrue(len(postSoldItems)==0, "No SoldItems are left.")

    def test_sorting_games(self):
        """Sorting by each of the url parameters T:t (opponent or -opponent), GD:gd (date or -date)... see views.py"""


        client = Client()

        # 'Q' is a URL parameter for querying
        # everything that comes after the '?' (Question mark) is a URL parameter

        # testing if the opponent will sort in ascending order
        response = client.get(reverse('MainPage')+'?Q=T')
        games = response.context.get('games')

        # checking if the team order is in alphabetical
        the_correct_order = [self.Canadiens, self.Oilers, self.Red_wings]


        # g is for games. c is for the_correct_order
        # checking each of the game is in correct order
        for g, c in zip(games, the_correct_order):
            self.assertEqual(g,c, "Each Game is in the correct alphabetical order by opponent name")

        # testing if the opponent will sort in descending order
        desc_games = client.get(reverse('MainPage')+'?Q=t').context.get('games')
        # Now it is descending

        # reversing the opponent order
        the_correct_order.reverse()
        for g, c in zip(desc_games, the_correct_order):
            self.assertEqual(g, c, "Each game is in the correct desc alphabetical order by opponent name.")


        # testing the game dates for each team by ascending date order
        games_by_date = client.get(reverse('MainPage')+'?Q=GD').context.get('games')
        the_correct_order = [self.Oilers, self.Canadiens, self.Red_wings]

        for g, c in zip(games_by_date, the_correct_order):
            self.assertEqual(g, c, "Each game is in the correct order by date. Earliest to latest")


        # testing the game date for each team by descending order
        games_by_date_latest_to_earliest = client.get(reverse('MainPage')+'?Q=gd').context.get('games')
        the_correct_order.reverse()
        for g, c in zip(games_by_date_latest_to_earliest, the_correct_order):
            self.assertEqual(g, c, "Each game is in latest to earliest order by date.")


        # TODO write homeVSaway test. first that the Aways are first then the Homes

    # TODO write more ordering/sorting tests



    def test_fuzz(self):
        """This tests that the MainPage view will only look for certain parameters and if they aren't there or are
        replaced by something else, it won't error."""
        client = Client()

        # giving the server a bad URL parameter
        # but it doesn't have a server error , so it is design well
        malicious_junk = ['zzz', 'z', 'u', 'UUUUi']
        for mal in malicious_junk:
            self.assertEqual(client.get(reverse("MainPage")+'?Q='+mal).status_code, 200, "Can't cause the server to error.")



