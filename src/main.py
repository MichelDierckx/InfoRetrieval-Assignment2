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

    lucene.initVM()  # initialize VM to adapt java lucene to python

    index_dir = FSDirectory.open(Paths.get(config.index_dir))  # set index dir

    data_dir = config.data_dir  # set data directory path (absolute or relative)
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' does not exist.")

    analyzer = AnalyzerFactory.get_analyzer(config.analyzer)  # retrieve specified analyzer

    indexWriterConfig = IndexWriterConfig(analyzer)

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

    print("Indexing complete.")

    return 0


if __name__ == "__main__":
    main()
