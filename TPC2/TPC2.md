

### Foi usado em todas as queries este PREFIX

```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
```

### Quantos triplos existem na Ontologia?
A ontologia tem 6603 triplos

```
select (count (*) as ?count) {
    ?a ?p ?s .
}
```

### Que classes estão definidas?

```
select ?class where {
   ?class rdf:type owl:Class
} 
```

### Que propriedades tem a classe "Rei"?

```
select distinct ?prop where {
    ?s a :Rei .
    ?s ?prop ?o .
}
```

### Quantos reis aparecem na ontologia?

```
select (count(distinct ?reis) as ?count) {
    ?reis rdf:type :Rei .
} 
```

### Calcula uma tabela com o seu nome, data de nascimento e cognome.

```
select ?nome ?data_nascimento ?cognome where {
    ?reis rdf:type :Rei .
    ?reis :nome ?nome .
    ?reis :nascimento ?data_nascimento .
    ?reis :cognomes ?cognome .
}
```


### Acrescenta à tabela anterior a dinastia em que cada rei reinou.

```
select ?nome ?data_nascimento ?cognome ?dinastia where {
    ?reis rdf:type :Rei ;
    	 :nome ?nome ;
    	 :nascimento ?data_nascimento ;
    	 :cognomes ?cognome .
    ?reinado :temMonarca ?reis ;
     	:dinastia ?dinastia .
}
```

### Qual a distribuição de reis pelas 4 dinastias?

```
select ?dinastia (count(distinct ?reis) as ?count) where {
    ?reis rdf:type :Rei .
    ?reinado :temMonarca ?reis ;
     		:dinastia ?dinastia .
}
group by ?dinastia order by ?count
```


### Lista os descobrimentos (sua descrição) por ordem cronológica.

```
select ?Data ?Descrição where {
    ?descobrimento rdf:type :Descobrimento .
    ?descobrimento :data ?Data ;
    			 :notas ?Descrição .
} order by ?Data
```


### Lista as várias conquistas, nome e data, juntamento com o nome que reinava no momento.


```
select ?conquista ?nome ?data ?nome_rei where {
    ?conquista rdf:type :Conquista;
            :nome ?nome;
            :data ?data;
    		:temReinado ?reinado .
    ?reinado :temMonarca ?rei .
    ?rei     rdf:type :Rei ;
    	 	 :nome ?nome_rei .
            
}
```


### Calcula uma tabela com o nome, data de nascimento e número de mandatos de todos os presidentes portugueses.

select ?nome ?data_nascimento (count(distinct ?num_mandatos) as ?Mandatos) where {
    ?presidente rdf:type :Presidente;
    			:nome ?nome;
    			:nascimento ?data_nascimento;
    			:mandato ?num_mandatos.
} group by ?nome ?data_nascimento


### Quantos mandatos teve o presidente Sidónio Pais? Em que datas iniciaram e terminaram esses mandatos?

```
select ?data_inicio ?data_fim (count(distinct ?mandato) as ?Mandatos) where {
    ?presidente rdf:type :Presidente;
    			:nome "Sidónio Bernardino Cardoso da Silva Pais";
    			:mandato ?mandato.
    ?mandato :comeco ?data_inicio;
    		 :fim ?data_fim.    
} group by ?presidente ?data_inicio ?data_fim

```


### Quais os nomes dos partidos políticos presentes na ontologia?

```
select ?nome_partido where {
    ?partido rdf:type :Partido;
    	:nome ?nome_partido.
} 
```


### Qual a distribuição dos militantes por cada partido político?

```
select ?nome_partido (count (distinct ?militante) as ?Militantes) where {
    ?partido rdf:type :Partido;
    	:nome ?nome_partido;
        :temMilitante ?militante .
} group by ?nome_partido
```

### Qual o partido com maior número de presidentes militantes?

select ?nome_partido (count (distinct ?militante) as ?Militantes) where {
    ?partido rdf:type :Partido;
    	:nome ?nome_partido;
        :temMilitante ?militante .
} group by ?nome_partido order by desc(?Militantes) limit 1
