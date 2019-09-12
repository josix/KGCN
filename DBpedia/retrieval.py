from SPARQLWrapper import SPARQLWrapper, TSV
from time import sleep

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
for i in range(0, 100*10000, 10000):
    query_string = "SELECT *\n\tWHERE {\n\t\t?movie ?relation ?property.  FILTER(?relation in (dbo:cinematography, dbo:country, dbo:director, dbo:distributor, dbo:editing, dbo:musicComposer, dbo:producer, dbo:starring, dbp:studio, dbp:writer))\n\t\t}\n\t\t\nOFFSET %d LIMIT 10000" % (i)
    sparql.setQuery(query_string)
    sparql.setReturnFormat(TSV)
    results = sparql.query().convert()
    sleep(1)

    print(results.decode('utf-8'), end = '')
