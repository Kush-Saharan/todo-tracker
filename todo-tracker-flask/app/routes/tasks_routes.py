from flask import Blueprint,render_template,request,redirect
from app.models.tasks import Tasks,db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def home():
    tasks=Tasks.query.all()
    return render_template("index.html",tasks=tasks)


@tasks_bp.route('/task/add',methods=['POST'])
def add_task():

    task_add=request.form['task']
    existing_task = Tasks.query.filter(Tasks.task_name.ilike(task_add)).first()
    if(existing_task):
        message="This task already exists in tasks!"
    else:
        new_task=Tasks(task_name=task_add)
        db.session.add(new_task)
        db.session.commit()
        message="Task added successfully!"

    tasks=Tasks.query.all()
    return render_template('index.html',tasks=tasks, message=message)
    

@tasks_bp.route('/task/update')
def update_task():
    pass

