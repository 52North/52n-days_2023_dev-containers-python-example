from flask import Flask
import psycopg2
import os
from datetime import date

app = Flask(__name__)

APP_TITLE="52N Days 2023 - breakout session - devcontainer"

APP_HEADER=f"""
        <html>
            <head>
                <title>{APP_TITLE}</title>
            </head>
            <body>
                <h1>{APP_TITLE}</h1>"""

APP_FOOTER=f"""
            <hr />
            ©2023 - {date.today().strftime("%Y")} 52°North Spatial Information Research GmbH
            </body>
       </html>"""

@app.route('/echo/<message>')
def echo(message):
    return f"{APP_HEADER}\nYour message was: <tt>{str(message)}</tt>\n{APP_FOOTER}"

@app.route('/store/<message>')
def store(message):
    table_name = 'message'
    message_column = 'message'
    #connect to database
    conn = psycopg2.connect(database="messages", user="postgres",
                        password="postgres", host="localhost", port="5432")

    #create cursor
    cur = conn.cursor()
    #insert message and commit
    cur.execute('INSERT INTO ' + table_name + ' (message) VALUES(%s)', (message,))
    conn.commit()

    output = 'stored messages:' + '<ol>\n'
    #select all stored messages
    cur.execute('SELECT ' + message_column + ' FROM ' + table_name)
    messages = cur.fetchall()
    for row in messages:
        output = output + '<li>' + row[0] + '</li>\n'

    #close resources
    cur.close()
    conn.close()

    return f"{APP_HEADER}{output}</ol>{APP_FOOTER}"