#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__, template_folder='templates')


@admin_article.route('/admin/meuble/show')
def show_meuble():
    mycursor = get_db().cursor()

    sql = '''select id_meuble,nom,prix,dateFabrication,M.libelle_materiaux,id_MeubleType,
        id_MeubleMateriaux,T.libelle_type, image
        from meubles
        inner join materiaux M on M.id_materiaux = id_MeubleMateriaux
        inner join types_meubles T on T.id_type = id_MeubleType
        order by nom
        ;'''
    mycursor.execute(sql)
    meubles = mycursor.fetchall()

    sql = '''select id_ColoreMeuble, nbStock, libelle_couleur 
        from colore 
        inner join couleur  on id_couleur = id_ColoreCouleur;'''
    mycursor.execute(sql)
    couleur = mycursor.fetchall()
    return render_template('admin/article/show_article.html', meubles=meubles, couleur=couleur)


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
    tuple_insert = (nom, prix, date_fabrication, materiaux, type_meuble_id, image)
    sql = '''insert into meubles(nom,prix,dateFabrication,id_MeubleMateriaux,id_MeubleType,
             image)
             values(%s,%s,%s,%s,%s,%s);'''
    mycursor.execute(sql, tuple_insert)

    sql = "select last_insert_id() as last_insert_id from meubles;"
    mycursor.execute(sql)
    id_meuble = mycursor.fetchone()

    tuple_insert = (id_meuble['last_insert_id'], couleur, stock)
    sql = '''insert into colore(id_ColoreMeuble, id_ColoreCouleur, nbStock) values(%s,%s,%s);'''
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
        sql = "delete from colore where id_ColoreMeuble = %s;"
        mycursor.execute(sql, id)
        sql = "delete from meubles where id_meuble=(%s);"
        mycursor.execute(sql, id)
        get_db().commit()
        print("un meuble supprimé, id :", id)
        flash('un meuble supprimé, id : ' + id)

        sql = "select * from colore;"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print("result = ",result)
    else:
        flash("Le meuble n'as pas pu être suprimer car il intéresse ou à été commandé par un client")
    return redirect(url_for('admin_article.show_meuble'))


@admin_article.route('/meuble/edit/<int:id>', methods=['GET'])
def edit_meuble(id):
    mycursor = get_db().cursor()
    sql = '''select id_meuble,nom,prix,dateFabrication,M.libelle_materiaux,id_MeubleType,
            T.libelle_type,image
            from meubles
            inner join materiaux M on M.id_materiaux = id_MeubleMateriaux
            inner join types_meubles T on T.id_type = id_MeubleType
            where id_meuble=%s
            order by M.libelle_materiaux;'''
    mycursor.execute(sql, id)
    meuble = mycursor.fetchall()
    print("meuble = ",meuble)
    sql = "select * from materiaux order by libelle_materiaux;"
    mycursor.execute(sql)
    materiaux = mycursor.fetchall()
    sql = "select * from types_meubles order by libelle_type;"
    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', meuble=meuble, materiaux=materiaux,
                           type_meuble=type_meuble)


@admin_article.route('/meuble/edit', methods=['POST'])
def valid_edit_meuble():
    mycursor = get_db().cursor()
    id = request.form.get('id')
    nom = request.form.get('nom')
    prix = request.form.get('prix')
    date_fabrication = request.form.get('dateFabrication')
    type_meuble_id = request.form.get('typeMeuble_id')
    materiaux = request.form.get('materiaux')
    image = request.form.get('image')

    tuple_edit = (nom, prix, date_fabrication, type_meuble_id, materiaux, image, id)
    print("tuple_edit = ", tuple_edit)
    sql = '''update meubles set nom=%s,prix=%s,dateFabrication=%s,id_MeubleType=%s,
            id_MeubleMateriaux=%s,image=%s
            where id_meuble=%s;'''
    mycursor.execute(sql, tuple_edit)
    get_db().commit()

    flash('meuble modifié , nom: ' + nom + ' - prix: ' + prix + ' - dateFabrication: ' + date_fabrication +
          ' - type_meuble: ' + type_meuble_id + ' - materiaux: ' + materiaux + ' - image: ' +
          image)
    return redirect(url_for('admin_article.show_meuble'))

@admin_article.route('/meubles/stock', methods=['GET'])
def stock_meuble():
    mycursor = get_db().cursor()

    id_meuble = request.args.get('id')

    sql = '''select nom, id_meuble, prix, c.nbStock
            from meubles
            left join colore c on c.id_ColoreMeuble = id_meuble
            where id_meuble = %s
            group by id_meuble
            ;'''
    mycursor.execute(sql, id_meuble)
    meuble = mycursor.fetchall()

    sql = '''select * from couleur;'''
    mycursor.execute(sql)
    couleur = mycursor.fetchall()
    return render_template('admin/article/stock_article.html', meuble=meuble, couleur=couleur)

@admin_article.route('/meubles/stock', methods=['POST'])
def valid_stock_meuble():
    mycursor = get_db().cursor()

    couleur = request.form.get('couleur')
    id_meuble = request.form.get('id_meuble')
    stock = request.form.get('stock')
    tuple = (stock, couleur, id_meuble)

    sql = '''select * from colore where id_ColoreCouleur = %s and id_ColoreMeuble = %s;'''
    mycursor.execute(sql, (couleur, id_meuble))
    colore = mycursor.fetchall()

    if colore == ():
        sql = "insert into colore(nbStock, id_ColoreCouleur, id_ColoreMeuble) values(%s,%s,%s);"
        mycursor.execute(sql, tuple)
    else:
        sql = "update colore set nbStock=nbStock+%s where id_ColoreCouleur = %s and id_ColoreMeuble = %s;"
        mycursor.execute(sql, tuple)
    get_db().commit()
    return redirect(url_for('admin_article.show_meuble'))