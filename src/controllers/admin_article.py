#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                        template_folder='templates')

@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    articles = None
    # print(articles)
    return render_template('admin/article/show_article.html', articles=articles)

@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    types_articles = None
    return render_template('admin/article/add_article.html', types_articles=types_articles)

@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
   # type_article_id = int(type_article_id)
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description', '')
    image = request.form.get('image', '')


    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix, ' - stock:', stock, ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:'+nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - stock:'+  stock + ' - description:' + description + ' - image:' + image
    flash(message)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete', methods=['POST'])
def delete_article():
    # id = request.args.get('id', '')
    id = request.form.get('id', '')

    print("un article supprimé, id :", id)
    flash(u'un article supprimé, id : ' + id)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/edit/<int:id>', methods=['GET'])
def edit_article(id):
    mycursor = get_db().cursor()
    article = None
    types_articles = None
    return render_template('admin/article/edit_article.html', article=article, types_articles=types_articles)

@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    nom = request.form['nom']
    id = request.form.get('id', '')
    type_article_id = request.form.get('type_article_id', '')
    #type_article_id = int(type_article_id)
    prix = request.form.get('prix', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description', '')
    image = request.form.get('image', '')

    print(u'article modifié , nom : ', nom, ' - type_article:', type_article_id, ' - prix:', prix, ' - stock:', stock, ' - description:', description, ' - image:', image)
    message = u'article modifié , nom:'+nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - stock:'+  stock + ' - description:' + description + ' - image:' + image
    flash(message)
    return redirect(url_for('admin_article.show_article'))
