#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, flash, url_for
from flask import request, render_template, redirect

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__, template_folder='templates')


@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    id_cmd = request.args.get('id_cmd')
    print(id_cmd)

    sql = '''select C.id_cmd, C.date_achat, L.quantite, SUM(M.prix*L.quantite) as prix_tot, C.id_CmdEtat, E.libelle_etat,
            C.id_CmdUser, U.username, CONCAT(PR.adresse, ' - ', PR.ville) as adress
            from commande C
            inner join ligne_de_commande L on L.id_LigneCmd=C.id_cmd
            inner join meubles M on M.id_meuble = L.id_LigneMeuble
            inner join etat E on E.id_etat = C.id_CmdEtat
            inner join user U on U.id_User = C.id_CmdUser
            inner join pointRelais PR on PR.id_pointRelais = C.id_PointRelais
            group by C.id_cmd
            ;
            '''
    mycursor.execute(sql)
    commande = mycursor.fetchall()

    if id_cmd != None:
        sql = '''select M.nom, L.quantite, M.prix, (M.prix*L.quantite) as prix_tot
                from meubles M
                inner join ligne_de_commande L on L.id_LigneMeuble = M.id_meuble
                inner join commande C on C.id_cmd = L.id_LigneCmd
                where C.id_cmd = (%s)
                group by M.nom, L.quantite, M.prix
                ;
            '''
        mycursor.execute(sql, id_cmd)
        article_commande = mycursor.fetchall()
        print(article_commande)
        return render_template('admin/commandes/show.html', commande=commande, article_commande=article_commande)

    return render_template('admin/commandes/show.html', commande=commande)


@admin_commande.route('/admin/commande/valider', methods=['get', 'post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    id = request.args.get('id_cmd')
    print("id =", id)
    sql = '''update commande set id_CmdEtat=2 where id_cmd=(%s);'''
    mycursor.execute(sql, id)
    get_db().commit()
    return redirect('/admin/commande/show')
