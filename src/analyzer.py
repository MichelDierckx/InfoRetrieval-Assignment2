from org.apache.lucene.analysis.core import SimpleAnalyzer, WhitespaceAnalyzer, StopAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer  # Used as StemAnalyzer for English
from org.apache.lucene.analysis.standard import StandardAnalyzer

from .stopwords import load_stopwords_spacy, load_lucene_stopwords


class AnalyzerFactory:
    @staticmethod
    def get_analyzer(analyzer_type: str) -> "Analyzer":
        if analyzer_type == "simple":
            # An Analyzer that filters LetterTokenizer with LowerCaseFilter
            return SimpleAnalyzer()  # https://lucene.apache.org/core/9_12_0/analysis/common/org/apache/lucene/analysis/core/SimpleAnalyzer.html
        elif analyzer_type == "standard":
            stopwords = load_lucene_stopwords()
            # Filters StandardTokenizer with LowerCaseFilter and StopFilter, using a configurable list of stop words.
            return StandardAnalyzer(
                stopwords)  # https://lucene.apache.org/core/9_12_0/core/org/apache/lucene/analysis/standard/StandardAnalyzer.html
        elif analyzer_type == "whitespace":
            # An Analyzer that uses WhitespaceTokenizer.
            return WhitespaceAnalyzer()  # https://lucene.apache.org/core/9_12_0/analysis/common/org/apache/lucene/analysis/core/WhitespaceAnalyzer.html
        elif analyzer_type == "stop":
            stopwords = load_lucene_stopwords()
            # LetterTokenizer with LowerCaseFilter and StopFilter
            return StopAnalyzer(
                stopwords)  # https://lucene.apache.org/core/9_12_0/analysis/common/org/apache/lucene/analysis/core/StopAnalyzer.html
        elif analyzer_type == "english":
            # Analyzer for English. Builds an analyzer with the default english stop words.
            # A Analyzer.TokenStreamComponents built from an StandardTokenizer filtered with EnglishPossessiveFilter, LowerCaseFilter, StopFilter, SetKeywordMarkerFilter if a stem exclusion set is provided and PorterStemFilter.
            return EnglishAnalyzer()  # https://lucene.apache.org/core/9_12_0/analysis/common/org/apache/lucene/analysis/en/EnglishAnalyzer.html
        elif analyzer_type == "english_spacy":
            stopwords = load_stopwords_spacy()
            # Analyzer for English. Builds an analyzer with the SPACY english stop words.
            # A Analyzer.TokenStreamComponents built from an StandardTokenizer filtered with EnglishPossessiveFilter, LowerCaseFilter, StopFilter, SetKeywordMarkerFilter if a stem exclusion set is provided and PorterStemFilter.
            return EnglishAnalyzer(
                stopwords)  # https://lucene.apache.org/core/9_12_0/analysis/common/org/apache/lucene/analysis/en/EnglishAnalyzer.html

        else:
            raise ValueError(f"Unknown analyzer type: {analyzer_type}")
