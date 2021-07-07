from sqlalchemy.orm import defaultload, relationship
from sqlalchemy.sql.schema import ForeignKey
from main import db
from sqlalchemy import Sequence
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    project = relationship('Project', back_populates='user')

    def __repr__(self):
        return '<User full name: {} {}, email: {}>'.format(self.first_name, self.last_name, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    projectid = db.Column(db.Integer, Sequence('projectid_seq'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    statusid = db.Column(db.Integer, ForeignKey('status.statusid'), nullable=False)

    user = relationship('User', back_populates = 'project')
    task = relationship('Task', back_populates = 'projectp')
    projects = relationship('Status', back_populates = 'statusp')

    def __repr__(self):
        return '<Project: {} of user {}>'.format(self.projectid, self.desc, self.user_id)
    
class Task(db.Model):
    taskid = db.Column(db.Integer, Sequence('taskid_seq'), primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    projectid = db.Column(db.Integer, ForeignKey('project.projectid'), nullable=False)
    priorityid = db.Column(db.Integer, ForeignKey('priority.priorityid'), nullable=False)
    statusid = db.Column(db.Integer, ForeignKey('status.statusid'), nullable=False)
    deadline = db.Column(db.String(255), nullable=False)

    projectp = relationship('Project', back_populates='task')
    taskp = relationship('Priority', back_populates='priority')
    tasks = relationship('Status', back_populates='statust')

    def __repr__(self):
        return '<Task: {} of project {}>'.format(self.taskid, self.description, self.projectid)
    
    def getPriorityClass(self):
        if (self.priority_id == 1):
            return "text-danger"
        elif (self.priority_id == 2):
            return "text-warning"
        elif (self.priority_id == 3):
            return "text-info"
        elif (self.priority_id == 4):
            return "text-success"
        else:
            return "text-primary"

class Priority(db.Model):
    priorityid = db.Column(db.Integer, Sequence('priorityid_seq'), primary_key=True)
    priority_description = db.Column(db.String(255), nullable=True)

    priority = relationship('Task', back_populates='taskp')

def __repr__(self):
        return '<Priority: {} of task {}>'.format(self.task_priority, self.priority_description)

class Status(db.Model):
    statusid= db.Column(db.Integer, Sequence('statusid_seq'), primary_key=True)
    desc = db.Column(db.String(255), nullable=True)

    statust = relationship('Task', back_populates='tasks')
    statusp = relationship('Project', back_populates='projects')
