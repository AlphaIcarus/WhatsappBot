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
    This class defines the testing on the user cases where the inputs are expected and positive.
    In other words, the testing where the user inputs are correct, wants to interact with the system
    and gives confirmation every time something is demanded.
    '''

    def test_full_newsletter(self):
        pass


class TestKnownNegativeFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are unexpected but negative.
    In other words, the testing where the user inputs are correct but doesn't want to interact with the system,
    so he rejects something the system offers.
    '''

    def test_reject_newsletter(self):
        pass

    def test_reject_giving_email(self):
        pass

    def test_give_wrong_email(self):
        pass

    ''' We put here the test for the ask_for_card motive '''

    def test_ask_for_card(self):
        pass

class TestUnknownFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are nothing expected by the system.
    In other words, where the system is expecting for some possible answers (yes/no, confirm/reject, valid email/invalid email...)
    and the user gives an answer out of these possible (or doesn't give an answer at all) 
    '''

    def test_no_expected_answer_newsletter(self):
        pass

    def test_no_expected_answer_email(self):
        pass
