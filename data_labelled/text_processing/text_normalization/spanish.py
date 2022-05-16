import spacy
from text_processing.vocabulary_utils import CONCEPTS
from spacy.matcher import PhraseMatcher


# We are using a simple pipeline
def nlp_function(text, stopwords=None):
    nlp = spacy.load('es_core_news_sm', exclude=[
                     "ner", 'tagger', "morphologizer",
                     "parser", "attribute_ruler"])
    if stopwords:
        nlp.Defaults.stop_words |= set(stopwords)
    doc = nlp(text)
    return doc

def concept_matcher():
    nlp = spacy.load('es_core_news_sm', exclude=[
                     "ner", 'tagger', "morphologizer",
                     "parser", "attribute_ruler"])
    concept_matcher = PhraseMatcher(nlp.vocab)
    for concept, options in CONCEPTS.items():
        concept_matcher.add(
            concept.upper(), [nlp(opt) for opt in options])

    return concept_matcher
