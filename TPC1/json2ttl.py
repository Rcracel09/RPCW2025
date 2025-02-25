import json

f = open ("emd.json")
emds = json.load(f)

output = ""
modalidades = {}
clubes = {}
pessoas = {}

#enumerate transforme uma lista em tuplos (chekcs)
for i,e in enumerate(emds):

    if e['email'] not in pessoas:
        pessoas[e['email']] = "P" + str(len(pessoas))
        output += f"""
###  http://www.semanticweb.org/user/ontologies/2025/1/EMD#{"P" + str(len(pessoas))}
:P{"P" + str(len(pessoas))} rdf:type owl:NamedIndividual ,
             :Pessoa ;
    :email "{e['email']}" ;
    :genero "{e['género']}" ;
    :idade {e['idade']} ;
    :morada "{e['morada']}" ;
    :nome "{e["nome"]["primeiro"]} {e["nome"]["último"]}" .
        """
    idPessoa = pessoas[e['email']]

    #Tratamento Clube
    if e['clube'] not in clubes:
        clubes[e['clube']] = "C" + str(len(clubes))
        output += f"""
        ###  http://www.semanticweb.org/user/ontologies/2025/1/EMD#{"C" + str(len(clubes))}
:{"C" + str(len(clubes))} rdf:type owl:NamedIndividual ,
             :Clube ;
    :temAtleta :{idPessoa} ;
    :nome "{e['clube']}" .
        """
    idClube = clubes[e['clube']]

    #Tratamento Modalidade
    if e['modalidade'] not in modalidades:
        modalidades[e['modalidade']] = "M" + str(len(modalidades))
        output += f"""
        ###  http://www.semanticweb.org/user/ontologies/2025/1/EMD#{modalidades[e['modalidade']]}
:{modalidades[e['modalidade']]} rdf:type owl:NamedIndividual ,
             :Modalidade ;
    :temExame :E{i} ;
    :éPraticadaPor :P{idPessoa} ;
    :éPraticadoEm :C{idPessoa} ;
    :nome "{e['modalidade']}" .
        """
    else: 
        output += f"""
        :{modalidades[e['modalidade']]}:temExame :E{i} ;
                                       :éPraticadaPor :P{idPessoa} ;
                                       :éPraticadoEm :C{idPessoa} .
        """

    output += f"""
###  http://www.semanticweb.org/user/ontologies/2025/1/EMD#E{i}
:E{i} rdf:type owl:NamedIndividual ,
             :Exame ;
    :éRealizadoPor :{idPessoa} ;
    :dataEMD "{e['dataEMD']}" ;
    :resultado "{str(e['resultado']).lower()}"^^xsd:boolean .

"""
print(output)