#!/bin/bash

python3  ./cut_kg.py -r 0.75
python3  ./cut_kg.py -r 0.5
python3  ./cut_kg.py -r 0.25
touch item_index2entity_id_ratio_0.00.txt
