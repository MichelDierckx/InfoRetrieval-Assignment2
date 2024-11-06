from org.apache.lucene.analysis import CharArraySet


def load_stopwords_spacy():
    """
    https://github.com/igorbrigadir/stopwords/blob/master/en/spacy.txt
    """
    file_path = "resources/spacy_stopwords.txt"
    stopwords_list = []
    # read line by line
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            stopwords_list.append(line.strip(line))

    stopwords_set = CharArraySet(len(stopwords_list), True)
    # Add each custom stopword to the set
    for stopword in stopwords_list:
        stopwords_set.add(stopword)
    return stopwords_set


def load_lucene_stopwords():
    stopwords = [
        "but", "be", "with", "such", "then", "for", "no", "will", "not", "are",
        "and", "their", "if", "this", "on", "into", "a", "or", "there", "in",
        "that", "they", "was", "is", "it", "an", "the", "as", "at", "these",
        "by", "to", "of"
    ]
    stopwords_set = CharArraySet(len(stopwords), True)
    # Add each custom stopword to the set
    for stopword in stopwords:
        stopwords_set.add(stopword)
    return stopwords_set
