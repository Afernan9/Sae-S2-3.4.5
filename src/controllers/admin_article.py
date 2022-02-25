#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__, template_folder='templates')


@admin_article.route('/admin/meuble/show')
def show_meuble():
    mycursor = get_db().cursor()
    sql = '''select id_meuble,nom,prix,dateFabrication,C.libelle_couleur,M.libelle_materiaux,id_MeubleType,
        id_MeubleCouleur,id_MeubleMateriaux,T.libelle_type,nbStock,image
        from meubles
        inner join couleur C on C.id_couleur = id_MeubleCouleur
        inner join materiaux M on M.id_materiaux = id_MeubleMateriaux
        inner join types_meubles T on T.id_type = id_MeubleType
        order by nom;'''
    mycursor.execute(sql)
    meubles = mycursor.fetchall()
    sql = '''select t.id_type, m.id_MeubleType, count(m.nom) as stockDispo
        from meubles m
        inner join types_meubles t on t.id_type=m.id_MeubleType
        group by m.id_MeubleType, t.id_type;'''
    mycursor.execute(sql)
    stock_dispo = mycursor.fetchall()
    return render_template('admin/article/show_article.html', meubles=meubles, stockDispo=stock_dispo)


@admin_article.route('/meuble/add', methods=['GET'])
def add_meuble():
    mycursor = get_db().cursor()
    sql = "select * from couleur order by libelle_couleur;"
    mycursor.execute(sql)
    couleur = mycursor.fetchall()
    sql = "select * from materiaux order by libelle_materiaux;"
    mycursor.execute(sql)
    materiaux = mycursor.fetchall()
    sql = "select * from types_meubles order by libelle_type;"
    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    return render_template('admin/article/add_article.html', couleur=couleur, materiaux=materiaux,
                           typeMeuble=type_meuble)


@admin_article.route('/meuble/add', methods=['POST'])
def valid_add_meuble():
    mycursor = get_db().cursor()
    nom = request.form.get('nom_meuble')
    prix = request.form.get('prix_meuble')
    date_fabrication = request.form.get('dateFabrication')
    couleur = request.form.get('couleur')
    materiaux = request.form.get('materiaux')
    stock = request.form.get('stock')
    type_meuble_id = request.form.get('typeMeuble_id')
    image = request.form.get('image')
    # __________________________________________________________________________________________________________________
    tuple_insert = (nom, prix, date_fabrication, couleur, materiaux, stock, type_meuble_id, image)
    sql = '''insert into meubles(nom,prix,dateFabrication,id_MeubleCouleur,id_MeubleMateriaux,nbStock,id_MeubleType,
             image)
             values(%s,%s,%s,%s,%s,%s,%s,%s);'''
    print(sql)
    print(tuple_insert)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    # __________________________________________________________________________________________________________________
    print('meuble ajouté , nom: ', nom, ' - prix', prix, ' - dateFabrication', date_fabrication, ' - couleur', couleur,
          ' - type_meuble:', type_meuble_id, ' - materiaux', materiaux, ' - image:', image)
    message = 'meuble ajouté , nom:' + nom + ' - prix: ' + prix + ' - dateFabrication: ' + date_fabrication + \
              ' - couleur: ' + couleur + ' - type_meuble: ' + type_meuble_id + ' - materiaux: ' + materiaux + \
              ' - stock: ' + stock + ' - image: ' + image
    flash(message)
    return redirect(url_for('admin_article.show_meuble'))


@admin_article.route('/meuble/delete', methods=['GET'])
def delete_meuble():
    mycursor = get_db().cursor()
    id = request.args.get('id')
    sql = '''select * from ligne_de_commande
            where id_LigneMeuble = %s'''
    mycursor.execute(sql, id)
    cmd = mycursor.fetchall()
    sql = '''select * from panier
                where id_PanierMeuble = %s'''
    mycursor.execute(sql, id)
    panier = mycursor.fetchall()
    if cmd == () and panier == ():
        sql = "delete from meubles where id_meuble=(%s);"
        mycursor.execute(sql, id)
        get_db().commit()
        print("un meuble supprimé, id :", id)
        flash('un meuble supprimé, id : ' + id)
    else:
        flash("Le meuble n'as pas pu être suprimer car il intéresse ou à été commandé par un client")
    return redirect(url_for('admin_article.show_meuble'))


@admin_article.route('/meuble/edit/<int:id>', methods=['GET'])
def edit_meuble(id):
    mycursor = get_db().cursor()
    sql = '''select id_meuble,nom,prix,dateFabrication,C.libelle_couleur,M.libelle_materiaux,id_MeubleType,
            T.libelle_type,nbStock,image
            from meubles
            inner join couleur C on C.id_couleur = id_MeubleCouleur
            inner join materiaux M on M.id_materiaux = id_MeubleMateriaux
            inner join types_meubles T on T.id_type = id_MeubleType
            where id_meuble=%s
            order by C.libelle_couleur;'''
    mycursor.execute(sql, id)
    meuble = mycursor.fetchall()
    print(meuble)
    sql = "select * from couleur order by libelle_couleur;"
    mycursor.execute(sql)
    couleur = mycursor.fetchall()
    sql = "select * from materiaux order by libelle_materiaux;"
    mycursor.execute(sql)
    materiaux = mycursor.fetchall()
    sql = "select * from types_meubles order by libelle_type;"
    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', meuble=meuble, couleur=couleur, materiaux=materiaux,
                           type_meuble=type_meuble)


@admin_article.route('/meuble/edit', methods=['POST'])
def valid_edit_meuble():
    mycursor = get_db().cursor()
    id = request.form.get('id')
    nom = request.form.get('nom')
    prix = request.form.get('prix')
    date_fabrication = request.form.get('dateFabrication')
    couleur = request.form.get('couleur')
    stock = request.form.get('stock')
    type_meuble_id = request.form.get('typeMeuble_id')
    materiaux = request.form.get('materiaux')
    image = request.form.get('image')
    tuple_edit = (nom, prix, date_fabrication, couleur, stock, type_meuble_id, materiaux, image, id)
    sql = '''update meubles set nom=%s,prix=%s,dateFabrication=%s,id_MeubleCouleur=%s,nbStock=%s,id_MeubleType=%s,
            id_MeubleMateriaux=%s,image=%s
            where id_meuble=%s;'''
    mycursor.execute(sql, tuple_edit)
    get_db().commit()
    print('meuble modifié , nom: ', nom, ' - prix', prix, ' - dateFabrication', date_fabrication, ' - couleur', couleur,
          ' - type_meuble:', type_meuble_id, ' - materiaux', materiaux, ' - image:', image)
    flash('meuble modifié , nom: ' + nom + ' - prix: ' + prix + ' - dateFabrication: ' + date_fabrication +
          ' - couleur: ' + couleur + ' - type_meuble: ' + type_meuble_id + ' - materiaux: ' + materiaux + ' - image: ' +
          image)
    return redirect(url_for('admin_article.show_meuble'))
