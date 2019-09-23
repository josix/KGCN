import subprocess
import random
import re
import argparse
import concurrent.futures as cf


def get_mapping(dbpedia_id):
    command = 'grep -P "\\"{}\\"\\t" ./mappingToEntityId.tsv'.format(
            re.sub('\)', "\)",
                re.sub('\(', "\(",
                    dbpedia_id)
                )
            )
    try:
        output = subprocess.check_output(command, shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        return
    _, kg_id = output.strip().split('\t')
    return kg_id

parser = argparse.ArgumentParser()
parser.add_argument('-r', type=float, default=0.0, help='ratio of missing items')
args = parser.parse_args()
RATIO = 1 - args.r

with open('../ml-1m/ratining.csv') as fin:
    fin.readline()
    ALL_ITEMS = {line.strip().split(',')[1] for line in fin}


with open('item_index2entity_id_ratio_{:.2f}.txt'.format(RATIO), 'wt') as fout:
    future_to_movie = {}
    with cf.ProcessPoolExecutor(max_workers=50) as executor:
        with open('./MappingMovielens2DBpedia-1.2.tsv') as fin:
            fin.readline()
            for line in fin:
                movie_id, _, dbpedia_id = line.strip().split('\t')
                if movie_id in ALL_ITEMS:
                    future_to_movie[executor.submit(get_mapping, dbpedia_id)] = movie_id
        output:list = []
        for future in cf.as_completed(future_to_movie):
            movie_id = future_to_movie[future]
            kg_id = future.result()
            if kg_id:
                output.append('{}\t{}'.format(movie_id, kg_id))
    random.shuffle(output)
    fout.write("\n".join(output[:int(len(output)*(RATIO))]))
