# Project 2 information retrieval

## Description

Assignment 2 for the course Information Retrieval 2024-2025 at UAntwerpen.

## Usage

### Requirements

Make sure PyLucene (9.12.0) is installed and configured.

Install other requirements via:

```bash
pip install -r requirements.txt
```

### Configuration

To request an overview of the available parameters:

```bash
python3 -m src.main --help
```

Program arguments:

`--data_dir` *Directory containing the documents*  
`--index_dir` *Directory that will contain the indexes*  
`--analyzer` *The analyzer to be used (simple, standard, whitespace, stop, english, english_spacy)*  
`--similarity` *The similarity function to be used for document ranking (bm25, classic)*  
`--k1` *BM25 k1 parameter, controls term frequency saturation. Typical range is 1.2 to 2.0*  
`--b` *BM25 b parameter, controls document length normalization. Typical range is 0 to 1*  
`--queries`: *Path to the query file (supported formats: CSV and TSV).*  
`--ranking_dir`: *Directory where computed query results will be saved.*  
`--evaluation_file`: *CSV file where evaluation results will be appended.*  
`--reference_file`: *Path to the file containing the reference query results for evaluation.*  
`--query_type`: *The type of query to evaluate (options: fuzzy, phrase, boolean_and, boolean_or). Default is
boolean_or.*  
`--maxEdits`: *Maximum number of edits (insert, delete, or change) for fuzzy queries (range: 0 to 2). Default is 2.*  
`--slop`: *Number of terms that may occur between terms in a phrase query. Default is 0.*

The program arguments can be provided either by a configuration file (by default config.ini) or by command-line
arguments.
The command-line arguments take precedence over the configuration file.

### Running the program

```bash
python3 -m src.main -c /path/to/config.ini
```

