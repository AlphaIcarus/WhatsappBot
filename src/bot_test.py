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

    - Resulta que el flujo de las conversaciones no era como yo creía, así que falta poner
      métodos para el flujo de conversación de tipo ask_for_email

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

    # confirm newsletter -> valid email given, and thus email stored and subscribed to newsletter -> end

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_full_newsletter(self, mock1, mock2):

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

    # give email when ask_for_email -> valid email given and stored -> end

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_full_email(self, mock1, mock2):

        bot = WhatsappBot('en')
        response = None

        #Flux of the program
        response = bot.message("validemail@gmail.com", "ask_for_email")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "Perfect, we've stored your e-mail! Enjoy the experience at the restaurant")
        self.assertEqual(response["action"], 'hangup')


class TestKnownNegativeFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are unexpected but negative.
    In other words, the testing where the user inputs are correct but doesn't want to interact with the system,
    so he rejects something the system offers.
    '''

    # reject newsletter -> end

    @mock.patch('classifier.Classifier.extract_intent', return_value='reject')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_reject_newsletter(self,mock1, mock2):

        bot = WhatsappBot('en')

        #Flux of the program
        response = bot.message('I do not want to subscribe to the newsletter', 'newsletter')
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], 'Okay, I hope you enjoy the experience at the restaurant')
        self.assertEqual(response["action"], 'hangout')

        pass

    # confirm newsletter -> give wrong email (format) -> end

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_wrong_email(self, mock1, mock2):

        bot = WhatsappBot('en')

        #Flux of the program
        response = bot.message("Yes, I would like to receive notifications", "newsletter")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], 'Great! Please, let me know your e-mail')
        self.assertEqual(response["action"], 'continue')

        with mock.patch('classifier.Classifier.extract_intent', return_value='other'):
            response = bot.message("I'm not a valid email", "newsletter")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "It seems that this e-mail is not valid. Please make sure it's correct")
        self.assertEqual(response["action"], 'hangup')

        pass

    # give wrong emil when ask_for_email -> wrong email given, try again -> start again

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_wrong_email_ask_for_email(self, mock1, mock2):

        bot = WhatsappBot('en')

        #Flux of the program
        response = bot.message("I'm not a valid email", "ask_for_email")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "It seems that this e-mail is not valid. Please make sure it's correct")
        self.assertEqual(response["action"], 'continue')

        # Here we would have to insert the email making sure the format is correct -> recurssive definition
        pass

    # give valid email when ask_for_email -> valid email given and stored -> give email once again -> error -> end 

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_valid_email_then_wrong_email(self, mock1, mock2):

        bot = WhatsappBot('en')

        #Flux of the program
        response = bot.message("validemail@gmail.com", "ask_for_email")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "Perfect, we've stored your e-mail! Enjoy the experience at the restaurant")
        self.assertEqual(response["action"], 'hangup')

        response = bot.message("I'm not a valid email", "ask_for_email")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "Thanks for reaching out. I can't help you with anything else yet but if you want to make a reservation you can call the restaurant again")
        self.assertEqual(response["action"], 'hangup')

    ''' We put here the test for the ask_for_card motive '''

    # give card -> end 

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_ask_for_card(self, mock1, mock2):

        bot = WhatsappBot('en')

        #Flux of the program
        response = bot.message("I want to give my card", "ask_for_card")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "Thanks for reaching out. I can't help you with anything else yet but if you want to make a reservation you can call the restaurant again")
        self.assertEqual(response["action"], 'hangup')

        pass

class TestUnknownFlow(unittest.TestCase):

    '''
    This class defines the testing on the user cases where the inputs are nothing expected by the system.
    In other words, where the system is expecting for some possible answers (yes/no, confirm/reject, valid email/invalid email...)
    and the user gives an answer out of these possible (or doesn't give an answer at all) 
    '''

    # wrong answer to asking for newsletter-> end?*

    @mock.patch('classifier.Classifier.extract_intent', return_value='non_deterministic_response')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_no_expected_answer_newsletter(self, mock1, mock2):

        bot = WhatsappBot('en')

        response = bot.message("I neither confirm nor reject my newsletter subscription", "newsletter")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "Thanks for reaching out. I can't help you with anything else yet but if you want to make a reservation you can call the restaurant again")
        self.assertEqual(response["action"], 'hangup')

        pass

    # confirm newsletter -> wrong email format (random input) -> end?*

    @mock.patch('classifier.Classifier.extract_intent', return_value='confirm')
    @mock.patch('api.BooklineAPI.insert_customer_email', return_value='okey')
    def test_no_expected_answer_email_request(self, mock1, mock2):

        bot = WhatsappBot('en')

        #Flux of the program
        response = bot.message("Yes, I would like to receive notifications", "newsletter")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], 'Great! Please, let me know your e-mail')
        self.assertEqual(response["action"], 'continue')

        response = bot.message("I do not insert a valid email format","newsletter")
        self.assertEqual(response["id"], 0)
        self.assertEqual(response["message"], "It seems that this e-mail is not valid. Please make sure it's correct")
        self.assertEqual(response["action"], 'hangup')

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
    suite.addTest(TestKnownPositiveFlow('test_full_email'))

    ''' Known negative flow tests '''
    suite.addTest(TestKnownNegativeFlow('test_reject_newsletter'))
    suite.addTest(TestKnownNegativeFlow('test_wrong_email'))
    suite.addTest(TestKnownNegativeFlow('test_ask_for_card'))
    suite.addTest(TestKnownNegativeFlow('test_valid_email_then_wrong_email'))
    suite.addTest(TestKnownNegativeFlow('test_wrong_email_ask_for_email'))



    ''' Unknown flow tests '''
    suite.addTest(TestUnknownFlow('test_no_expected_answer_newsletter'))
    suite.addTest(TestUnknownFlow('test_no_expected_answer_email_request'))

    #Return of test flow variable
    return suite

''' Main function - Calling of Unittest '''

if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(suite())












# FULL TESTING

'''
Notas:

    - El decorador mock a efectos prácticos es como un atributo que le pasas por parámetro, así que necesitas definirle una
    variable asociada a cada decorador
'''

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

'''