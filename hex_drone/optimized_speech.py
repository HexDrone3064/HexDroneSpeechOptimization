"""
⬡-Drone's speech which limited to the status codes by 'Speech Optimization'.
"""

import re
from status_codes import status_codes
from typing import Optional, Sequence


class OptimizedSpeech:
    """
    A speech which limited to the status code.
    """
    
    def __init__(
            self,
            drone_id: str, status_code: str, status_message: str,
            predefined_message: Optional[str], user_defined_messages: Sequence[str]
    ):
        """
        Instantiate OptimizedSpeech object.
        
        :param drone_id: 4 digit of ⬡-Drone ID.
        :param status_code: 3 digit of ⬡-Drone status code.
        :param status_message: A message indicating the classification of the status code.
        :param predefined_message: A message describing the status code.
        :param user_defined_messages: Massages defined by user.
        """
        self.drone_id = drone_id
        self.status_code = status_code
        self.status_message = status_message
        self.predefined_message = predefined_message
        self.user_defined_messages = list(user_defined_messages)
    
    def __str__(self):
        v = [
            self.drone_id, f'Code {self.status_code}', self.status_message,
            self.predefined_message, *self.user_defined_messages
        ]
        v = list(filter(lambda x: x is not None, v))
        return ' :: '.join(v)
    
    def __repr__(self):
        v = [
            self.drone_id, self.status_code, self.status_message,
            self.predefined_message, self.user_defined_messages
        ]
        v = list(map(lambda x: repr(x), v))
        v = ', '.join(v)
        return f"OptimizedSpeech({v})"
    
    def __eq__(self, other):
        if not isinstance(other, OptimizedSpeech):
            return None
        return \
            self.drone_id == other.drone_id and \
            self.status_code == other.status_code and \
            self.status_message == other.status_message and \
            self.predefined_message == other.predefined_message and \
            self.user_defined_messages == other.user_defined_messages
    
    @classmethod
    def parse(cls, speech: str):
        """
        Parse str to OptimizedSpeech.
        
        :param speech: Speech to parse.
        :return: Return None if speech is invalid.
        """
        tokens = speech.split(' :: ')
        if len(tokens) < 2:
            return None  # Too few tokens.

        drone_id = tokens.pop(0)
        if not re.match(r'^\d{4}$', drone_id):
            return None  # Drone ID's format is invalid.
        
        match = re.match(r'^Code (?P<CODE>\d{3})$', tokens.pop(0))
        if match is None:
            return None  # Status code's format is invalid.
        status_code = match.group('CODE')
        data = status_codes.get(status_code, None)
        if data is None:
            return None  # Status code is invalid.
        
        while len(tokens) > 0 and tokens[0] in [data.status_message, data.predefined_message]:
            tokens.pop(0)  # Remaining tokens are drone-defined string.
            
        return OptimizedSpeech(
            drone_id, status_code, data.status_message,
            data.predefined_message, tokens
        )
    
    @classmethod
    def build(cls, drone_id: str, status_code: str, *user_defined_messages: str):
        """
        Build OptimizedSpeech.
        
        :param drone_id: 4 digit of ⬡-Drone ID.
        :param status_code: 3 digit of ⬡-Drone status code.
        :param user_defined_messages: Massages defined by user.
        :return: Return None if no such status code exists.
        """
        data = status_codes.get(status_code)
        if data is None:
            return None
        
        return OptimizedSpeech(
            drone_id, status_code, data.status_message,
            data.predefined_message, user_defined_messages
        )
