from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'JohnDoe'}
    return render_template('index.html', title='Home', user=user)
	
"""
	The operation that converts a template into a complete HTML page is called rendering. 
	To render the template I had to import a function that comes with the Flask framework called render_template(). 
	This function takes a template filename and a variable list of template arguments and returns the same template, 
	but with all the placeholders in it replaced with actual values.

	The render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework. 
	Jinja2 substitutes {{ ... }} blocks with the corresponding values, given by the arguments provided in the 
	render_template() call.

"""


"""
 Not a good way of coding
 
	from app import app

	@app.route('/')
	@app.route('/index')
	def index():
		user = {'username': 'Miguel'}
		return '''
	<html>
		<head>
			<title>Home Page - Microblog</title>
		</head>
		<body>
			<h1>Hello, ''' + user['username'] + '''!</h1>
		</body>
	</html>'''


"""
