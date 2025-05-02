# TPC4 - Construção de um dataset sobre cinema a partir da DBPedia.

## Objetivo
Desenvolver um script Python para extrair informações sobre filmes a partir do endpoint SPARQL do DBpedia e armazená-las em formato JSON.

## Implementação
Foi criado um script Python que realiza as seguintes operações:

1. Efetua consultas SPARQL ao endpoint do DBpedia
2. Extrai informações básicas sobre filmes como título, país, data de lançamento, diretor e sinopse
3. Para cada filme, obtém informações adicionais sobre:
   - Elenco (nome, data de nascimento e local de nascimento)
   - Gêneros cinematográficos
4. Organiza todas as informações em uma estrutura de dados
5. Exporta os dados para um arquivo JSON formatado


## Conclusão
O script desenvolvido permite a extração de um conjunto rico de dados sobre filmes a partir de uma fonte aberta de conhecimento