'''
This file will have all the different classes, one for each test, that will implement the different user interactions with the bot.

We want to define an important ammount of possible interactions from user to bot and bot to user, in order to test them and see how the
bot behaves.
'''

'''
COSAS QUE FALTAN POR HACER:

    - Implementación de la clase:
        * TestKnownPositiveFlow
        * TestKnownNegativeFlow
        * TestUknownFlow
    - Comentarios de la clase:
        * TestKnownNegativeFlow
        * TestUnknownFlow

'''

# Modules and frameworks

import unittest

# Classes from local file system

class TestKnownPositiveFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the outputs are expected and positive.
    In other words, the testing where the user inputs are correct, wants to interact with the system
    and gives confirmation every time something is demanded.

    We have three user cases where this happens:

        - Newsletter confirmation.
        - Giving email confirmation.
        - Valid email given.

    Every one of them is dependent from the one before (except the first one), and because of that we're goint to test them all together.
    '''

    def test_full_newsletter(self):
        pass


class TestKnownNegativeFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the outputs are unexpected but negative.
    In other words, the testing where the user inputs are correct but doesn't want to interact with the system,
    so he rejects every single thing the system offers.

    We have INSERT_NUMBER_OF_CASES user cases where this happens:

        - 

    We are going to test every user case separatedly, and then some of them together, in specific order of flow.
    '''


class TestUnknownFlow(unittest.TestCase):

