import logging
import os
from typing import Union, List

import lucene
from java.nio.file import Paths
from org.apache.lucene.document import Document, TextField, Field
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.store import FSDirectory

from .analyzer import AnalyzerFactory
from .config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_index_dir_name(data_dir: str, analyzer: str) -> str:
    # Get the base name of the directory from data_dir (e.g., 'full_docs_small')
    base_name = os.path.basename(os.path.normpath(data_dir))

    # Combine the base directory name with the analyzer name to create a unique index dir name
    index_dir_name = f"{base_name}_{analyzer}"

    return index_dir_name


def index_txt_file(ind_writer: IndexWriter, file_path: str) -> None:
    """Indexes a single text file."""
    doc = Document()
    with open(file_path, "r", encoding='utf-8') as f:
        text_to_index = f.read()
        doc.add(TextField("text_content", text_to_index, Field.Store.YES))
        ind_writer.addDocument(doc)


def main(args: Union[str, List[str]] = None) -> int:
    config.parse(args)  # parse config file or command line arguments
    if config.get('help', False):
        return 0

    logging.info(f"Lucene version: {lucene.VERSION}")  # 9.12.0
    logging.info(f"data_dir: {config.data_dir}")
    logging.info(f"index_dir: {config.index_dir}")
    logging.info(f"analyzer: {config.analyzer}")

    lucene.initVM()  # initialize VM to adapt java lucene to python

    data_dir = config.data_dir  # set data directory path (absolute or relative)

    analyzer = AnalyzerFactory.get_analyzer(config.analyzer)  # retrieve specified analyzer

    indexWriterConfig = IndexWriterConfig(analyzer)

    base_name = os.path.basename(os.path.normpath(config.data_dir))
    index_dir_name = f"{base_name}_{config.analyzer}"
    full_index_path = os.path.join(config.index_dir, index_dir_name)
    index_dir = FSDirectory.open(Paths.get(full_index_path))  # set index dir

    indexWriter = IndexWriter(index_dir, indexWriterConfig)

    logging.info(f"Indexing directory {data_dir}...")
    # os.listdir return a list of all files within
    # the specified directory
    for file in os.listdir(data_dir):

        # The following condition checks whether
        # the filename ends with .txt or not
        if file.endswith(".txt"):
            # Appending the filename to the path to obtain
            # the fullpath of the file
            data_path = os.path.join(data_dir, file)
            index_txt_file(indexWriter, data_path)

    indexWriter.close()

    logging.info(f"Indexing complete, saved to '{full_index_path}'.")

    return 0


if __name__ == "__main__":
    main()
