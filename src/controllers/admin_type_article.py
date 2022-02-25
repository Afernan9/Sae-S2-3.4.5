#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__, template_folder='templates')


@admin_type_article.route('/admin/type-article/show')
def show_type_meuble():
    mycursor = get_db().cursor()
    sql = '''select * from types_meubles;'''
    mycursor.execute(sql)
    types_meubles = mycursor.fetchall()
    print(types_meubles)
    sql = '''select t.id_type, count(m.id_MeubleType) as nbMeubles_Types
            from meubles m
            right join types_meubles t on m.id_MeubleType=t.id_type
            group by t.id_type;'''
    mycursor.execute(sql)
    compte = mycursor.fetchall()
    print('compte = ', compte)
    return render_template('admin/type_article/show_type_article.html', types_meubles=types_meubles, compte=compte)


@admin_type_article.route('/type-meuble/add', methods=['GET'])
def add_type_meuble():
    return render_template('admin/type_article/add_type_article.html')


@admin_type_article.route('/type-meuble/add', methods=['POST'])
def valid_add_type_meuble():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle)
    sql = "insert into types_meubles(libelle_type) values(%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print('type ajouté , libellé :', libelle)
    message = 'type meuble ajouté , libellé :' + libelle
    flash(message)
    return redirect('/admin/type-article/show')


@admin_type_article.route('/type-meuble/delete', methods=['GET'])
def delete_type_meuble():
    mycursor = get_db().cursor()
    id = request.args.get('id')
    print("id = ", id)
    sql = '''select * from meubles m
        where m.id_MeubleType=%s;'''
    mycursor.execute(sql, id)
    result = mycursor.fetchall()
    if result == ():
        mycursor = get_db().cursor()
        sql = "delete from types_meubles where id_type = (%s);"
        mycursor.execute(sql, id)
        get_db().commit()
        print("un type de meuble supprimé, id :", id)
        flash('un type de meuble supprimé, id : ' + id)
        return redirect(url_for('admin_type_article.show_type_meuble'))
    else:
        sql = '''select count(m.nom) as nbMeublesSup
            from meubles m
            where m.id_MeubleType=%s
            order by m.nom;'''
        mycursor.execute(sql, id)
        nb_tot = mycursor.fetchall()
        print("nbTot = ", nb_tot)
        sql = '''select m.nom, m.id_meuble, m.id_MeubleType, m.nbStock
            from meubles m
            inner join types_meubles t on t.id_type=m.id_MeubleType
            where t.id_type=%s
            order by m.nom;'''
        mycursor.execute(sql, id)
        meubles_associes = mycursor.fetchall()
        print("meublesAssocies = ", meubles_associes)
        return render_template('/admin/type_article/delete_type_article.html', nbTot=nb_tot,
                               meublesAssocies=meubles_associes)


@admin_type_article.route('/type-meuble/deleteMeuble', methods=['GET'])
def deleteMeuble_type_meuble():
    mycursor = get_db().cursor()
    id_meuble = request.args.get('id_meuble')
    id = request.args.get('id')
    print("id_meuble = ", id_meuble, " id = ", id)
    sql = '''select * from ligne_de_commande
                where id_LigneMeuble = %s'''
    mycursor.execute(sql, id_meuble)
    cmd = mycursor.fetchall()
    sql = '''select * from panier
                    where id_PanierMeuble = %s'''
    mycursor.execute(sql, id_meuble)
    panier = mycursor.fetchall()
    if cmd == () and panier == ():
        sql = "delete from meubles where id_meuble=(%s);"
        mycursor.execute(sql, id_meuble)
        get_db().commit()
        print("un meuble supprimé, id :", id_meuble)
        flash('un meuble supprimé, id : ' + id_meuble)
    else:
        flash("Le meuble n'as pas pu être suprimer car il intéresse ou à été commandé par un client")
    sql = '''select count(m.nom) as nbMeublesSup
        from meubles m
        inner join types_meubles t on t.id_type=m.id_MeubleType
        where t.id_type=%s
        order by m.nom;'''
    mycursor.execute(sql, id)
    nb_tot = mycursor.fetchall()
    sql = '''select m.nom, m.id_meuble, m.id_MeubleType, m.nbStock
        from meubles m
        inner join types_meubles t on t.id_type=m.id_MeubleType
        where t.id_type=%s
        order by m.nom;'''
    mycursor.execute(sql, id)
    meubles_associes = mycursor.fetchall()
    print("meublesAssocies = ", meubles_associes)
    if meubles_associes == ():
        mycursor = get_db().cursor()
        sql = "delete from types_meubles where id_type=%s;"
        mycursor.execute(sql, id)
        get_db().commit()
        print('un type de meuble suprimé')
        return redirect(url_for('admin_type_article.show_type_meuble'))
    else:
        return render_template('admin/type_article/delete_type_article.html', nbTot=nb_tot,
                               meublesAssocies=meubles_associes)


@admin_type_article.route('/type-meuble/edit/<int:id>', methods=['GET'])
def edit_type_meuble(id):
    mycursor = get_db().cursor()
    sql = "select * from types_meubles where id_type=(%s);"
    mycursor.execute(sql, id)
    type_meuble = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_meuble=type_meuble)


@admin_type_article.route('/type-meuble/edit', methods=['POST'])
def valid_edit_type_meuble():
    mycursor = get_db().cursor()
    id = request.form.get('id')
    libelle = request.form.get('libelle')
    tuple_update = (libelle, id)
    sql = "update types_meubles set libelle_type=%s where id_type = (%s);"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    print('type de meuble modifié, id : ', id, " libelle :", libelle)
    flash('type de meuble modifié, id : ' + id + " libelle : " + libelle)
    return redirect('/admin/type-article/show')
