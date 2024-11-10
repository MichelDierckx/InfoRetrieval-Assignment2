import csv
import logging
import os
import time
from typing import Union, List, Optional

import lucene
import pandas as pd
from java.nio.file import Paths
from org.apache.lucene.document import Document, TextField, Field, StoredField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import FSDirectory

from .analyzer import AnalyzerFactory
from .config import config
from .evaluate import evaluate
from .query_factory import QueryFactory
from .similarity import SimilarityFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def float_to_str_no_decimal_point(x: float) -> str:
    return str(x).replace('.', '')


def create_index_dir_name(data_dir: str, analyzer: str) -> str:
    # Get the base name of the directory from data_dir (e.g., 'full_docs_small')
    base_name = os.path.basename(os.path.normpath(data_dir))

    # Combine the base directory name with the analyzer name to create a unique index dir name
    index_dir_name = f"{base_name}_{analyzer}"

    return index_dir_name


def extract_id_from_filename(filename: str) -> int:
    """
    Extract textfile id from filename.
    :param filename: the filename (not including the path)
    :return: the integer present in the filename.
    """
    id_str = filename.split('_')[1]
    id_str = id_str.split('.')[0]
    return int(id_str)


def index_txt_file(ind_writer: IndexWriter, data_dir: str, file: str) -> None:
    """Indexes a single text file."""
    data_path = os.path.join(data_dir, file)
    doc = Document()
    with open(data_path, "r", encoding='utf-8') as f:
        text_to_index = f.read()
        doc.add(TextField("text_content", text_to_index, Field.Store.NO))  # Don't store the text field
        doc_id = extract_id_from_filename(file)
        doc.add(StoredField("doc_id", doc_id))  # stored but not indexed
        ind_writer.addDocument(doc)


def rank_queries_from_file(index_searcher: IndexSearcher, query_parser: QueryParser, input_file: str, output_file: str,
                           delimiter: str = ',',
                           top_k: Optional[int] = 10, query_type: str = "", maxEdits: int = 0, slop: int = 0) -> None:
    """
    Reads queries from a csv file and generates a ranking for them.

    :param input_file: Path to the input CSV or TSV file with queries.
    :param output_file: Path to the output file where rankings will be saved.
    :param delimiter: The character used to separate values in the input file (default is ',').
    :param top_k: How many top ranked documents to save in the output file; if None, saves all.
    :param query_type: The type of query
    :param maxEdits: The maximum number of edits allowed per query
    """
    logging.info(
        f"Ranking documents for the queries in '{input_file}' with limit: {top_k if top_k is not None else 'no limit'}...")
    queries_df = pd.read_csv(input_file, delimiter=delimiter)
    with open(output_file, 'w') as output_f:
        output_f.write("Query_number,doc_number\n")
        # loop over queries
        for i, (_, row) in enumerate(queries_df.iterrows()):
            query_number = row['Query number']
            query_text = row['Query']

            # TODO: different types of querying? fuzzy queries, boolean queries, exact queries, ...?
            query = QueryFactory.create_query(query_text=query_text, query_type=query_type, query_parser=query_parser,
                                              maxEdits=maxEdits, slop=slop)

            top_docs = index_searcher.search(query, top_k)  # Get top k results
            hits = top_docs.scoreDocs  # internal doc id's found for query
            nr_hits = top_docs.totalHits  # number of hits
            for hit in hits:
                internal_id = hit.doc
                doc = index_searcher.doc(internal_id)
                doc_id = doc.get("doc_id")
                output_f.write(f"{query_number},{doc_id}\n")
    logging.info(f"Saved document rankings to '{output_file}'.")


