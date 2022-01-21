#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from connexion_db import get_db

auth_security = Blueprint('auth_security', __name__,
                        template_folder='templates')


@auth_security.route('/login')
def auth_login():
    return render_template('auth/login.html')


@auth_security.route('/login', methods=['POST'])
def auth_login_post():
    mycursor = get_db().cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    tuple_select = (username)
    sql = '''requete1'''
    retour = mycursor.execute(sql, (username))
    user = mycursor.fetchone()
    if user:
        mdp_ok = check_password_hash(user['password'], password)
        if not mdp_ok:
            flash(u'Vérifier votre mot de passe et essayer encore.')
            return redirect('/login')
        else:
            session['username'] = user['username']
            session['role'] = user['role']
            session['user_id'] = user['id']
            print(user['username'], user['role'])
            if user['role'] == 'ROLE_admin':
                return redirect('/admin/commande/index')
            else:
                return redirect('/client/article/show')
    else:
        flash(u'Vérifier votre login et essayer encore.')
        return redirect('/login')

@auth_security.route('/signup')
def auth_signup():
    return render_template('auth/signup.html')


@auth_security.route('/signup', methods=['POST'])
def auth_signup_post():
    mycursor = get_db().cursor()
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    tuple_select = (username, email)
    sql = '''requete2'''
    retour = mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        flash(u'votre adresse <strong>Email</strong> ou  votre <strong>Username</strong> (login) existe déjà')
        return redirect('/signup')

    # ajouter un nouveau user
    password = generate_password_hash(password, method='sha256')
    tuple_insert = (username, email, password, 'ROLE_client')
    sql = '''requete3'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()                    # position de cette ligne discutatble !
    sql='''requete4'''
    mycursor.execute(sql)
    info_last_id = mycursor.fetchone()
    user_id = info_last_id['last_insert_id']
    print('last_insert_id', user_id)
    get_db().commit()
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)
    session['username'] = username
    session['role'] = 'ROLE_client'
    session['user_id'] = user_id
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@auth_security.route('/logout')
def auth_logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)
    return redirect('/')
    #return redirect(url_for('main_index'))

@auth_security.route('/forget-password', methods=['GET'])
def forget_password():
    return render_template('auth/forget_password.html')

