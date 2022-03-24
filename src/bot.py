import re
from typing import Any, Dict, Match, Optional, Tuple

from api import BooklineAPI, InsertEmailError
from classifier import Classifier


class WhatsappBot:

    LANGUAGES = ["es", "en"]

    def __init__(self, language: str = "es") -> None:
        """Initialise attributes."""
        if language not in self.LANGUAGES:
            raise ValueError(f"Language {language} not available.")
        else:
            self.language = language
        self.conversation_status: str = "start"
        self.bookline_api = BooklineAPI()
        self.classifier = Classifier(self.language)

    def _validate_email(self, email: str) -> Match:
        """Return a regex email Match."""
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def _get_intent(self, query: str) -> str:
        """Given a user query, return the identified intent."""
        return self.classifier.extract_intent(query)

    def _newsletter_flow(self, intent: str, query: str) -> Tuple[str, Dict[str, str], Optional[str]]:
        """Return next action, answer dictionary and retrieved email."""
        email = None
        next_action = "continue"

        # Initial message from us was:
        # Please confirm that you wish to receive additional info via subscription to our newsletter.
        if self.conversation_status == "start":
            if intent == "confirm":
                self.conversation_status = "expectingEmail"
                answer = {
                    "es": "¡Genial! Por favor, indícame tu correo electrónico",
                    "en": "Great! Please, let me know your e-mail",
                }
            elif intent == "reject":
                next_action = "hangup"
                self.conversation_status = "hangup"
                answer = {
                    "es": "De acuerdo, espero que disfrutes de la experiencia en el restaurante. ¡Hasta pronto!",
                    "en": "Okay, I hope you enjoy the experience at the restaurant",
                }
            else:
                answer = {
                    "es": "Por favor, dime si confirmas o no",
                    "en": "Please, let me know if you agree or not",
                }
        # User has agreed to provide email
        elif self.conversation_status == "expectingEmail":
            if intent == "reject":
                self.conversation_status = "hangup"
                answer = {
                    "es": "De acuerdo, espero que disfrutes de la experiencia en el restaurante. ¡Hasta pronto!",
                    "en": "Okay, I hope you enjoy the experience at the restaurant",
                }
            elif intent == "confirm":
                answer = {
                    "es": "¡Genial! Por favor, indícame tu correo electrónico",
                    "en": "Great! Please, let me know your e-mail",
                }
            else:
                if self._validate_email(query.strip()):
                    email = self._validate_email(query.strip()).string
                    self.conversation_status = "hangup"
                    answer = {
                        "es": "¡Perfecto, hemos guardado tu e-mail! Disfruta de la experiencia en el restaurante.",
                        "en": "Perfect, we've stored your e-mail! Enjoy the experience at the restaurant",
                    }
                else:
                    answer = {
                        "es": "Este e-mail no parece válido. Por favor, revisalo de nuevo",
                        "en": "It seems that this e-mail is not valid. Please make sure it's correct",
                    }
        elif self.conversation_status == "hangup":
            next_action = "hangup"
            answer = {
                "es": "¡Gracias por contactar con nosotros! Todavía no puedo ayudarte en nada más pero si quieres hacer una reserva llama al restaurante otra vez",
                "en": "Thanks for reaching out. I can't help you with anything else yet but if you want to make a reservation you can call the restaurant again",
            }
        else:
            next_action = "hangup"
            answer = {
                "es": "¡Gracias por contactar con nosotros! Todavía no puedo ayudarte en nada más pero si quieres hacer una reserva llama al restaurante otra vez",
                "en": "Thanks for reaching out. I can't help you with anything else yet but if you want to make a reservation you can call the restaurant again",
            }

        return (next_action, answer, email)

    def _ask_for_email_flow(self, intent: str, query: str) -> Tuple[str, Dict[str, str], Optional[str]]:
        """Return next action, answer dictionary and retrieved email."""
        email = None
        next_action = "continue"

        # These conversations always start with expecting email status
        if self.conversation_status == "start":
            self.conversation_status = "expectingEmail"

        if self.conversation_status != "hangup":
            if self._validate_email(query.strip()):
                email = self._validate_email(query.strip()).string
                self.conversation_status = "hangup"
                answer = {
                    "es": "¡Perfecto, hemos guardado tu e-mail! Disfruta de la experiencia en el restaurante.",
                    "en": "Perfect, we've stored your e-mail! Enjoy the experience at the restaurant",
                }
            else:
                answer = {
                    "es": "Este e-mail no parece válido. Por favor, revisalo de nuevo",
                    "en": "It seems that this e-mail is not valid. Please make sure it's correct",
                }
        else:
            next_action = "hangup"
            answer = {
                "es": "¡Gracias por contactar con nosotros! Todavía no puedo ayudarte en nada más pero si quieres hacer una reserva llama al restaurante otra vez",
                "en": "Thanks for reaching out. I can't help you with anything else yet but if you want to make a reservation you can call the restaurant again",
            }

        return (next_action, answer, email)

    def _ask_for_card_flow(self, intent: str, query: str) -> Tuple[str, Dict[str, str], Optional[str]]:
        """Return next action, answer dictionary and retrieved email."""
        email = None
        next_action = "hangup"
        answer = {
            "es": "¡Gracias por contactar con nosotros! Todavía no puedo ayudarte en nada más pero si quieres hacer una reserva llama al restaurante otra vez",
            "en": "Thanks for reaching out. I can't help you with anything else yet but if you want to make a reservation you can call the restaurant again",
        }

        return (next_action, answer, email)

    def message(self, query: str, motive: str) -> Dict[str, Any]:

        # 1 - Get intent
        intent = self._get_intent(query)

        # 2 - Process query-intent
        if motive == "newsletter":
            next_action, answer, email = self._newsletter_flow(intent, query)
        elif motive == "ask_for_email":
            next_action, answer, email = self._ask_for_email_flow(intent, query)
        elif motive == "ask_for_card":
            next_action, answer, email = self._ask_for_card_flow(intent, query)
        
        # 3 - Insert email if we have retrieved it
        if email:
            try:
                self.bookline_api.insert_customer_email(email)
            except InsertEmailError:
                answer = {
                    "es": "Ha habido un error. Inténtelo de nuevo más tarde.",
                    "en": "There has been an error. Please try again later."
                }
                next_action = "hangup"

        # 4 - Build and return JSON response
        resp = {
            "answer": {
                "id": 0,
                "message": answer[self.language],
            },
            "action": next_action
        }
        return resp
