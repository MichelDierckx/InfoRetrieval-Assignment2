from org.apache.lucene.analysis.core import SimpleAnalyzer, WhitespaceAnalyzer, StopAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer  # Used as StemAnalyzer for English
from org.apache.lucene.analysis.standard import StandardAnalyzer


class AnalyzerFactory:
    @staticmethod
    def get_analyzer(analyzer_type: str) -> "Analyzer":
        if analyzer_type == "simple":
            return SimpleAnalyzer()
        elif analyzer_type == "standard":
            return StandardAnalyzer()
        elif analyzer_type == "whitespace":
            return WhitespaceAnalyzer()
        elif analyzer_type == "stop":
            return StopAnalyzer()
        elif analyzer_type == "stem":
            return EnglishAnalyzer()
        else:
            raise ValueError(f"Unknown analyzer type: {analyzer_type}")
