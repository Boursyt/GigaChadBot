from ChatBot_Flask import app
import flask
from flask import render_template

@app.route('/')
def index():
    history = {'inputs': [], 'responses': []}
    return render_template('chat.html', history=history)


@app.route('/chat')
def chatPage():
    return render_template('chat.html')


        

if __name__ == '__main__':
    app.run(debug=True, port=5000)
