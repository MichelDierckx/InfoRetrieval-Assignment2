from org.apache.lucene.index import Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BooleanQuery, PhraseQuery, BooleanClause, FuzzyQuery


class QueryFactory:
    @staticmethod
    def create_query(query_text, query_type, query_parser=None, maxEdits=2, slop=0):
        if query_type == "fuzzy":
            return QueryFactory._create_fuzzy_query(query_text, maxEdits, 1, 50)
        elif query_type == "phrase":
            return QueryFactory._create_phrase_query(query_text, slop)
        elif query_type == "boolean_and":
            return QueryFactory._create_boolean_query(query_text, query_parser)
        elif query_type == "boolean_or":
            return QueryFactory._create_standard_query(query_text, query_parser)
        else:
            raise ValueError(f"Unknown query type: {query_type}")

    @staticmethod
    def _create_fuzzy_query(query_text, maxEdits, prefixLength, maxExpansions):
        terms = query_text.split()
        boolean_query_builder = BooleanQuery.Builder()

        for term_text in terms:
            escaped_term = QueryParser.escape(term_text)
            term = Term("text_content", escaped_term)
            fuzzy_query = FuzzyQuery(term, prefixLength, maxExpansions, maxEdits=maxEdits)
            boolean_query_builder.add(fuzzy_query, BooleanClause.Occur.SHOULD)

        return boolean_query_builder.build()

    @staticmethod
    def _create_phrase_query(query_text, slop):
        phrase_query = PhraseQuery.Builder()
        terms = query_text.split()

        for t in terms:
            term = Term("text_content", t)
            phrase_query.add(term)

        phrase_query.setSlop(slop)
        return phrase_query.build()

    @staticmethod
    def _create_boolean_query(query_text, query_parser):
        query_parser.setDefaultOperator(QueryParser.Operator.AND)
        return query_parser.parse(QueryParser.escape(query_text))

    @staticmethod
    def _create_standard_query(query_text, query_parser):
        return query_parser.parse(QueryParser.escape(query_text))
