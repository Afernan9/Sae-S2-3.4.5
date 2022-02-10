from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="localhost",
            #host="serveurmysql",
            user="ggodailf",
            password="2711",
            database="BDD_ggodailf",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db
