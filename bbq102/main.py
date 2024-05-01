import requests
from bs4 import BeautifulSoup
import ctypes  # An included library with Python install.   
accent_map = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"} 
URL_SLACK_GROUPE="https://hooks.slack.com/services/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"
URL_SLACK_MAX = "https://hooks.slack.com/services/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"
# Fonction pour récupérer la liste depuis la page web
def get_list():
    url = 'https://bbqquebec.com/collections/boutique-bbqquebec-cours-et-evenements-cours-en-personne/products/cours-bbq-102'
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Supposons que la liste est dans une balise ul avec des éléments li
        listebs = soup.find_all('label', class_='opt-label opt-label--btn btn relative text-center')
        listeVille =[]
        for itm in listebs:
            if itm.has_attr('for'):
                attr = itm['for']
                if "main-ville-opt" in attr:
                    listeVille.append(itm.text)

        return listeVille
    else:
        print("Erreur lors de la récupération de la page :", response.status_code)
        return None


def validerVille(listeVille):
    for itm in listeVille:
        if "quebec" in remove_accents(itm.lower()) or "levis" in remove_accents(itm.lower()):
            return True


def remove_accents(input_str):
  for char in accent_map:
    input_str = input_str.replace(char, accent_map[char])
  return input_str


def postSlack(strListVille,url):

    payload = {
        "text": strListVille
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Message envoyé avec succès à Slack")
    else:
        print("Erreur lors de l'envoi du message à Slack :", response.status_code)
        print("Message envoyé :", strListVille)
        print("Payload :", payload)
        print("Headers :", headers)
        print("Réponse :", response.text)
        print("Réponse HTTP :", response.status_code)
        print("Headers :", response.headers)    


liste_ville = get_list()
strListVille = "".join(liste_ville)  
postSlack(strListVille,URL_SLACK_GROUPE)



if validerVille(liste_ville) :
    msg = "C'EST LE TEMPS DE RESERVER LE COURS BBQ 102!! \n \n Disponibilités : \n" + strListVille
    postSlack(msg,URL_SLACK_GROUPE) 
else : 
    print("ville non valides")