def update_evaluation_file(evaluation_file_path: str, run_name: str, k: int, map_at_k: float, mar_at_k: float,
                           elapsed_time: float):
    # Check if the file exists
    file_exists = os.path.exists(evaluation_file_path)

    # Open the CSV file in read mode if it exists to check for existing entries
    if file_exists:
        with open(evaluation_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Check if headers exist, if not, create them
        if not rows or rows[0] != ['run_name', 'k', 'MAP@K', 'MAR@K', 'time(s)']:
            rows.insert(0, ['run_name', 'k', 'MAP@K', 'MAR@K', 'time(s)'])

        # Check if the run_name and k already exist
        updated = False
        for i, row in enumerate(rows):
            if row[0] == run_name and int(row[1]) == k:
                # If run_name and k exist, update that row with new values
                rows[i] = [run_name, k, map_at_k, mar_at_k, f"{elapsed_time:.2f}"]
                updated = True
                break

        if not updated:
            # If run_name and k do not exist, append a new row
            rows.append([run_name, k, map_at_k, mar_at_k, f"{elapsed_time:.2f}"])

    else:
        # If the file does not exist, create it and add the header
        rows = [['run_name', 'k', 'MAP@K', 'MAR@K', 'time(s)'],
                [run_name, k, map_at_k, mar_at_k, f"{elapsed_time:.2f}"]]

    # Write the updated or new rows to the CSV file
    with open(evaluation_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def main(args: Union[str, List[str]] = None) -> int:
    start_time = time.time()  # Start timing
    config.parse(args)  # parse config file or command line arguments
    if config.get('help', False):
        return 0

    logging.info(f"Lucene version: {lucene.VERSION}")  # 9.12.0
    logging.info(f"data_dir: {config.data_dir}")
    logging.info(f"index_dir: {config.index_dir}")
    logging.info(f"analyzer: {config.analyzer}")
    logging.info(f"similarity: {config.similarity}")
    # Log BM25 parameters if using BM25
    if config.similarity.lower() == "bm25":
        logging.info(f"BM25 Parameter k1: {config.get('k1')}")
        logging.info(f"BM25 Parameter b: {config.get('b')}")
    logging.info(f"queries: {config.get('queries')}")
    logging.info(f"ranking_dir: {config.get('ranking_dir')}")
    logging.info(f"evaluation_dir: {config.get('evaluation_dir')}")
    logging.info(f"reference_file: {config.get('reference_file')}")
    logging.info(f"query type: {config.query_type}")

    lucene.initVM()  # initialize VM to adapt Java Lucene to Python

    data_dir = config.data_dir
    base_name = os.path.basename(os.path.normpath(config.data_dir))
    k1 = float_to_str_no_decimal_point(config.k1)
    b = float_to_str_no_decimal_point(config.b)
    index_dir_name = f"{base_name}_{config.analyzer}_{config.similarity}_{k1}_{b}"
    full_index_path = os.path.join(config.index_dir, index_dir_name)

    analyzer = AnalyzerFactory.get_analyzer(config.analyzer)
    similarity = SimilarityFactory.get_similarity(similarity_type=config.similarity, k1=config.k1, b=config.b)

    if os.path.exists(full_index_path) and any(os.scandir(full_index_path)):
        logging.info(f"Index directory '{full_index_path}' already exists, skipping indexing.")
    else:
        # Set up IndexWriterConfig with specified analyzer and similarity
        indexWriterConfig = IndexWriterConfig(analyzer)
        indexWriterConfig.setSimilarity(similarity)
        indexWriterConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE)  # Overwrite existing index files if present

        # Create and open the index directory
        index_dir = FSDirectory.open(Paths.get(full_index_path))

        indexWriter = IndexWriter(index_dir, indexWriterConfig)

        # Start indexing files
        logging.info(f"Indexing directory {data_dir}...")
        for file in os.listdir(data_dir):
            if file.endswith(".txt"):
                index_txt_file(indexWriter, data_dir, file)

        indexWriter.close()
        logging.info(f"Indexing complete, saved to '{full_index_path}'.")

    # Open the index directory
    index_dir = FSDirectory.open(Paths.get(full_index_path))
    # create reader object
    reader = DirectoryReader.open(index_dir)
    # instantiate/define reader
    searcher = IndexSearcher(reader)
    searcher.setSimilarity(similarity)

    queries_file: str = config.queries
    if queries_file.endswith(".tsv") or queries_file == "data/queries/queries.csv":
        delimiter = '\t'
    else:
        delimiter = ','

    queries_filename = os.path.splitext(os.path.basename(config.queries))[0]

    # Set up the QueryParser for the 'text_content' field
    query_parser = QueryParser("text_content", analyzer)
    print(config.query_type)
    if config.query_type != "fuzzy" and config.query_type != "phrase":
        print("other")
        rankings_file_name = f"{index_dir_name}_{config.query_type}_{queries_filename}.csv"
        rankings_file = os.path.join(config.ranking_dir, rankings_file_name)
        rank_queries_from_file(index_searcher=searcher, query_parser=query_parser, input_file=config.queries,
                               output_file=rankings_file,
                               delimiter=delimiter, top_k=10, query_type=config.query_type)
    elif config.query_type == "phrase":
        slop = config.get('slop')
        rankings_file_name = f"{index_dir_name}_{config.query_type}_{slop}_{queries_filename}.csv"
        rankings_file = os.path.join(config.ranking_dir, rankings_file_name)
        rank_queries_from_file(index_searcher=searcher, query_parser=query_parser, input_file=config.queries,
                               output_file=rankings_file,
                               delimiter=delimiter, top_k=10, query_type=config.query_type, slop=slop)
    else:
        print("fuzzy")
        max_edits = config.get("maxEdits")
        rankings_file_name = f"{index_dir_name}_{config.query_type}_{max_edits}_{queries_filename}.csv"
        rankings_file = os.path.join(config.ranking_dir, rankings_file_name)
        rank_queries_from_file(index_searcher=searcher, query_parser=query_parser, input_file=config.queries,
                               output_file=rankings_file,
                               delimiter=delimiter, top_k=10, query_type=config.query_type, maxEdits=max_edits)
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    logging.info(f"Program execution time: {elapsed_time:.2f} seconds")

    k_list = [1, 3, 5, 10]
    for k in k_list:
        evaluation = evaluate(result_file=rankings_file, expected_result_file=config.reference_file, k=k)
        update_evaluation_file(evaluation_file_path=config.evaluation_file, run_name=rankings_file_name, k=k,
                               map_at_k=evaluation.map_at_k, mar_at_k=evaluation.mar_at_k, elapsed_time=elapsed_time)

    return 0


if __name__ == "__main__":
    main()
