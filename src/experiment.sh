#!/bin/bash

if [ ${#} != 1 ]
then
  echo "USAGE: ./experiment.sh {DBpedia | IMDb |KTUP_DBpedia | Satori}";
  exit 1
fi

KG="${1}"

case ${KG} in
  Satori)
    kg="satori";;
  KTUP_DBpedia)
    kg="ktup_debpdia";;
  DBpedia)
    kg="dbpedia";;
  IMDb)
    kg="imdb";;
   *)
    echo "USAGE: ./experiment.sh {DBpedia | IMDb | KTUP_DBpedia | Satori}"
    exit 1
esac


Target="Satori_f1_score_distribution_user_10000_user_degree"
for ratio in `seq 0.0 1.00 1.0`
do
  mkdir -p ../exp_result/$Target
  cp ../exp_result/template.txt ../exp_result/$Target/kgcn_on_ml_${kg}_ratio_${ratio}.txt
  python3 main.py --dataset "movie/${KG}/items_ratio_${ratio}" >> ../exp_result/$Target/kgcn_on_ml_${kg}_ratio_${ratio}.txt
done
