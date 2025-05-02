import json
import requests

def query_graphdb(endpoint_url, sparql_query):
    # Set up the headers
    headers = {
        'Accept': 'application/json',  # You can change this based on the response format you need
    }
    
    # Make the GET request to the GraphDB endpoint
    response = requests.get(endpoint_url, params={'query': sparql_query}, headers=headers)
    
    if response.status_code == 200 or response.status_code == 206 or response.status_code == 500:
        return response.json()  # Return the JSON response from the GraphDB endpoint
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

endpoint = "http://dbpedia.org/sparql"

# Query que seleciona os filmes e devolve informação básica sobre os mesmos
# ?g e ?s presentes para filtrar os filmes que contenham essa informação
sparql_query = """
select distinct ?movie ?titulo ?pais ?realizador ?abs ?dataLancamento where {
    ?movie a dbo:Film ;
           rdfs:label ?titulo ;
           dbp:country ?pais ;
           dbo:director/rdfs:label ?realizador ;
           dbo:abstract ?abs;
           dbo:releaseDate ?dataLancamento ;
           dbo:genre ?g;
           dbo:starring ?s.

    filter(lang(?titulo)="en")
    filter(lang(?pais)="en")
    filter(lang(?realizador)="en")
    filter(lang(?abs)="en")
} LIMIT 100
"""

result = query_graphdb(endpoint, sparql_query)
movies = result["results"]["bindings"]

dataset = []
for m in movies:
    m = m["movie"]["value"]

    genres_query = f"""
    select distinct ?genre where {{
    <{m}> dbo:genre/rdfs:label ?genre .
    filter(lang(?genre) = "en")
    }}
    """

    result2 = query_graphdb(endpoint, genres_query)
    generos = []
    for genre in result2["results"]["bindings"]:
        generos.append(genre["genre"]["value"])

    actors_query = f"""
    select distinct ?actor ?nome ?data ?origem where {{
      <{m}> dbo:starring ?actor.
        ?actor rdfs:label ?nome;
                dbo:birthDate ?data;
                dbo:birthPlace/rdfs:label ?origem.
    filter(lang(?nome) = "en")
    filter(lang(?origem) = "en")
    }}
    """

    result3 = query_graphdb(endpoint, actors_query)
    actors = []
    for actor in result3["results"]["bindings"]:
        actors.append({
            "id": actor["actor"]["value"],
            "nome": actor["nome"]["value"],
            "dataNasc": actor["data"]["value"],
            "origem": actor["origem"]["value"],
        })

    dataset.append({
        "id": m,
        "titulo": result["results"]["bindings"][0]["titulo"]["value"],
        "pais": result["results"]["bindings"][0]["pais"]["value"],
        "dataLancamento": result["results"]["bindings"][0]["dataLancamento"]["value"],
        "realizador": result["results"]["bindings"][0]["realizador"]["value"],
        "abstract": result["results"]["bindings"][0]["abs"]["value"],
        "genero": generos,
        "elenco": actors
    })

with open("movies.json", "w") as fout:
    json.dump(dataset, fout, ensure_ascii=False, indent=2)