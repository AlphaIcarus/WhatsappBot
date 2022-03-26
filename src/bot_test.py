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

from bot import WhatsappBot

class TestKnownPositiveFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are expected and positive.
    In other words, the testing where the user inputs are correct, wants to interact with the system
    and gives confirmation every time something is demanded.
    '''

    # confirm newsletter -> confirm giving email -> valid email given, 
    # and thus email stored and subscribed to newsletter -> end
    def test_full_newsletter(self):

        bot = WhatsappBot()

        

        pass


class TestKnownNegativeFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are unexpected but negative.
    In other words, the testing where the user inputs are correct but doesn't want to interact with the system,
    so he rejects something the system offers.
    '''

    def test_reject_newsletter(self):

        bot = WhatsappBot()
        pass

    def test_reject_giving_email(self):

        bot = WhatsappBot()
        pass

    def test_give_wrong_email(self):

        bot = WhatsappBot()
        pass

    ''' We put here the test for the ask_for_card motive '''

    def test_ask_for_card(self):

        bot = WhatsappBot()
        pass

class TestUnknownFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are nothing expected by the system.
    In other words, where the system is expecting for some possible answers (yes/no, confirm/reject, valid email/invalid email...)
    and the user gives an answer out of these possible (or doesn't give an answer at all) 
    '''

    def test_no_expected_answer_newsletter(self):

        bot = WhatsappBot()
        pass

    def test_no_expected_answer_email(self):

        bot = WhatsappBot()
        pass


''' 
Building test flow function. 

It returns a variable describing the workflow of the unittest execution
'''

def suite():

    #Creation of sequential tests
    suite = unittest.TestSuite()

    #Addition of test added in order
    #suite.addTest(Name_Of_Class('name_of_method'))

    ''' Known positive flow tests '''
    suite.addTest(TestKnownPositiveFlow('test_full_newsletter'))

    ''' Known negative flow tests '''
    suite.addTest(TestKnownNegativeFlow('test_reject_newsletter'))
    suite.addTest(TestKnownNegativeFlow('test_reject_giving_email'))
    suite.addTest(TestKnownNegativeFlow('test_give_wrong_email'))
    suite.addTest(TestKnownNegativeFlow('test_ask_for_card'))

    ''' Unknown flow tests '''
    suite.addTest(TestUnknownFlow('test_no_expected_answer_newsletter'))
    suite.addTest(TestUnknownFlow('test_no_expected_answer_email'))

    #Return of test flow variable
    return suite


''' Main function - Calling of Unittest '''

'''
if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(suite())

'''

# FULL TESTING

def main():

    my_bot = WhatsappBot(language='en')

    my_bot.message("Yes, I would like to receive notifications", "newsletter")


main()