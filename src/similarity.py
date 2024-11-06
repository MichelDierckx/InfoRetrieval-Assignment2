# Add to your main indexing script

from org.apache.lucene.search.similarities import BM25Similarity, ClassicSimilarity


class SimilarityFactory:
    @staticmethod
    def get_similarity(similarity_type: str) -> "Similarity":
        """Return the appropriate Lucene similarity based on a name."""
        similarity_name = similarity_type.lower()
        if similarity_name == "bm25":
            return BM25Similarity()
        elif similarity_name == "classic":
            return ClassicSimilarity()
        else:
            raise ValueError(f"Unknown similarity type: {similarity_name}")
