# Code description and Relevant information

## Repository Structure

This repository has a single folder `src` with four files:

- api.py
- bot.py
- classifier.py
- main.py

### api.py

Defines class `BooklineAPI` with unimplemented public method `insert_customer_email`.  
Defines error `InsertEmailError`.

### classifier.py

Defines class `Classifier` with unimplemented public method `get_intent`.

### bot.py

Defines class `WhatsappBot` with public method `message`.  
`WhatsappBot` uses both `Classifier` and `BooklineAPI`.  
`WhatsappBot` also has several private methods used by `message`.

### main.py

Provides examples of how to use `WhatsappBot` to manage conversations.

## WhatsappBot conversation flow

When Bookline receives a new Whatsapp message, it creates a `WhatsappBot` instance to manage this new conversation.  
A new `WhatsappBot` starts with `conversation_status = "start"`.   

A conversation is handled by `WhatsappBot` as a sequence of interactions.
Interactions are independent from each other, and the only variable that is stored from one interaction to the next
is the `conversation_status`. 

### Input

An interaction is passed to `WhatsappBot` via a call to its `message` method - by providing two strings: the user query
and the conversation motive. **All interactions from the same conversation share the same motive.**

### Conversation Flow

According to the conversation motive, `WhatsappBot.message` handles the user query with a proper conversation flow.
There are currently three conversation motives, each of them with its correspondent flow:

1. *newsletter* - the conversation starts when a user replies to an automatic message from Bookline asking if they wish to receive
updates via a newsletter subscription. If the user confirms their interest, the bot asks for an email address.
2. *ask_for_email* - the conversation starts when a user replies to an automatic message from Bookline asking for an email address
3. *ask_for_card* - this conversation flow is not implemented yet, so any conversation started with this motive triggers
a hangup reply from the bot  

### Output

`WhatsappBot` provides a response to query in the form of a `JSON` with an answer
(consisting of an id and a string) and a next action to perform.  
This output will be then handled by another service.

The bot continues to process interactions until it decides to send out a **hangup** response.  
At that time the `WhatsappBot` is destroyed and the conversation ends.

# Task

Your task is to plan and implement a test structure to ensure that `WhatsappBot` behaves correctly when handling
a few default conversations, as well as achieving a high degree of code coverage. To do that, you will need to

1. **Plan the tests**
    - By looking at the code, write down sample conversations that you consider should be implemented as tests in order to achieve a high degree of coverage of `WhatsappBot`
    - `main.py` has five examples of how a conversation might start, as well as an example of a full conversation (only the user input)
2. **Implement the tests**
    - Using unittest, implement one or more of your full-conversation tests
    - You will need to mock calls to `Classifier` and `BooklineAPI` methods - methods for these classes are not implemented,
    so we need to mock them in order to perform the tests.
3. **(Optional) Suggest improvements to the code of `WhatsappBot`**
    - In case you see something that you consider could/should be improved, feel free to point it out!