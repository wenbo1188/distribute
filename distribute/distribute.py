import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort

app = Flask(__name__)

app.config.update(dict(
    DATABASE='/tmp/distribute.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('DISTRIBUTE_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Successfully initialized database")

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    db = get_db()
    db.execute('insert into persons (name, address, skills) values (?, ?, ?)',
            [request.form['name'], request.form['address'], request.form['skills']])
    db.commit()
    print("A user was added\n")
    return "A user was added\n"

@app.route('/del_user', methods=['POST'])
def del_user():
    db = get_db()
    db.execute('delete from persons where name=?', (request.form['name'],))
    db.commit()
    print("A user was deleted\n")
    return "A user was deleted\n"

@app.route('/distribute/<string:problem>')
def distribute(problem):
    db = get_db()
    res = db.execute('select name, address from persons where skills=?', problem)
    listres = res.fetchall()
    
    flag = 0 
    for item in listres:
        if item != None:
            print("the problem %s is distributed to %s, address is %s\n" % (problem, item[0], item[1])) 
            flag = 1
        else:
            break
    
    if flag == 0:
        return ("Nobody is good at the problem\n")
    else:
        return "Problem %s was distributed!\n" %problem



