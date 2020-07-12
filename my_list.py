# -*- coding: utf-8 -*-

import time
import database
import requests
import datetime
import main
from bs4 import BeautifulSoup


def home():
    print("""
    1 - Ajouter Société
    2 - Supprimer Société
    3 - Liste Société
    0 - Retour""")
    choose = input("\nAction que vous voulez effectuer : ")
    if choose == "0":
        main.main()
    elif choose == "1":
        add_society()
    elif choose == "2":
        delete_society()
    elif choose == "3":
        list_society()
    else:
        print("\nMerci de choisir un choix valide")
        time.sleep(2)
        home()


def add_society():
    code = input("Code de la société a rajouter : ")
    url = "https://www.boursorama.com/cours/" + code
    req = requests.get(url)
    if "cours" in req.url:
        soup = BeautifulSoup(req.content, 'html.parser')
        name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
        sql = """INSERT INTO my_list ('name', 'code') VALUES ('{n}', '{c}')""".format(n=name, c=code)
        request = database.insert_data(sql)
        if request == "good":
            print("Ajout Compagnie Nom: {n}; Code: {c}".format(n=name, c=code))
    else:
        print("Code Société Erreur")
    time.sleep(2)
    home()


def delete_society():
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    if len(results) > 0:
        i = 1
        for result in results:
            print("{} - Name: {}; Code: {}".format(i, result[1], result[2]))
            i += 1
        print("0 - Retour")
        choose = input("Quelle société voulez-vous enlever ? ")
        choose = int(choose)
        if choose == 0:
            home()
        if 0 < choose <= len(results):
            database.delete("company", results[choose - 1])
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def list_society():
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    if len(results) > 0:
        for result in results:
            print("Nom: {}; Code: {}".format(result[1], result[2]))
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()