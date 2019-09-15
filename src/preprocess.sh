#!/bin/bash

if [ $# != 1 ]
then
  echo "USAGE: ./experiment.sh {DBpedia | IMDb}";
  exit 1
fi

KG="$1"

case $KG in
  DBpedia)
    ;;
  IMDb)
    ;;
   *)
    echo "USAGE: ./experiment.sh {DBpedia | IMDb}"
    exit 1
esac

if [ -e ../data/movie/kg.txt ]
then
  rm ../data/movie/kg.txt
  ln -s "../../${KG}/kg.txt" ../data/movie/kg.txt
fi

for ratio in `seq 0.0 0.25 1.0`
do
  echo "Runing $ratio..."
  if [ -e ../data/movie/item_index2entity_id.txt ]
  then
    rm ../data/movie/item_index2entity_id.txt
    ln -s "../../${KG}/item_index2entity_id_ratio_${ratio}.txt"  ../data/movie/item_index2entity_id.txt
  fi
  python3 ./preprocess.py -d movie > ${ratio}_desc.txt
  DATA_DIR="items_ratio_${ratio}"
  mkdir -p ../data/movie/${KG}/$DATA_DIR
  mv ../data/movie/*_final.txt ${ratio}_desc.txt ../data/movie/${KG}/$DATA_DIR
done
