import io, csv, nltk, re, os, logging, uuid
from nltk.tag.senna import SennaTagger
from nltk.tag import pos_tag as BUILT_IN_TAGGER
from os.path import expanduser

HOME = expanduser('/')
STOPWORDS = set(nltk.corpus.stopwords.words("english"))
GRAMMAR = r"""
    ADJ: {  <JJ.*>*<CC>*<IN>*<JJ.*><NN.*>* }
"""
CHUNKER = nltk.RegexpParser(GRAMMAR)
SENNA_TAGGER = SennaTagger(HOME+'senna')

def normalize(sentence):
  sentence = re.sub('[^a-zA-Z]', ' ', sentence)
  sentence = sentence.lower()
  tokens = nltk.word_tokenize(sentence)
  lemmatized =  [ nltk.WordNetLemmatizer().lemmatize(t) for t in tokens if t not in STOPWORDS ]
  
  return set(lemmatized)

def flatten(lol):
    return [ele for lst in lol for ele in lst]

def extractADJ(tree):
    return [node for node in tree if isinstance(node, nltk.tree.Tree)]

class DataRow:
  def __init__(self, row):
    self.date = row.get('Date', None)
    self.brewery = row.get('Brewery', None)
    self.name = row.get('Name', None)
    self.description = row.get('Description', None)
    self.aroma = row.get('Aroma', None)
    self.taste = row.get('Taste', None)
    self.finish = row.get('Finish', None)
    self.rating = row.get('Rating', None)

  def __str__(self):
    return '''Date: {}
Brewery: {}
Name: {}
Description: {}
Aroma: {}
Taste: {}
Finish: {}
Rating: {}'''.format(self.date, self.brewery, self.name, self.description, self.aroma, self.taste, self.finish, self.rating)

  def keywords(self):
    keywords_desc = normalize(self.description)
    keywords_aroma = normalize(self.aroma)
    keywords_taste = normalize(self.taste)
    keywords_finish = normalize(self.finish)

    return keywords_desc | keywords_aroma | keywords_taste | keywords_finish

  def keywords_taste(self):
    text = re.sub('-y', 'y', self.taste)  # Replace words like "citrus-y" with "citrusy"
    text_fragments = text.split(';')  # I separate sentence fragments with semi-colons a lot
    text_fragments = [ re.sub('[^a-zA-Z]', ' ', text) for text in text_fragments ]  # Replace symbols
    text_fragments = [ re.sub('well balanced', 'well-balanced', text) for text in text_fragments ]  # Catch "well-balanced" as adjective

    st_tagged_text_fragment = [ SENNA_TAGGER.tag(nltk.word_tokenize(text)) for text in text_fragments ]
    built_in_tagged_text_fragment = [ BUILT_IN_TAGGER(nltk.word_tokenize(text)) for text in text_fragments ]

    st_tagged_tree = [ CHUNKER.parse(text) for text in st_tagged_text_fragment ]
    built_in_tagged_tree = [ CHUNKER.parse(text) for text in built_in_tagged_text_fragment ]

    logging.info(flatten([extractADJ(t) for t in st_tagged_tree]) + flatten([extractADJ(t) for t in built_in_tagged_tree]))

    return flatten([extractADJ(t) for t in st_tagged_tree]) + flatten([extractADJ(t) for t in built_in_tagged_tree])

# Start: 
with io.open('data.csv', encoding='utf-8-sig') as csvfile:
  data_reader = csv.DictReader(csvfile)
  data_rows = [ DataRow(row) for row in data_reader ]

keywords = set()

for row in data_rows:
  keywords |= row.keywords()

# logging.info(keywords)

keywords = set(kw for kw in keywords if len(kw) >= 2)  # Some stems slipping through









