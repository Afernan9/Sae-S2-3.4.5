#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    sql = '''select C.id_cmd, C.date_achat, C.id_CmdEtat, E.libelle_etat, C.id_CmdUser, U.username
                from commande C
                inner join etat E on E.id_etat = C.id_CmdEtat
                inner join user U on U.id_User = C.id_CmdUser
                ;'''
    mycursor.execute(sql)
    commande = mycursor.fetchall()

# ====================================================================================================================== à revoir
    # sql='''select M.nom, L.quantite, M.prix, (M.prix*L.quantite) as prix_tot
    #             from meubles M
    #             inner join ligne_de_commande L on L.id_LigneMeuble=M.id_meuble;'''
    article_commande = mycursor.fetchall()
    return render_template('admin/commandes/show.html', commande=commande, article_commande=article_commande)


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    id = request.args.get('id_cmd')
    print("id =",id)
    sql = '''update commande set id_CmdEtat=2 where id_cmd=(%s);'''
    mycursor.execute(sql, (id))
    get_db().commit()
    return redirect('/admin/commande/show')
