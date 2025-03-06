# Backend & Frontend: app.py (Flask with Jinja templates)
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
# from SPARQLWrapper import SPARQLWrapper, JSON
import random
from tabulate import tabulate
import requests
import certifi



def query_graphdb(endpoint_url, sparql_query):
    # Set up the headers
    headers = {
        'Accept': 'application/json',  # You can change this based on the response format you need
    }
    
    # Make the GET request to the GraphDB endpoint
    response = requests.get(endpoint_url, params={'query': sparql_query}, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response from the GraphDB endpoint
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)


# endpoint = "http://localhost:7200/repositories/HistoriaPT"
# sparql_query_Reis_Nascimento_Cognome = """
#     PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
#     select ?nome ?data_nascimento ?cognome where {
#         ?reis rdf:type :Rei .
#         ?reis :nome ?nome .
#         ?reis :nascimento ?data_nascimento .
#         ?reis :cognomes ?cognome .
# }
# """
# result_reis = query_graphdb(endpoint, sparql_query_Reis_Nascimento_Cognome)

# listaReis_Nascimento_Cognome = []
# for r in result_reis['results']['bindings']:
#     t = (r['nome']['value'].split('#')[-1], r['data_nascimento']['value'].split('#')[-1], r['cognome']['value'].split('#')[-1])
#     listaReis_Nascimento_Cognome.append(t)


# print(tabulate(listasPresidentes_Nascimento_Nmandatos, tablefmt='fancy_grid'))

