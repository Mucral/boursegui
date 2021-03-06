# -*- coding: utf-8 -*-

import time
import database
import requests
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
    print()
    code = input("Url ou Code de la société à rajouter : ")
    if "boursorama.com" in code:
        url = code
        code = code.split("/")[4]
    else:
        url = "https://www.boursorama.com/cours/" + code
    req = requests.get(url)
    if "cours" in req.url:
        soup = BeautifulSoup(req.content, 'html.parser')
        name = soup.find(class_="c-faceplate__company-link").text.replace(" ", "").replace("\n", "")
        sql = """INSERT INTO my_list ('name', 'code') VALUES ('{n}', '{c}')""".format(n=name, c=code)
        request = database.insert(sql)
        if request == "good":
            print("\nAjout Compagnie\n{n} {u}".format(n=name, c=code, u=url))
    else:
        print("Code Société Erreur")
    time.sleep(2)
    home()


def delete_society():
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    print()
    if len(results) > 0:
        i = 1
        for result in results:
            url = "https://www.boursorama.com/cours/{}/".format(result[2])
            print("{} - {}  {}".format(i, result[1], url))
            i += 1
        print("0 - Retour\n")
        choose = input("Quelle société voulez-vous enlever ? ")
        if choose.isdigit():
            choose = int(choose)
            if choose == 0:
                home()
            if 0 < choose <= len(results):
                sql = "DELETE FROM my_list WHERE id={i}".format(i=results[choose - 1][0])
                request = database.delete(sql)
                if request == "delete":
                    print("Société Supprimée {}".format(results[choose - 1][1]))
            time.sleep(2)
            home()
        else:
            print("Merci de rentrer une valeut correcte")
            time.sleep(2)
            delete_society()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()


def list_society():
    sql = "SELECT * FROM my_list"
    results = database.select(sql)
    print()
    if len(results) > 0:
        for result in results:
            url = "https://www.boursorama.com/cours/{}/".format(result[2])
            print("- {}  {}".format(result[1], url))
        time.sleep(2)
        home()
    else:
        print("\nAucune Entreprise dans la liste")
        time.sleep(2)
        home()
