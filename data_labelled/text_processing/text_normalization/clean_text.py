import re
from .spanish import nlp_function, concept_matcher
from text_processing.vocabulary_utils import STOPWORDS, CONCEPTS
import emoji
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher, Matcher


def remove_characters(hashtags=True, mentions=True, special_characters=True,
                      emoticons=True, url=True, numbers=True):
    """
    This function return the function that will remove characters from text
    :param hashtags: flag to remove hashtags
    :param mentios: flag to remove @mentions
    :param special_characters: flag to remove punctuation and
    other special characters
    :param emoticons: flag to remove emoticons from text
    :param url: flag to remove url
    :param numbers: flag to remove numbers
    :return: the function that can be applied to some text
    """
    def _remove_characters(text):
        if url:
            text = re.sub(r'www.\S+', '', text)
            text = re.sub(r'https:\S+', '', text)
            text = re.sub(r'\S+.com ', '', text)
            text = re.sub(r'\S+.cl ', '', text)
        if hashtags:
            text = re.sub(r"(#[A-Za-z0-9-á-é-í-ó-ú]+)|(\w+:\/\/\S+)", '', text)
        if mentions:
            text = re.sub(r"(@[A-Za-z0-9-á-é-í-ó-ú]+)|(\w+:\/\/\S+)", '', text)
        if emoticons:
            text = re.sub(r'(<[\w.%+->]+)', '', text)
            text = emoji.get_emoji_regexp().sub(r'', text)
        if numbers:
            text = re.sub('[0-9]+', '', text)
        if special_characters:
            text = re.sub('[,.¿¡!?_�@|#:")(;-]', '', text)
            text = re.sub('[“”]', '', text)
            text = re.sub('[/]', '', text)
            text = re.sub('[…]', '', text)
            text = re.sub('  ', ' ', text)
            text = re.sub(r'\n', '', text)

        return text
    return _remove_characters


_remove_characters = remove_characters(
    hashtags=True, special_characters=True, emoticons=True)


def standard_text_pipeline(text, lista_stopwords=None):
    """
    This function creates the standard pipeline function
    :return:
    """
    # Remove characters
    text = _remove_characters(text)
    # Lower
    text = text.lower()
    # Tokenize and remove stopwords
    doc = nlp_function(text, lista_stopwords)
    return doc


def get_processed_text(doc):
    return [w.text for w in doc if not w.is_stop]

def detect_concepts(doc, return_context=None):
    """
    Detects concepts (single word or more) in the text.
    :param text: text where the concepts could appear in
    :param return_context: None or a tuple that indicates how
            many tokens before and after should be retrieved as context
    :return: a list of matches in the text.
        Each match is a string (name of the concept), start token, end token,
        matched text, context (if requested)
    """
    cond_1 = return_context is not None
    cond_2 = isinstance(return_context, tuple) and len(return_context) == 2
    if (cond_1) and not (cond_2):
        raise ValueError('return_context must be a tuple with lenght 2')

    #concept_matcher
    nlp = spacy.load('es_core_news_sm', exclude=[
                     "ner", 'tagger', "morphologizer",
                     "parser", "attribute_ruler"])
    #concept_matcher = PhraseMatcher(nlp.vocab)
    concept_matcher = Matcher(nlp.vocab)

    for concept, options in CONCEPTS.items():
        '''
        concept_matcher.add(
            concept, [nlp(opt) for opt in options])
        '''
        # CHANGE IT HERE
        pattern = [{"LOWER": {"IN": options}}, {"IS_LOWER": True, "OP": "?"}, {"IS_LOWER": True, "OP": "?"}, {"IS_LOWER": True, "OP": "?"}, {"LOWER": {"IN": options}}]
        concept_matcher.add(
            concept, [pattern])

        var = nlp.vocab.strings[concept.upper()]

    matches_text = []

    for match_id, start, end in concept_matcher(doc):
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        if return_context is not None:
            start_c = max(start - return_context[0], 0)
            end_c = min(end + return_context[1], len(doc))
            matches_text.append(string_id)
            #matches_text.append((string_id, start, end, span.text, span[start_c, end_c]))
        else:
            #matches_text.append((string_id, start, end, span.text))
            matches_text.append(string_id)
            
    # return unique matches    
    #matches = set(matches_text)
    return matches_text

def get_stopwords():
    lista_stopwords = STOPWORDS
    return lista_stopwords
