#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, redirect, session, flash
from datetime import datetime
from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__, template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    quantite = request.form.get('quantite')
    date = datetime.now().strftime('%Y-%m-%d')
    id_meuble = request.form.get('idArticle')
    id_user = session['user_id']

    sql = '''select * from panier P
             where P.id_PanierMeuble = %s and P.id_PanierUser = %s
             ;'''
    mycursor.execute(sql, (id_meuble, id_user))
    articles_panier = mycursor.fetchone()

    if (articles_panier is not None) and articles_panier['panier_quantite'] >= 1:
        sql = '''update panier set panier_quantite=panier_quantite+%s 
                 where id_PanierMeuble = %s and id_PanierUser = %s;'''
        tuple_edit = (quantite, id_meuble, id_user)
        mycursor.execute(sql, tuple_edit)
    else:
        sql = "insert into panier(panier_quantite,date_ajout,id_PanierMeuble,id_PanierUser) values (%s,%s,%s,%s);"
        tuple_edit = (quantite, date, id_meuble, id_user)
        mycursor.execute(sql, tuple_edit)

    get_db().commit()

    sql = '''update meubles M set M.nbStock = M.nbStock - %s where M.id_meuble = %s;'''
    mycursor.execute(sql, (quantite, id_meuble))
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_meuble = request.form.get('idArticle')
    id_user = session['user_id']

    sql = '''select panier_quantite from panier P
                 where P.id_PanierMeuble = %s and P.id_PanierUser = %s
                 ;'''
    mycursor.execute(sql, (id_meuble, id_user))
    quantite = mycursor.fetchone()

    if quantite['panier_quantite'] == 1:
        client_panier_delete_line()
        return redirect('/client/article/show')

    sql = '''update panier set panier_quantite=panier_quantite-1 where id_PanierMeuble = %s;'''
    mycursor.execute(sql, id_meuble)

    sql = '''update meubles M set M.nbStock = M.nbStock + 1  where M.id_meuble = %s;'''
    mycursor.execute(sql, id_meuble)
    get_db().commit()

    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_user = session['user_id']

    sql = '''select panier_quantite, id_PanierMeuble from panier where id_PanierUser = %s;'''
    mycursor.execute(sql, id_user)
    panier = mycursor.fetchall()

    for i in range(0, len(panier)):
        ligne_panier = panier[i]

        sql = '''update meubles M set M.nbStock = M.nbStock + %s where id_meuble = %s;'''
        mycursor.execute(sql, (ligne_panier['panier_quantite'], ligne_panier['id_PanierMeuble']))
        get_db().commit()

    sql = "delete from panier where id_PanierUser = %s;"
    mycursor.execute(sql, id_user)
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()

    id_meuble = request.form.get('idArticle')
    id_user = session['user_id']

    sql = '''select panier_quantite
                    from panier
                    where id_PanierMeuble = %s and id_PanierUser = %s;'''
    mycursor.execute(sql, (id_meuble, id_user))
    quantite = mycursor.fetchone()

    sql = '''update meubles M set M.nbStock = M.nbStock + %s where M.id_meuble=%s;'''
    mycursor.execute(sql, (quantite['panier_quantite'], id_meuble))
    get_db().commit()

    sql = '''delete from panier
             where id_PanierMeuble = %s;
          '''
    mycursor.execute(sql, id_meuble)
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u' votre Mot de recherché doit être composé uniquement de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')

    if filter_types and filter_types != []:
        print("filter_types:", filter_types)
        if isinstance(filter_types, list):
            check_filter_type = True
            for number_type in filter_types:
                print("test", number_type)
                if not number_type.isdecimal():
                    check_filter_type = False
                if check_filter_type:
                    session['filter_types'] = filter_types
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')