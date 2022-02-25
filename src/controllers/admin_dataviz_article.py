#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_dataviz_article = Blueprint('admin_dataviz_article', __name__, template_folder='templates')


@admin_dataviz_article.route('/admin/type-article/bilan-stock')
def show_type_article_stock():
    mycursor = get_db().cursor()
    types_articles_cout = []
    sql = '''select libelle_type from types_meubles;'''
    mycursor.execute(sql)
    labels = mycursor.fetchall()
    print(labels)
    values = []
    cout_total = 0
    return render_template('admin/dataviz/etat_type_article_stock.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total,
                           labels=labels, values=values)


@admin_dataviz_article.route('/admin/article/bilan')
def show_article_bilan():
    mycursor = get_db().cursor()
    sql = '''select t.id_type, t.libelle_type, count(m.id_meuble) as nbMeubleDispo, coalesce(sum(m.prix * m.nbStock),0)
        as coutStock
        from meubles m
        right join types_meubles t on t.id_type=m.id_MeubleType
        group by t.libelle_type, t.id_type
        order by t.libelle_type;'''
    mycursor.execute(sql)
    cout_stock = mycursor.fetchall()
    print(cout_stock)
    sql = '''select m.nbStock, coalesce(sum(m.prix * m.nbStock),0) as coutStock, count(m.id_meuble) as stockDispo
        from meubles m
        right join types_meubles t on t.id_type=m.id_MeubleType;'''
    mycursor.execute(sql)
    cout_stock_tot = mycursor.fetchall()
    return render_template('admin/dataviz/etat_article_vente.html', coutStock=cout_stock, coutStockTot=cout_stock_tot)
