from stanfordcorenlp import StanfordCoreNLP
import logging
import json
from nltk.parse import CoreNLPParser

class StanfordNLP:
    def __init__(self, url='http://localhost:9000'):
        super().__init__()
        self.nlp = CoreNLPParser(url)
        self.nlp_ner = CoreNLPParser(url, tagtype='ner')
        self.nlp_pos = CoreNLPParser(url, tagtype='pos')
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return list(self.nlp.tokenize(sentence))

    def pos(self, sentence):
        return list(self.nlp_pos.tag(sentence))

    def ner(self, sentence):
        self.tagtype = 'ner'
        return self.nlp_ner.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence, url='http://localhost:9000'):
        from nltk.parse.corenlp import CoreNLPDependencyParser
        dep_parser = CoreNLPDependencyParser(url)
        return self.dep_parser.parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))
    
    def raw_parse(self, sentence):
        return list(self.nlp.raw_parse(sentence))

    def plot_tree(self, sentence):
        tree = self.raw_parse(sentence)
        return tree[0].draw()

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word': token['word'],
                'lemma': token['lemma'],
                'pos': token['pos'],
                'ner': token['ner']
            }
        return tokens

if __name__ == '__main__':
    sNLP = StanfordNLP()
    text = 'How many teaspoons are in a tablespoon?'
    #print('annotate:', sNLP.annotate(text))
    #print("POS:", sNLP.pos(text))
    #print("Tokens:", sNLP.word_tokenize(text))
    #print("NER:", sNLP.ner(text))
    #print("Parse:", sNLP.parse(text))
    #print("Dep Parse:", sNLP.dependency_parse(text))
    tree = sNLP.raw_parse(text)
    print(sNLP.plot_tree(text))
    #print()