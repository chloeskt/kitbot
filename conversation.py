from collections.abc import Sequence
from dialog import Dialog
from operator import itemgetter

class SimpleConversation(Dialog, Sequence):
    """
    Simple version of a conversation
    """

    def __init__(self, dialogs):
        super().__init__()
        self._dialogs = dialogs

    def __getitem__(self, idx):
        return self._dialogs[idx]

    def __len__(self):
        return len(self._dialogs)

    def listen(self, text, response=True, **kwargs):
        """
        Returns the response with best confidence score
        """
        responses = [dialog.listen(text, response, **kwargs) for dialog in self._dialogs]

        return max(responses, key=itemgetter(1))

    def parse(self, text):
        """
        Returns parses for all internal dialogs for debugging
        """
        return [dialog.parse(text) for dialog in self._dialogs]

    def interpret(self, sents, **kwargs):
        """
        Returns interpretations for all internal dialogs for debugging
        """
        return [dialog.interpret(sents, **kwargs) for dialog in self._dialogs]

    def respond(self, sents, confidence, **kwargs):
        """
        Returns responses for all internal dialogs for debugging
        """
        return [dialog.respond(sents, confidence, **kwargs) for dialog in self._dialogs]
        