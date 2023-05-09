from flask import Flask
app = Flask(__name__)

@app.route('/echo/<message>')
def echo(message):
    return 'Your message was: ' + str(message)