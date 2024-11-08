#!/bin/bash

# Define your virtual environment path
VENV_PATH=".venv"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Define analyzers to run
ANALYZERS=("whitespace" "simple" "stop" "standard" "english" "english_spacy")

# Define common arguments
DATA_DIR="data/documents/full_docs"
INDEX_DIR="index"
SIMILARITY="bm25"
K1=1.2
B=0.75
QUERIES="data/queries/dev_queries.tsv"
RANKING_DIR="results/ranking"
EVALUATION_FILE="results/evaluation/evaluation.csv"
REFERENCE_FILE="data/queries/dev_query_results.csv"

# Loop through each analyzer and run the command
for ANALYZER in "${ANALYZERS[@]}"; do
    echo "Running with analyzer: $ANALYZER"
    python3 -m src.main \
        --data_dir "$DATA_DIR" \
        --index_dir "$INDEX_DIR" \
        --analyzer "$ANALYZER" \
        --similarity "$SIMILARITY" \
        --k1 "$K1" \
        --b "$B" \
        --queries "$QUERIES" \
        --ranking_dir "$RANKING_DIR" \
        --evaluation_file "$EVALUATION_FILE" \
        --reference_file "$REFERENCE_FILE"
done

# Additional run with english analyzer and classic similarity
echo "Running with analyzer: english_spacy and similarity: classic"
python3 -m src.main \
    --data_dir "$DATA_DIR" \
    --index_dir "$INDEX_DIR" \
    --analyzer "english_spacy" \
    --similarity "classic" \
    --queries "$QUERIES" \
    --ranking_dir "$RANKING_DIR" \
    --evaluation_file "$EVALUATION_FILE" \
    --reference_file "$REFERENCE_FILE"

# Additional run with english analyzer and custom BM25 parameters (k1=0.5, b=0.9)
echo "Running with analyzer: english_spacy, similarity: bm25, k1=0.5, b=0.9"
python3 -m src.main \
    --data_dir "$DATA_DIR" \
    --index_dir "$INDEX_DIR" \
    --analyzer "english_spacy" \
    --similarity "bm25" \
    --k1 0.5 \
    --b 0.9 \
    --queries "$QUERIES" \
    --ranking_dir "$RANKING_DIR" \
    --evaluation_file "$EVALUATION_FILE" \
    --reference_file "$REFERENCE_FILE"

# Deactivate the virtual environment
deactivate