def fetch_questions_from_King_name():
    endpoint = "http://localhost:7200/repositories/HistoriaPT"
    sparql_query_Reis_Nascimento_Cognome = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        select ?nome ?data_nascimento ?cognome where {
            ?reis rdf:type :Rei .
            ?reis :nome ?nome .
            ?reis :nascimento ?data_nascimento .
            ?reis :cognomes ?cognome .
    }
    """
    result_reis = query_graphdb(endpoint, sparql_query_Reis_Nascimento_Cognome)

    listaReis_Nascimento_Cognome = []
    for r in result_reis['results']['bindings']:
        t = (r['nome']['value'].split('#')[-1], r['data_nascimento']['value'].split('#')[-1], r['cognome']['value'].split('#')[-1])
        listaReis_Nascimento_Cognome.append(t)
    
    #Escolha Multipla sobre a data de Nascimento
    questions = []
    for current in listaReis_Nascimento_Cognome:
        nome = current[0]
        data_nascimento = current[1]
        cognome = current[2]
        question_text = f"Quando nasceu o rei {nome}?"
        options = [data_nascimento]
        while len(options) < 4:
            numero = random.randint(0, len(listaReis_Nascimento_Cognome) - 1)
            random_birth = listaReis_Nascimento_Cognome[numero][1]
            if random_birth not in options:
                options.append(random_birth)
        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": data_nascimento
        })
    
    #Verdadeiro e Falso sobre a data de Nascimento
    for current in listaReis_Nascimento_Cognome:
        nome = current[0]
        data_nascimento = current[1]
        cognome = current[2]
        number = random.randint(0,1)
        options = []
        options.append(f"Verdadeiro")
        options.append(f"Falso")
        if(number == 1):
            question_text = f"O rei {nome} nasceu em {data_nascimento}"
            answer = f"Verdadeiro"
        else:
            numero = random.randint(0, len(listaReis_Nascimento_Cognome) - 1)
            random_birth = listaReis_Nascimento_Cognome[numero][1]
            question_text = f"O rei {nome} nasceu em {random_birth}"
            answer = f"Falso"
        
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })

    #Escolha Multipla sobre o cognome do Rei
    for current in listaReis_Nascimento_Cognome:
        nome = current[0]
        data_nascimento = current[1]
        cognome = current[2]
        question_text = f"Qual o cognome do rei {nome}?"
        options = [cognome]
        while len(options) < 4:
            numero = random.randint(0, len(listaReis_Nascimento_Cognome) - 1)
            random_birth = listaReis_Nascimento_Cognome[numero][2]
            if random_birth not in options:
                options.append(random_birth)
        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": cognome
        })
    
    # **Selecionar 15 perguntas aleatórias**
    total_questions = min(15, len(questions))  # Evita erro se houver menos de 15 perguntas
    questions = random.sample(questions, total_questions)

    return questions

def fetch_questions_from_President_name():
    endpoint = "http://localhost:7200/repositories/HistoriaPT"
    sparql_query_Presidente_Nascimento_Nmandatos = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        select ?nome ?data_nascimento (count(distinct ?num_mandatos) as ?Mandatos) where {
        ?presidente rdf:type :Presidente;
        			:nome ?nome;
        			:nascimento ?data_nascimento;
        			:mandato ?num_mandatos.
    } group by ?nome ?data_nascimento
    """

    result_presidentes = query_graphdb(endpoint, sparql_query_Presidente_Nascimento_Nmandatos)

    listasPresidentes_Nascimento_Nmandatos = []
    for r in result_presidentes['results']['bindings']:
        t = (r['nome']['value'].split('#')[-1], r['data_nascimento']['value'].split('#')[-1], r['Mandatos']['value'].split('#')[-1])
        listasPresidentes_Nascimento_Nmandatos.append(t)

    #Escolha Multipla sobre a data de Nascimento
    questions = []
    for current in listasPresidentes_Nascimento_Nmandatos:
        nome = current[0]
        data_nascimento = current[1]
        Nmandatos = current[2]
        question_text = f"Quando nasceu o presidente {nome}?"
        options = [data_nascimento]
        while len(options) < 4:
            numero = random.randint(0, len(listasPresidentes_Nascimento_Nmandatos) - 1)
            random_birth = listasPresidentes_Nascimento_Nmandatos[numero][1]
            if random_birth not in options:
                options.append(random_birth)
        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": data_nascimento
        })
    
    #Verdadeiro e Falso sobre a data de Nascimento
    for current in listasPresidentes_Nascimento_Nmandatos:
        nome = current[0]
        data_nascimento = current[1]
        Nmandatos = current[2]
        number = random.randint(0,1)
        options = []
        options.append(f"Verdadeiro")
        options.append(f"Falso")
        if(number == 1):
            question_text = f"O presidente {nome} nasceu em {data_nascimento}"
            answer = f"Verdadeiro"
        else:
            numero = random.randint(0, len(listasPresidentes_Nascimento_Nmandatos) - 1)
            random_birth = listasPresidentes_Nascimento_Nmandatos[numero][1]
            question_text = f"O presidente {nome} nasceu em {random_birth}"
            answer = f"Falso"
        
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })

    #Escolha Multipla sobre o numero de mandatos do Presidente
    for current in listasPresidentes_Nascimento_Nmandatos:
        nome = current[0]
        data_nascimento = current[1]
        Nmandatos = current[2]
        question_text = f"Quantos mandatos teve o Presidente {nome}?"
        options = []
        i = 1
        while len(options) < 4:
            options.append(i)
            i+=1

        questions.append({
            "question": question_text,
            "options": options,
            "answer": Nmandatos
        })

    # **Selecionar 15 perguntas aleatórias**
    total_questions = min(15, len(questions))  # Evita erro se houver menos de 15 perguntas
    questions = random.sample(questions, total_questions)

    return questions


@app.route('/')
def home():
    session['score'] = 0
    questions = []
    questions.extend(fetch_questions_from_President_name())
    questions.extend(fetch_questions_from_King_name())
    session['questions'] = questions
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_text = request.form.get('question')
        
        for question in session.get('questions', []):
            if question['question'] == question_text:
                correct = question['answer'] == user_answer
                session['score'] = session.get('score', 0) + (1 if correct else 0)
                return render_template('result.html', correct=correct, correct_answer=question['answer'], score=session['score'])
    
    if session.get('questions'):
        numero = random.randint(0, len(session['questions']) - 1)
        question = session['questions'].pop(numero)
        return render_template('quiz.html', question=question)
    else:
        return redirect(url_for('score'))

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True)