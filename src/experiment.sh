#!/bin/bash

for ratio in `seq 0.75 0.25 1.0`
do
  cp ../exp_result/template.txt ../exp_result/kgcn_on_ml_dbpedia_ratio_${ratio}.txt
  python3 main.py --dataset "movie/DBpedia/items_ratio_${ratio}" >> ../exp_result/kgcn_on_ml_dbpedia_ratio_${ratio}.txt
done
