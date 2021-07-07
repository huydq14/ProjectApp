from operator import index
from flask import *
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms.validators import Email
from forms import AddProjectForm, SignInForm, SignUpForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HuyDQ Python-Flask Web App'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

@app.route('/')
def main():
	todolist = [
		{
			'name': 'Buy milk',
			'description': 'Buy 2 liter of milk in Coopmart.'
		},
		{
			'name': 'Get money',
			'description': 'Get 500k from ATM'
		}
	]
	return render_template('index.html',todolist = todolist)
	

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	form = SignUpForm()

	if 	form.validate_on_submit():
		print("Validate on submit")
		_fname = form.inputFirstName.data
		_lname = form.inputLastName.data
		_email = form.inputEmail.data
		_password = form.inputPassword.data

		if(db.session.query(models.User).filter_by(email=_email).count() == 0):
			user = models.User(first_name = _fname, last_name = _lname, email = _email)
			user.set_password(_password)
			db.session.add(user)
			db.session.commit()
			return render_template('signUpSuccess.html', user = user)
		else:
			flash('Email {} is already exsits!'.format(_email))
			return render_template('signup.html', form = form)
		
	print("Not validate on submit")
	return render_template('signup.html', form = form)

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
	form = SignInForm()

	if form.validate_on_submit():
		_email = form.inputEmail.data
		_password = form.inputPassword.data		

		user = db.session.query(models.User).filter_by(email=_email).first()
		if (user is None):
			flash('Wrong email address or password')
		else:
			if (user.check_password(_password)):
				session['user'] = user.user_id
				
				return redirect('/userHome')
			else:
				flash('Wrong email address or password!')

	return render_template('signin.html', form = form)

@app.route('/userHome', methods=['Get', 'Post'])
def userHome():
	_user_id = session.get('user')
	if _user_id:
		user = db.session.query(models.User).filter_by(user_id=_user_id).first()
		return render_template('userhome.html', user = user)
	else:
		return redirect('/')			



@app.route('/logOut')
def logOut():
    	return redirect('/signIn')


@app.route('/newProject', methods=['GET', 'POST'])
def newProject():
	
	_user_id = session.get('user')
	if _user_id:
		user = db.session.query(models.User).filter_by(user_id=_user_id).first()
	
	form = AddProjectForm()
	

	if form.validate_on_submit():
		
		_description = form.inputDescription.data
		_name = form.inputName.data
		_deadline = form.inputDeadline.data
		project_id = request.form.get("hiddenProjectID", False)
		print(project_id)
		
		if (project_id == "0"):
			project = models.Project(desc=_description, name=_name, statusid="1", deadline = _deadline, user=user)
			db.session.add(project)
			db.session.commit()
		else:
			project = db.session.query(models.Project).filter_by(projectid=project_id).first()
			project.desc = _description
			project.name = _name
			project.deadline = _deadline
		
		return render_template('userhome.html', user = user)
	
	return render_template('addproject.html', form = form)

@app.route('/doneProject', methods=['GET', 'POST'])
def doneProject():

	_user_id = session.get('user')
	if _user_id:
		user = db.session.query(models.User).filter_by(user_id=_user_id).first()
		project_id = request.form.get("hiddenProjectID", False)
	print(user)
	print(project_id)

	
	print(project_id)
	if project_id:
		project = db.session.query(models.Project).filter_by(projectid=project_id).first()
		project.statusid = "3"
		db.session.commit()

	
	return render_template('userhome.html', user = user)

@app.route('/editProject', methods=['Get', 'Post'])
def editProject():
	
	_user_id = session.get('user')
	form = AddProjectForm()

	if _user_id:
		user = db.session.query(models.User).filter_by(user_id=_user_id).first()
		project_id = request.form.get("hiddenProjectID", False)
	print(user)

	
	print(project_id)
	if project_id:
		project = db.session.query(models.Project).filter_by(projectid=project_id).first()
		form.inputName.default = project.name
		form.inputDescription.default = project.desc		
		form.inputDeadline.default = project.deadline
		form.process()
		
		
		return render_template('addproject.html',form = form, user = user, project = project)
	
	return redirect('/')
	
@app.route('/deleteProject', methods=['GET', 'POST'])
def deleteProject():

	_user_id = session.get('user')
	if _user_id:
		user = db.session.query(models.User).filter_by(user_id=_user_id).first()
		project_id = request.form.get("hiddenProjectID", False)
	print(user)

	if project_id:
		project = db.session.query(models.Project).filter_by(projectid=project_id).first()
		db.session.delete(project)
		db.session.commit()
		
	return render_template('userhome.html', user = user)

#doimain&port
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)



