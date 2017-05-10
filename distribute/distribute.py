import os
import sqlite3
import json
from server_comm import myCliSocket
from flask import Flask, request, session, g, redirect, url_for, abort

"""
The present code recognize the name of person as primary key, but in reality different persons can share the same name, so using ID should be better.
"""

app = Flask(__name__)

app.config.update(dict(
    DATABASE='/tmp/distribute.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

manager_ip = "59.78.25.163"
manager_port = 5050

app.config.from_envvar('DISTRIBUTE_SETTINGS', silent=True)

# connect to the database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# initalize the database
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# command for initalizing the database
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Successfully initialized database")

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# judgement function for resource
def get_resource():
    return False
'''
# update information to the manage server
def update_to_manager(operation, name, address=None, skills=None):
    if operation == "ADD":
        data = {"type":"ADD", "inform":{"name":name, "address":address, "skills":skills}} # raw data of tuple type
        data_string = json.dumps(data) # data of string type
        myClient = myCliSocket(manager_ip, manager_port)
        socket = myClient.createCliSocket()
        myClient.startCliSocket(socket, 1024, data_string)
        myClient.destroyCliSocket()
        return True
    if operation == "DEL":
        data = {"type":"DEL", "inform":{"name":name}} # notice: del request struct is different from others
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
'''

def request_to_manager(problem):
    data = {"type":"REQUEST", "inform":{"problem":problem}}
    data_string = json.dumps(data)
    myClient = myCliSocket(manager_ip, manager_port)
    socket = myClient.createCliSocket()
    myClient.startCliSocket(socket, 1024, data_string)
    myClient.destroyCliSocket()

# judge if solved locally
def solved_local(result):
    return False

# close the database
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# api for adding user
@app.route('/add_user', methods=['POST'])
def add_user():
    db = get_db()
    db.execute('insert into persons (name, address, skills) values (?, ?, ?)',
            [request.form['name'], request.form['address'], request.form['skills']])
    db.commit()
    print("A user was added to local\n")
#    if update_to_manager("ADD", request.form['name'], request.form['address'], request.form['skills']):
#        print("A user was added to manager\n")

    return "200|A user was added"

# api for deleting user
@app.route('/del_user', methods=['POST'])
def del_user():
    db = get_db()
    db.execute('delete from persons where name=?', (request.form['name'],))
    db.commit()
    print("A user was deleted local\n")
#    if update_to_manager("DEL", request.form['name']):
#        print("A user was deleted to manager\n")
    return "200|A user was deleted"

# api for clearing information
@app.route('/clear')
def clear():
    init_db()
    print("User information cleared\n")

# api for distributing problem
@app.route('/distribute/<string:problem>')
def distribute(problem):
    db = get_db()
    res = db.execute('select name, address from persons where skills=?', problem)
    listres = res.fetchall()

    if listres != None:
        for item in listres:
            print("the problem %s is distributed to %s, address is %s\n" % (problem, item[0], item[1]))
            return "problem " + item[0] + " " + item[1]
    else:
        return "No one can solve the problem"
