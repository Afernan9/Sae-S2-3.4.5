#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, redirect, url_for
from flask import render_template, request

from connexion_db import get_db

admin_dataviz_article = Blueprint('admin_dataviz_article', __name__, template_folder='templates')


@admin_dataviz_article.route('/admin/type-article/bilan-stock')
def show_type_article_stock():
    mycursor = get_db().cursor()
    sql = '''select t.id_type, t.libelle_type, coalesce(sum(c.nbStock), 0) as nbMeubleDispo, coalesce(sum(m.prix * c.nbStock),0)
            as coutStock
            from meubles m
            right join types_meubles t on t.id_type=m.id_MeubleType
            left join colore c on c.id_ColoreMeuble = m.id_meuble
            group by t.id_type
            order by t.libelle_type
            ;'''
    mycursor.execute(sql)
    cout_stock = mycursor.fetchall()
    print(cout_stock)
    sql = '''select c.nbStock, coalesce(sum(m.prix * c.nbStock),0) as coutStock, count(m.id_meuble) as stockDispo
            from meubles m
            left join types_meubles t on t.id_type=m.id_MeubleType
            left outer join colore c on c.id_ColoreMeuble = m.id_meuble
            ;'''
    mycursor.execute(sql)
    cout_stock_tot = mycursor.fetchall()


    return render_template('admin/dataviz/etat_type_article_stock.html',
                           cout_stock=cout_stock, cout_stock_tot=cout_stock_tot)


@admin_dataviz_article.route('/admin/article/bilan')
def show_article_bilan():
    mycursor = get_db().cursor()
    sql = '''select nom, c.nbStock
            from meubles
            inner join colore c on c.id_ColoreMeuble = id_meuble
            ;'''
    mycursor.execute(sql)
    meubles = mycursor.fetchall()
    labels = [str(row['nom']) for row in meubles]
    values = [str(row['nbStock']) for row in meubles]
    print(values, labels)
    return render_template('admin/dataviz/etat_article_vente.html',
                           labels=labels, values=values)


@admin_dataviz_article.route('/admin/article/adressbilan')
def show_adress_bilan():
    mycursor = get_db().cursor()
    sql = '''select PR.ville, sum(prix_unit * quantite) as price
            from commande C
            inner join pointRelais PR on PR.id_pointRelais = C.id_PointRelais
            inner join ligne_de_commande lc on lc.id_LigneCmd = C.id_cmd
            group by PR.ville;'''
    mycursor.execute(sql)
    rqt = mycursor.fetchall()
    labels = [str(row['ville']) for row in rqt]
    values = [str(row['price']) for row in rqt]
    print(values, labels)
    return render_template('admin/dataviz/livraison.html',
                           labels=labels, values=values)


@admin_dataviz_article.route('/admin/avis', methods=['GET'])
def show_avis():
    mycursor = get_db().cursor()
    sql = '''select * 
        from avis a
        inner join meubles m on m.id_meuble = a.id_AvisMeuble
        inner join user u on u.id_User = a.id_AvisUser;'''
    mycursor.execute(sql)
    avis = mycursor.fetchall()
    return render_template('admin/avis/avis.html', avis=avis)



@admin_dataviz_article.route('/admin/avis/del', methods=['GET'])
def del_avis():
    avis = request.args.get('id_avis')
    mycursor = get_db().cursor()
    sql = '''DELETE FROM avis 
            WHERE id_avis = %s;'''
    mycursor.execute(sql, avis)
    get_db().commit()
    return redirect(url_for('admin_dataviz_article.show_avis'))