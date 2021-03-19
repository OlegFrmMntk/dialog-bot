import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.data import load

import docx

import en_core_web_sm

import matplotlib.pyplot as plt

from wordcloud import WordCloud

from tkinter import *


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


def get_words(input_text):
    dictionary = []

    word = ''
    for sign in input_text:
        if 'a' <= sign <= 'z' or 'A' <= sign <= 'Z':
            word += sign
        elif len(word) > 0:
            dictionary.append(word)
            word = ""
    if len(word) > 0:
        dictionary.append(word)
    return dictionary


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


def tag_text(input_text):
    sentences = nltk.sent_tokenize(input_text)
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


def build_syntax_tree(input_text):
    sentences = nltk.sent_tokenize(input_text)
    for sentence in sentences:
        tag_sentence = pos_tag_sentence(sentence)
        ch = nltk.RegexpParser(grammar)
        print(input_text)
        print(tag_sentence)
        tree = ch.parse(tag_sentence)
       # return tree.draw()


def analyze(input_text):
    nlp = en_core_web_sm.load()

    doc = nlp(input_text)

    output_text = f"Number of characters: {len(input_text)}\n"
    output_text += f"Number of characters without spaces {len(input_text) - input_text.count(' ')}\n"

    words = get_words(input_text)
    output_text += f"Number of words {len(words)}\n"
    output_text += f"Number of unique words {len(set(words))}\n\n"
    output_text += "word    count      %\n"

    for i in set(words):
        output_text += "{}    {}        {:.3f}\n".format(i, words.count(i), (100 * words.count(i) / len(words)))

    output_text += "Recognized named entities:\n"
    for ent in doc.ents:
        output_text += "{} -- {}\n".format(ent.text, ent.label_)

    tokens = nltk.word_tokenize(input_text)

    output_text += "\nSymsets:\n"
    for token in tokens:
        if re.search(r"[A-Za-z]+", token) is not None:
            synsets = wn.synsets(token)

            if len(synsets) > 0:
                output_text += "\n{}".format(token)

                if len(synsets[0].lemmas()) > 0:
                    output_text += "\n -- Lemmas: "

                for lemma in synsets[0].lemmas():
                    output_text += lemma.name() + '; '

                if len(synsets[0].hyponyms()) > 0:
                    output_text += "\n -- Hyponyms: "

                for i in synsets[0].hyponyms():
                    output_text += i.lemma_names()[0] + '; '

                if len(synsets[0].hypernyms()) > 0:
                    output_text += "\n -- Hypernyms: "

                for j in synsets[0].hypernyms():
                    output_text += j.lemma_names()[0] + '; '

    return output_text


def get_text(doc):
    #doc = docx.Document(filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def generate_wordcloud(file):
    input_txt = get_text(file)
    wordcloud = WordCloud().generate(input_txt)
    plt.imshow(wordcloud)
    plt.show()
