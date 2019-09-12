#!/bin/bash

MAPPING_FILE_NAME="mappingToEntityId"
TARGET="kg"

# python3 ./retrieval.py > kg.tsv

# cat <(cut -f 1 <( tail +2 kg.tsv)) <(cut -f 3 <(tail +2 kg.tsv)) | sort -u | awk '{OFS="\t"}{print($1, NR)}' > $MAPPING_FILE_NAME.tsv
# awk -f ./extract_relation.awk $MAPPING_FILE_NAME.tsv <(tail +2 kg.tsv) > $TARGET.txt
python3  ./bind_ml_dbpedia.py
python3  ./bind_ml_dbpedia.py -r 0.75
python3  ./bind_ml_dbpedia.py -r 0.5
python3  ./bind_ml_dbpedia.py -r 0.25
touch item_index2entity_id_ratio_0.00.txt
