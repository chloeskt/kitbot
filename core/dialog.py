import abc

class Dialog(abc.ABC):
    """
    a dialog listens for utterances, parses and interprets them, then updates its internal state. It can formulate a response on demand.
    """

    def __init__(self):
        super().__init__()

    def listen(self, text, response=True, **kwargs):
        """
        A text utterance is passed in and parsed. it is then passed to the interpret method to determine how to respond. 
        If a response is requested, the respond method is used to generate a text response based on the most recent input and the current Dialog state.
        """
        sents = self.parse(text)
        sents, confidence, kwargs = self.interpret(sents, **kwargs)
        if response: 
            reply = self.respond(sents, confidence, **kwargs)
        else:
            reply = None 

        return reply, confidence

    @abc.abstractmethod
    def parse(self, text):
        """
        Parsing strategy
        """
        return []

    @abc.abstractmethod
    def interpret(self, sents, **kwargs):
        """
        Interprets the utterance passed in as a list of parsed sentences, updates the internal state of the dialog, 
        computes a confidence of the interpretation 
        """
        return sents, 0.0, kwargs

    @abc.abstractmethod
    def respond(self, sents, confidence, **kwargs):
        """
        Creates a response given the input utterances and the current state of the dialog, along with any arguments passed in from the listen 
        or the interpret methods
        """
        return None
    
    