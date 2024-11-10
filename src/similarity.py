# Add to your main indexing script

from org.apache.lucene.search.similarities import BM25Similarity, ClassicSimilarity


class SimilarityFactory:
    # https://lucene.apache.org/core/9_12_0/core/org/apache/lucene/search/package-summary.html
    @staticmethod
    def get_similarity(similarity_type: str, k1: float = 1.2, b: float = 0.75) -> "Similarity":
        """Return the appropriate Lucene similarity based on a name."""
        similarity_name = similarity_type.lower()
        if similarity_name == "bm25":
            return BM25Similarity(k1,
                                  b)  # https://lucene.apache.org/core/9_12_0/core/org/apache/lucene/search/similarities/BM25Similarity.html
        elif similarity_name == "classic":
            return ClassicSimilarity()  # https://lucene.apache.org/core/9_12_0/core/org/apache/lucene/search/similarities/ClassicSimilarity.html
        else:
            raise ValueError(f"Unknown similarity type: {similarity_name}")
