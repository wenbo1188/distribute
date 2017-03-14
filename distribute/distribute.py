import os
import sqlite3
import json
from server_comm import myCliSocket
from flask import Flask, request, session, g, redirect, url_for, abort

app = Flask(__name__)

app.config.update(dict(
    DATABASE='/tmp/distribute.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

manager_ip = "192.168.1.1"
manager_port = 5050

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

def get_resource():
    return False

def update_to_manager(operation, name, address=None, skills=None):
    if operation == "ADD":
        data = {"type":"ADD", "inform":{"name":name, "address":address, "skills":skills}}
        data_string = json.dumps(data)
        myClient = myCliSocket(manager_ip, manager_port)
        socket = myClient.createCliSocket()
        myClient.startCliSocket(socket, 1024, data_string)
        myClient.destroyCliSocket()
        return True
    if operation == "DEL":
        data = {"type":"DEL", "inform":{"name":name}} 
        data_string = json.dumps(data)
        myClient = myCliSocket(manager_ip, manager_port)
        socket = myClient.createCliSocket()
        myClient.startCliSocket(socket, 1024, data_string)
        myClient.destroyCliSocket()
        return True
    if operation == "UPDATE":
        data = {"type":"UPDATE", "inform":{"name":name, "address":address, "skills":skills}} 
        data_string = json.dumps(data)
        myClient = myCliSocket(manager_ip, manager_port)
        socket = myClient.createCliSocket()
        myClient.startCliSocket(socket, 1024, data_string)
        myClient.destroyCliSocket()
        return True
    return False

def request_to_manager(problem):
    data = {"type":"REQUEST", "inform":{"problem":problem}}
    data_string = json.dumps(data)
    myClient = myCliSocket(manager_ip, manager_port)
    socket = myClient.createCliSocket()
    myClient.startCliSocket(socket, 1024, data_string)
    myClient.destroyCliSocket()

def solved_local(result):
    return False

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
    print("A user was added to local\n")
    if update_to_manager("ADD", request.form['name'], request.form['address'], request.form['skills']):
        print("A user was added to manager\n")

    return "200|A user was added"

@app.route('/del_user', methods=['POST'])
def del_user():
    db = get_db()
    db.execute('delete from persons where name=?', (request.form['name'],))
    db.commit()
    print("A user was deleted local\n")
    if update_to_manager("DEL", request.form['name']):
        print("A user was deleted to manager\n")
    return "200|A user was deleted"

@app.route('/clear')
def clear():
    init_db()
    print("User information cleared\n")

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
        request_to_manager(problem)
        return ("Requesting to manager server\n")
    else:
        return "Problem %s was distributed!\n" %problem



