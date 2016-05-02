# Hockey Inventory App


## Key feature

- Sorting by ascending and descending on any attributes on any model.

- Delete the row from the database by using checkbox

- Drop down list of filterable attributes for Total sales button, Best sale button and Least sale button


## Test

 Testing for how many lines of code were tested in each file.

 Below are the test coverage report for integration test from the terminal.
 From terminal, first I typed "python manage.py test" and click enter.
 Then I typed "coverage run manage.py test" and click enter.
 And I typed "coverage report" and click enter and this test coverage report displayed on terminal
 

(myvenv) C:\Users\Jessy\PycharmProjects\Project 5>coverage report
Name                                                Stmts   Miss  Cover
-----------------------------------------------------------------------
hockeyInventory\__init__.py                             0      0   100%
hockeyInventory\settings.py                            18      0   100%
hockeyInventory\urls.py                                 4      0   100%
manage.py                                               6      0   100%
merchandise\__init__.py                                 0      0   100%
merchandise\admin.py                                    3      0   100%
merchandise\forms.py                                   28      0   100%
merchandise\migrations\0001_initial.py                  7      0   100%
merchandise\migrations\0002_auto_20160401_1210.py       5      0   100%
merchandise\migrations\__init__.py                      0      0   100%
merchandise\models.py                                  17      2    88%
merchandise\tests.py                                   69      0   100%
merchandise\views.py                                  117     67    43%
-----------------------------------------------------------------------
TOTAL                                                 274     69    75%


