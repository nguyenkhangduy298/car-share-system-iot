# import the Flask class from the flask module
from flask import Flask, render_template

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('homepage.html')  # return a string

@app.route('/login')
def welcome():
    return render_template('login.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)