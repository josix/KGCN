#!/bin/bash

MAPPING_FILE_NAME="mappingToEntityId"
TARGET="kg"

cat <(cut -f 1 <( tail +2 title.basics.tsv)  <( tail +2 name.basics.tsv)) \
    <( cut -f 2 <( tail +2 title.basics.tsv) | sort -u) \
    <(awk -f extract_genre.awk <(tail +2 title.basics.tsv) | sort -u) \
    | awk '{OFS="\t"}{print($1, NR)}' > $MAPPING_FILE_NAME.tsv

awk -f ./extract_film_principals.awk $MAPPING_FILE_NAME.tsv <(tail +2 title.principals.tsv) > $TARGET.txt
awk -f ./extract_film_basics.awk $MAPPING_FILE_NAME.tsv <(tail +2 title.basics.tsv) >> $TARGET.txt
python3  ./bind_ml_imdb.py
python3  ./bind_ml_imdb.py -r 0.75
python3  ./bind_ml_imdb.py -r 0.5
python3  ./bind_ml_imdb.py -r 0.25
touch item_index2entity_id_ratio_0.0.txt
