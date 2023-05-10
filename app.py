from flask import Flask
import psycopg2
import os

app = Flask(__name__)



@app.route('/echo/<message>')
def echo(message):
    return 'Your message was: ' + str(message)

@app.route('/store/<message>')
def store(message):
    table_name = 'message'
    message_column = 'message'
    #connect to database
    conn = psycopg2.connect(database="postgres", user="postgres",
                        password="postgres", host="localhost", port="5432")

    #create cursor
    cur = conn.cursor()
    #insert message and commit
    cur.execute('INSERT INTO ' + table_name + ' (message) VALUES(%s)', (message,))
    conn.commit()

    output = 'stored messages:' + '<br />\n'
    #select all stored messages
    cur.execute('SELECT ' + message_column + ' FROM ' + table_name)
    messages = cur.fetchall()
    for row in messages:
        output = output + row[0] + '<br />\n'

    #close resources
    cur.close()
    conn.close()

    return output