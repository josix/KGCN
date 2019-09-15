#!/bin/bash

if [ $# != 1 ]
then
  echo "USAGE: ./experiment.sh {DBpedia | IMDb}";
  exit 1
fi

KG="$1"

case $KG in
  DBpedia)
    kg="dbpedia";;
  IMDb)
    kg="imdb";;
   *)
    echo "USAGE: ./experiment.sh {DBpedia | IMDb}"
    exit 1
esac


for ratio in `seq 0.0 0.25 1.0`
do
  cp ../exp_result/template.txt ../exp_result/kgcn_on_ml_${kg}_ratio_${ratio}.txt
  python3 main.py --dataset "movie/${KG}/items_ratio_${ratio}" >> ../exp_result/kgcn_on_ml_${kg}_ratio_${ratio}.txt
done
