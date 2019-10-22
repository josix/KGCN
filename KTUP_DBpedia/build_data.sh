#!/bin/bash

MAPPING_FILE_NAME="mappingToEntityId"
TARGET="kg"


cat ./train.dat ./test.dat ./valid.dat | awk 'BEGIN{OFS="\t"}{print $1, $3, $2}' > "$TARGET.txt"
awk 'BEGIN{ FS="\t"; OFS="\t" } { print $2,$1; }' ./e_map.dat > "$MAPPING_FILE_NAME.tsv"

python3  ./bind_ml_dbpedia.py
python3  ./bind_ml_dbpedia.py -r 0.75
python3  ./bind_ml_dbpedia.py -r 0.5
python3  ./bind_ml_dbpedia.py -r 0.25
touch item_index2entity_id_ratio_0.00.txt
