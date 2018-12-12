"""Test for my functions.
	
	Test whether "exchange programs.csv" exists or not.

"""


def test_my_func():

    import os.path
    assert(os.path.isfile("exchange programs.csv") )==True

    



