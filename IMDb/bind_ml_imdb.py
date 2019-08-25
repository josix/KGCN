import subprocess
import concurrent.futures as cf

def get_mapping(imdb_id):
    command = "grep 'tt{}\t' ./mappingToEntityId.tsv".format(imdb_id)
    try:
        output = subprocess.check_output(command, shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        return
    _, kg_id = output.strip().split('\t')
    return kg_id

with open('item_index2entity_id.txt', 'wt') as fout:
    future_to_movie = {}
    with cf.ProcessPoolExecutor(max_workers=50) as executor:
        with open('./links.csv') as fin:
            fin.readline()
            for line in fin:
                movie_id, imdb_id, *_ = line.strip().split(',')
                future_to_movie[executor.submit(get_mapping, imdb_id)] = movie_id
        for future in cf.as_completed(future_to_movie):
            movie_id = future_to_movie[future]
            kg_id = future.result()
            if kg_id:
                fout.write('{}\t{}\n'.format(movie_id, kg_id))
