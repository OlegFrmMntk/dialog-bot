import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.data import load

from tkinter import *

import docx

lemmatizer = WordNetLemmatizer()


tag_dict = {
            "JJ": wn.ADJ,
            "JJR": wn.ADJ,
            "JJS": wn.ADJ,
            "NN": wn.NOUN,
            "NNP": wn.NOUN,
            "NNS": wn.NOUN,
            "NNPS": wn.NOUN,
            "VB": wn.VERB,
            "VBN": wn.VERB,
            "VBG": wn.VERB,
            "VBZ": wn.VERB,
            "VBP": wn.VERB,
            "VBD": wn.VERB,
            "RB": wn.ADV,
            "RBR": wn.ADV,
            "RBS": wn.ADV,
            }


grammar = r"""
        P: {<IN>}
        V: {<V.*|MD>}
        N: {<NN.*>}
        JJP: {<RB|RBR|RBS|JJ|JJR|JJS|CD>}
        NP: {<N|PP>+<DT|PR.*|JJP|CC>}
        NP: {<PDT>?<DT|PR.*|JJP|CC><N|PP>+}
        PP: {<P><N|NP>}
        VP: {<NP|N|PR.*><V|VP>+}
        VP: {<V><NP|N>}
        VP: {<V><JJP>}
        VP: {<VP><PP>}
        """


def get_text(filename):
    doc = docx.Document(filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def pos_tag_sentence(sent):
    pos_tags = nltk.pos_tag(nltk.word_tokenize(sent))
    rtgs = list()
    i = 0
    pos = 1
    while i < len(pos_tags):
        pt = pos_tags[i]
        if re.search(r'[A-Za-z]+', pt[0]) is not None:
            lemma = str()
            if pt[1] in tag_dict:
                lemma = lemmatizer.lemmatize(pt[0], pos=tag_dict.get(pt[1]))
            else:
                lemma = lemmatizer.lemmatize(pt[0])
            rtgs.append([lemma.upper(), pt[1], pos])
            pos += 1
        i += 1
    return rtgs


tag_dictionary = load('help/tagsets/upenn_tagset.pickle')


def tag_text(txt):
    sentences = nltk.sent_tokenize(txt)
    out = str()
    for sent in sentences:
        out += "--- Sentence: {}\n".format(sent)
        sentence = pos_tag_sentence(sent)
        i = 0
        sentence = sorted(sentence, key=lambda s: s[0])
        while i < len(sentence):
            pt = sentence[i]
            out += "{} -- {}({}). Position: {}\n".format(pt[0], pt[1], tag_dictionary[pt[1]][0], pt[2])
            i += 1
    return out


def build_syntax_tree(text):
    sentences = nltk.sent_tokenize('\n'.join(text))
    for sentence in sentences:
        tag_sentence = pos_tag_sentence(sentence)
        ch = nltk.RegexpParser(grammar)
        tree = ch.parse(tag_sentence)
        return tree.draw()
