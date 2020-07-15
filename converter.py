import os 
import json
import inflect 
import humanize
from nltk.stem.snowball import SnowballStemmer
from parsing import StanfordNLP
from dialog import Dialog
from nltk.tree import Tree
from nltk.util import breadth_first

class Converter(Dialog, StanfordNLP):
    """
    Answers questions about converting units
    """

    def __init__(self, conversion_path='conversions.json'):
        super().__init__()
        with open(conversion_path, 'r') as f:
            self.metrics = json.load(f)
        self.inflect = inflect.engine()
        self.stemmer = SnowballStemmer('english')
        self.parser = StanfordNLP()

    def parse(self, sentence):
        parse = self.parser.raw_parse(sentence)
        return parse 

    def interpret(self, sents, **kwargs):
        measures = []
        confidence = 0
        results = dict()
    
        #the root is the first item in the parsed sents tree
        root = sents[0]

        #make sure there are wh- adverb phrases 
        if 'WRB' in [tag for word, tag in root.pos()]:
            #if so, increment confidence and traverse parse tree
            confidence += .2
            #set maxdepth to limit recursion 
            for clause in breadth_first(root, maxdepth=8):
                #find the simple declarative clauses 
                if isinstance(clause, Tree):
                    if clause.label() in ["S", "SQ", "WHNP"]:
                        for token, tag in clause.pos():
                            #store nouns as target measures
                            if tag in ['NN', 'NNS']:
                                measures.append(token)
                            #store numbers as target quantities
                            elif tag in ["CD"]:
                                results["quantity"] = token
            #handle duplication for very nested trees
            measures = list(set([self.stemmer.stem(mnt) for mnt in measures]))

            #if both source and destination measures are provided ... 
            if len(measures) == 2:
                confidence += .4
                results["src"] = measures[0]
                results["dst"] = measures[1]

                #check to see if they correspond to our lookup table
                if results["src"] in self.metrics.keys():
                    confidence += .2
                    if results["dst"] in self.metrics[results["src"]]['Destination']:
                        confidence += .2

        return results, confidence, kwargs

    def convert(self, src, dst, quantity=1.0):
        """
        Converts from the source unit to the destination unit for the given quantity
        of the source unit
        """
        #stem source and destination to remove pluralization 
        src, dst = tuple(map(self.stemmer.stem, (src, dst)))

        #check that we can convert 
        if dst not in self.metrics:
            raise KeyError("cannot convert to '{}' units".format(src))
        if src not in self.metrics[dst]['Destination']:
            raise KeyError("cannot convert from '{}' to '{}'".format(src, dst))

        idx = self.metrics[dst]['Destination'].index(src)
        return self.metrics[dst]['Units'][idx] * float(quantity), src, dst

    def round(self, num):
        num = round(float(num), 4)
        if num.is_integer():
            return int(num)
        return num

    def pluralize(self, noun, num):
        return self.inflect.plural_noun(noun, num)

    def numericalize(self, amt):
        if amt > 100.0 and amt < 1e6:
            return humanize.intcomma(int(amt))
        if amt >= 1e6:
            return humanize.intword(int(amt))
        elif isinstance(amt, int) or amt.is_integer():
            return humanize.apnumber(int(amt))
        else:
            return humanize.fractional(amt)

    def respond(self, sents, confidence, **kwargs):
        """
        Response makes use of the humanize and inflect lib to produce much more human
        understandable results
        """
        if confidence < .5:
            return "I'm sorry, I don't know that one :("
        try:
            quantity = sents.get('quantity', 1)
            amount, source, target = self.convert(**sents)
            amount = self.round(amount)
            quantity = self.round(quantity)
            source = self.pluralize(source, quantity)
            target = self.pluralize(target, amount)
            verb = self.inflect.plural_verb("is", amount)
            quantity = self.numericalize(quantity)
            amount = self.numericalize(amount)

            return "There {} {} {} in {} {}.".format( verb, amount, target, quantity, source )

        except KeyError as e:
            return "I'm sorry I {}".format(str(e))  

if __name__ == "__main__":
    conv = Converter() 
    print(conv.listen("How many cups are in a gallon?")) 
    print(conv.listen("How many gallons are in 2 cups?")) 
    print(conv.listen("How many tablespoons are in a cup?")) 
    print(conv.listen("How many tablespoons are in 10 cups?")) 
    print(conv.listen("How many tablespoons are in a teaspoon?"))
    

