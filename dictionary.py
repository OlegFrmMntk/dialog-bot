import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.data import load

from tkinter import *

root = Tk()

txt = StringVar()
txt.set("There are numerous regions that have appeared in the various media of the Pokemon franchise.")

res = StringVar()

lemmatizer = WordNetLemmatizer()


def help_window():
    children = Toplevel(root)
    children.title('Help')

    text = Text(children, height=20, width=100)
    scroll = Scrollbar(children)
    scroll.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    text.insert(END, helpmsg)

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


def pos_tag_sentence(sent):
    postgs = nltk.pos_tag(nltk.word_tokenize(sent))
    rtgs = list()
    i = 0
    pos = 1
    while i < len(postgs):
        pt = postgs[i]
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


tagdict = load('help/tagsets/upenn_tagset.pickle')


def tag_text():
    sentences = nltk.sent_tokenize(txt.get())
    out = str()
    for sent in sentences:
        out += "--- Sentence: {}\n".format(sent)
        tsent = pos_tag_sentence(sent)
        i = 0
        tsent = sorted(tsent, key=lambda s: s[0])
        while i < len(tsent):
            pt = tsent[i]
            out += "{} -- {}({}). Position: {}\n".format(pt[0], pt[1], tagdict[pt[1]][0], pt[2])
            i += 1
    res.set(out)


helpmsg = str()
for key in tagdict.keys():
    helpmsg += "* {} -- {}\nExamples: {}\n".format(key, tagdict[key][0], tagdict[key][1])
