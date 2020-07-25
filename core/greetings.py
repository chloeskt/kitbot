import abc
import re
from dialog import Dialog

class Greeting(Dialog):
    """
    Keeps track of the participants entering of leaving the conversation and responds with appropriate salutations.
    Rule based system which keeps track of state and uses regular expressions and logic to handle the dialog
    """

    PATTERNS = {
        "greeting": r'hello|hi|hey|good morning|good evening',
        'introduction': r"(?:my name is )|(?:I'm )([a-zA-Z\-\s]+)", #non capturing group
        #'introduction': r"my name is ([a-zA-Z\-\s]+)",
        #'introduction' : r"I'm ([a-zA-Z\-\s]+)",
        'goodbye': r'goodbye|bye|ttyl|see you|see you later',
        'rollcall': r'roll call|who\'s here?'
        }
    
    def __init__(self, participants=None):
        super().__init__()
        self.participants = {}
        if participants is not None: 
            for participant in participants:
                self.participants[participant] = None
        
        self._patterns = {
            key: re.compile(pattern, re.I)
            for key, pattern in self.PATTERNS.items()
        }

    def parse(self, text):
        """
        Applies regular expressions to find matches
        """
        matches = {}
        for key, pattern in self._patterns.items():
            match = pattern.match(text)
            if match is not None: 
                matches[key] = match
        return matches

    def interpret(self, sents, **kwargs):
        """
        Takes in parsed matches and determines if the message is an enter, exit or name change
        """
        if len(sents) == 0:
            return sents, 0.0, kwargs

        user = kwargs.get('user', None)

        if 'introduction' in sents:
            name = sents['introduction'].groups()[0]
            user = user or name.lower()

            if user not in self.participants or self.participants[user] != name:
                kwargs['name_changed'] = True 

            self.participants[user] = name 
            kwargs['user'] = user

        if 'greeting' in sents: 
            if not self.participants.get(user, None):
                kwargs['request_introduction'] = True 

        if 'goodbye' in sents and user is not None: 
            self.participants.pop(user)
            kwargs.pop('user', None)

        return sents, 1.0, kwargs

    def respond(self, sents, confidence, **kwargs):
        """
        Gives a greeting or a goodbye depending on what's appropriate
        """
        if confidence == 0:
            return None 

        name = self.participants.get(kwargs.get('user', None), None)
        name_changed = kwargs.get('name_changed', False)
        request_introduction = kwargs.get('request_introduction', False)

        if 'greeting' in sents or 'introduction' in sents:
            if request_introduction:
                return 'Hello, what is your name ? '
            else:
                return "Hello, {}!".format(name)

        if 'goodbye' in sents:
            return "Talk to you later !"

        if 'rollcall' in sents:
            people = list(self.participants.values())

            if len(people) > 1:
                roster = ", ".join(people[:-1])
                roster += " and {}".format(people[-1])
                return "Currently, in the conversation there are " + roster

            elif len(people) ==1:
                return "It's just you and me right now, {}".format(name)

            else: 
                return "So lonely right now ..., what who is that ?"

        #raise Exception(
        #    "expected response to be returned, but not could find rule"
        #)

if __name__ == "__main__":
    dialog = Greeting()
    print(dialog.listen("Hello!", user="chloeskt")[0])
    print(dialog.listen("I'm Chloe", user="chloeskt")[0])
    print(dialog.listen("Roll call!", user="chloeskt")[0])
    print(dialog.listen("Have to go, goodbye !", user="chloeskt")[0])