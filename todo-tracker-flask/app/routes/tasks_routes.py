from flask import Blueprint,render_template,request,redirect
from app.models.tasks import Tasks,db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def home():
    # tasks=Tasks.query.all()
    return render_template("index.html")


@tasks_bp.route('/add_task')
def add_task():
    pass


@tasks_bp.route('/update_task')
def update_task():
    pass

