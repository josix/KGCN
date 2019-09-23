from SPARQLWrapper import SPARQLWrapper, TSV
from time import sleep

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
RELATIONS = ["dbo:cinematography", "dbo:country", "dbo:director", "dbo:distributor", "dbo:editing", "dbo:musicComposer", "dbo:producer", "dbo:starring", "dbo:studio", "dbo:writer"]
for relation in RELATIONS:
    for i in range(0, 5*10000, 10000):
        query_string = "SELECT *\n\tWHERE {\n\t\t?movie ?relation ?property.  FILTER(?relation in (%s))\n\t\t}\n\t\t\nOFFSET %d LIMIT 10000" % (relation, i)
        sparql.setQuery(query_string)
        sparql.setReturnFormat(TSV)
        results = sparql.query().convert()
        sleep(1)
        output = results.decode('utf-8')
        first_line_pos = output.index("\n")
        print(output[first_line_pos+1:], end="")

