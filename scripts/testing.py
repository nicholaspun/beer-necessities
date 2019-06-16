import io, csv, nltk, re
from os.path import expanduser
from nltk.tag.senna import SennaTagger
nltk.download('stopwords')
nltk.download('wordnet')

HOME = expanduser('~')

STOPWORDS = set(nltk.corpus.stopwords.words("english"))

GRAMMAR = r"""
    ADJ: { <JJ.*>*<CC>*<IN>*<JJ.*><NN.*>* }
"""

def flatten(lol):
    return [ ele for lst in lol for ele in lst ]

def extractADJ(tree):
    return [node for node in tree if isinstance(node, nltk.tree.Tree) ]


# raw = "Met with an initial sweet cherry, citrus-y taste; sort of tangy, zesty; then met with those sharp hops; extremely well balanced. Definitely on the stronger side with respects to bitterness, but really well done, really fun beer"
raw = "Crisp, clear, slightly sweet with a hint of wheaty, malty flavours. Nothing too special"
raw = re.sub('-y', 'y', raw) # Replace words like "citrus-y" with "citrusy"
raws = raw.split(';') # I separate sentence fragments with semi-colons a lot
raws = [ re.sub('[^a-zA-Z]', ' ', raw) for raw in raws ] # Replace symbols 
raws = [ re.sub('well balanced', 'well-balanced', raw) for raw in raws ] # Catch "well-balanced" as adjective

chunker = nltk.RegexpParser(GRAMMAR)

st = SennaTagger(HOME+'/senna')
taggeds = [ st.tag(nltk.word_tokenize(raw)) for raw in raws ]
trees = [ chunker.parse(tagged) for tagged in taggeds ]

trees_2 = [chunker.parse(chunker.parse(nltk.pos_tag(nltk.word_tokenize(raw)))) for raw in raws ]

cmbnd = flatten([extractADJ(t) for t in trees]) + flatten([extractADJ(t) for t in trees_2])

print(cmbnd)


            


 
