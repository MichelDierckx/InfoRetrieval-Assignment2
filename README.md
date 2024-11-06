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

Program arguments:

`--data_dir` *Directory containing the documents*  
`--index_dir` *Directory that will contain the index*  
`--analyzer` *The analyzer to be used (simple, standard, whitespace, stop, stem)*  


The program arguments can be provided either by a configuration file (by default config.ini) or by command-line arguments.
The command-line arguments take precedence over the configuration file.

### Running the program

```bash
python3 -m src.main
```

