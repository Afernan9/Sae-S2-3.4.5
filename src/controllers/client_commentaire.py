#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, redirect, flash

from connexion_db import get_db

client_commentaire = Blueprint('client_commentaire', __name__, template_folder='templates')


@client_commentaire.route('/client/comment/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    libelle = request.form.get('commentaire')
    note = request.form.get('note')
    if not libelle or not note:
        flash('Valeures incorrectes')
        return redirect('/client/article/details/'+article_id)
    id_user = request.form.get('idUser', None)
    tuple_insert = (libelle, note, id_user, article_id)
    sql = '''insert into avis(libelle_avis, note, id_AvisUser, id_AvisMeuble) values(%s,%s,%s,%s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details/'+article_id)


@client_commentaire.route('/client/comment/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    id_avis = request.form.get('idAvis', None)
    sql = "delete from avis where id_avis = %s;"
    mycursor.execute(sql, id_avis)
    get_db().commit()

    return redirect('/client/article/details/'+article_id)
