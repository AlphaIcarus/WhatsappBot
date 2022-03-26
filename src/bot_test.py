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

from typing import Any, Dict
import unittest
from unittest import mock

# Classes from local file system

from bot import WhatsappBot
#from classifier import Classifier
#from api import BooklineAPI

''' 
Every output is fo the form:

    {'answer': {'id': 0, 'message': 'Great! Please, let me know your e-mail'}, 'action': 'continue'}

    Where answer -> Dict, id -> int, message -> str, action -> string

'''

class TestKnownPositiveFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are expected and positive.
    In other words, the testing where the user inputs are correct, wants to interact with the system
    and gives confirmation every time something is demanded.
    '''

    # confirm newsletter -> confirm giving email -> valid email given, 
    # and thus email stored and subscribed to newsletter -> end

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_full_newsletter(self):

        bot = WhatsappBot('en')
        response = None

        #Flux of the program
        response = bot.message("Yes, I would like to receive notifications", "newsletter")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], 'Great! Please, let me know your e-mail')
        self.assertEqual(response["action"], 'continue')

        with mock.patch('classifier.Classifier.extract_intent', return_value='other'):
            response = bot.message("abc@email.com", "newsletter")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "Perfect, we've stored your e-mail! Enjoy the experience at the restaurant")
        self.assertEqual(response["action"], 'hangout')
        
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

'''
Notes:

    - El decorador mock a efectos prácticos es como un atributo que le pasas por parámetro, así que necesitas definirle una
    variable asociada a cada decorador
'''

class Testing(unittest.TestCase):

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value=True)
    def main(self, mock_check_output_1, mock_check_output_2):

        my_bot = WhatsappBot()

        #Flux of the program

        response = my_bot.message("Yes, I would like to receive notifications", "newsletter")  # bot status changes to expectingEmail
        print(str(response['answer']['id']) + ', ' + str(response['answer']['message']) + ', ' + str(response['action']))

        with mock.patch('classifier.Classifier.extract_intent', return_value='other'): 
            response = my_bot.message("abc@email.com", "newsletter")  # valid email, bot inserts email and sends hangup
        print(str(response['answer']['id']) + ', ' + str(response['answer']['message']) + ', ' + str(response['action']))

        pass


# Execution of the testing program

testing = Testing()
testing.main()