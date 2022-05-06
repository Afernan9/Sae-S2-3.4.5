#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, flash, url_for
from flask import request, render_template, redirect

from connexion_db import get_db

admin_adresse = Blueprint('admin_adresse', __name__, template_folder='templates')

@admin_adresse.route('/admin/adress/show')
def show_adress():
    mycursor = get_db().cursor()

    sql = '''SELECT * FROM pointrelais;'''
    mycursor.execute(sql)
    adresse = mycursor.fetchall()

    return render_template('admin/adresse/show_adress.html', adresse=adresse)

@admin_adresse.route('/admin/adress/add', methods=['GET'])
def add_adress():
    return render_template('admin/adresse/add_adress.html')


@admin_adresse.route('/admin/adress/add', methods=['POST'])
def valid_add_meuble():
    mycursor = get_db().cursor()
    ville = request.form.get('ville')
    adress = request.form.get('adress')
    # __________________________________________________________________________________________________________________
    tuple_insert = (ville, adress)
    sql = '''insert into pointrelais (ville, adresse)
             values(%s,%s);'''
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    # __________________________________________________________________________________________________________________
    print('meuble ajouté , adresse: ', adress, ' - ville', ville)
    message = 'meuble ajouté , ville:' + ville + ' - adresse: ' + adress
    flash(message)
    return redirect(url_for('admin_adresse.show_adress'))
