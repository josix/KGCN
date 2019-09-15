import subprocess
import random
import argparse
import concurrent.futures as cf

def get_mapping(imdb_id):
    command = "grep 'tt{}\t' ./mappingToEntityId.tsv".format(imdb_id)
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

with open('item_index2entity_id_ratio_{:.2f}.txt'.format(RATIO), 'wt') as fout:
    future_to_movie = {}
    with cf.ProcessPoolExecutor(max_workers=50) as executor:
        with open('./links.csv') as fin:
            fin.readline()
            for line in fin:
                movie_id, imdb_id, *_ = line.strip().split(',')
                future_to_movie[executor.submit(get_mapping, imdb_id)] = movie_id
        output:list = []
        for future in cf.as_completed(future_to_movie):
            movie_id = future_to_movie[future]
            kg_id = future.result()
            if kg_id:
                output.append('{}\t{}'.format(movie_id, kg_id))
    random.shuffle(output)
    fout.write("\n".join(output[:int(len(output)*(RATIO))]))
