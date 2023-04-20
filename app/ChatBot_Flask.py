import json
import spacy
from flask import Flask, render_template, request, make_response, jsonify


app = Flask(__name__)

#config de spacy avec un modele pré entrainnée & liste de stop_word par defaut
nlp = spacy.load('fr_core_news_lg')
stop_words = nlp.Defaults.stop_words


history={'inputs': [], 'responses': []}

def OuvrirFichierJSon(filename):
    """_summary_
        Ouvre le fichier json soughaiter et stocks les data

    Args:
        filename (int): nom du fichier json

    Returns:
        liste: liste des données contenue dans le json
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def TraitementQuestionUser(input_text, nlp):
    """_summary_
        Permet de retirer les mots d'arret de la saisie utilisateur

    Args:
        input_text (string): texte issu saisie de l'utilisateur 

    Returns:
        liste NPL: Liste spaCy avec les mots non considerer comme mot d'arret issu de la saisie utilisateur
    """
    doc = nlp(input_text.lower())
    words = [token.text for token in doc if not token.is_stop]
    return words

def TraitementQuestionJson(question, nlp):
    """_summary_
    Permet de retirer les mots d'arret des question du fichier json
    
    Args:
        question (string): question stocké dans notre fichier json

    Returns:
        Liste NPL: _Liste SpaCy avec les mots principaux de la question
    """
    question_doc = nlp(question.lower())
    question_words = [token.text for token in question_doc if not token.is_stop]
    return question_words

def MeilleureReponse(input_words, data, nlp):
    """_summary_
    permet de trouver la meilleures reponse en comparant chaques question du fichier a notre input utilisateur 
     
    Args:
        input_words (NLP string): Saisie utilisateur issu du traitement NLP
        data (liste): liste des données du fichier json

    Returns:
        string: Meilleure réponse trouver pour la question de l'utilisateur 
    """
    max_similarity = 0
    best_response = ''
    for key in data:
        for question in data[key]["questions"]:
            for response in data[key]["réponses"]:
                question_words = TraitementQuestionJson(question, nlp)
                similarity = nlp(' '.join(input_words)).similarity(nlp(' '.join(question_words)))
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_response = response
    
    return best_response, max_similarity

def MinScore(best_reponse,max_similarity):
    """_summary_
    Verifie sir le score minimum est suffisament grand pour donner une réponse. 
    plus le score mini est proche de 1, plus la réponse certaine. Pour des raison de reformulation de l'utilisateur , 
    le score est ici placée  plutot bas.

    Args:
        best_reponse (_type_): _description_
        max_similarity (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    if max_similarity <0.2 :
        best_reponse="Aucune information. Essayer de rajouter du contexte dans votre phrase."
    else:
        best_reponse=best_reponse   
    return best_reponse

def tableauOUTPUT(input,response):
    global history
    history['inputs'].append(input)
    history['responses'].append(response)
    return history

def chatbot(user_input):
    """_summary_
    gestion de l'execution du programme 

    Args:
        user_input (string): message de l'utilisateur
    """
    filename = "DataChatBot.json" 
    data = OuvrirFichierJSon(filename)
    input_words = TraitementQuestionUser(user_input, nlp)
    best_response,maxSimilarity = MeilleureReponse(input_words, data, nlp)
    best_response=MinScore(best_response,maxSimilarity)
    return best_response

@app.route('/chat', methods=['POST'])
def chat():
    global history
    #history = json.loads(request.form.get('history', '{"inputs":[], "responses":[]}'))
    user_input = request.form['user_input']
    response = chatbot(user_input)
    history = tableauOUTPUT(user_input, response)
    return render_template('chat.html', history=history)



#main
chat 