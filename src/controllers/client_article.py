#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')      # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()

    id_user = session['user_id']

    sql = 'select * from types_meubles;'
    mycursor.execute(sql)
    types_articles = mycursor.fetchall()

    username = session['user_id']
    sql = '''select M.nom, M.id_meuble, P.panier_quantite, M.prix, M.nbStock
             from panier P
             inner join meubles M on M.id_meuble = P.id_PanierMeuble
             where P.id_PanierUser = %s
             ;'''
    mycursor.execute(sql, username)
    articles_panier = mycursor.fetchall()

    sql = '''select M.id_meuble,M.nom,M.prix,M.nbStock,M.image,coalesce(count(A.libelle_avis),0) as nb_avis,
           coalesce(count(A.note),0) as nb_notes,avg(A.note) as moy_notes
           from meubles M
           left join avis A on A.id_AvisMeuble = id_meuble
         '''
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " where "
    if "filter_word" in session:
        sql = sql + "nom like %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = "and "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + "prix between %s and %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = "and "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "id_MeubleType = %s "
            if item != last_item:
                sql = sql + "or "
            list_param.append(item)
        sql = sql + ")"
    sql = sql + "group by M.id_meuble,M.nom,M.prix,M.nbStock,M.image;"
    tuple_sql = tuple(list_param)
    mycursor.execute(sql, tuple_sql)
    meubles = mycursor.fetchall()

    sql = '''select sum(M.prix * P.panier_quantite) as sous_total 
            from panier P
            inner join meubles M on M.id_meuble = P.id_PanierMeuble
            where P.id_PanierUser = %s;'''
    mycursor.execute(sql, id_user)
    prix_total = mycursor.fetchone()['sous_total']
    return render_template('client/boutique/panier_article.html', articlesPanier=articles_panier, meubles=meubles,
                           prix_total=prix_total, itemsFiltre=types_articles)


@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()

    sql = '''select id_meuble, nom, prix, image
             from meubles
             where id_meuble = %s;
          '''
    mycursor.execute(sql, id)
    article = mycursor.fetchall()

    sql = '''select libelle_avis, id_AvisUser, note, id_AvisMeuble, id_avis
             from avis
             where id_AvisMeuble = %s;
          '''
    mycursor.execute(sql, id)
    commentaires = mycursor.fetchall()

# ====================================================================================================================== dans html cmd | lenght ???
    id_user = session['user_id']
    sql = '''select count(C.id_cmd) as qte
             from ligne_de_commande L
             inner join commande C on C.id_cmd = L.id_LigneCmd
             inner join user U on U.id_User = C.id_CmdUser
             where L.id_LigneMeuble = %s and U.id_user = %s;
          '''
    mycursor.execute(sql, (id, id_user))
    commandes_articles = mycursor.fetchone()
    print(commandes_articles)
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires,
                           commandes_articles=commandes_articles)
