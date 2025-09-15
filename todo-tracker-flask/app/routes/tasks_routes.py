from flask import Blueprint,render_template,request,redirect
from app.models.tasks import Tasks,db,Day,TaskStatus
from datetime import date,datetime, timedelta

tasks_bp = Blueprint('tasks', __name__)


def get_number_of_days():
    first_day=Day.query.order_by(Day.date.asc()).first()
    last_day=Day.query.order_by(Day.date.desc()).first()
    if first_day and last_day:
        return (last_day.date-first_day.date).days+1
    return 0

def get_task_status(tasks, start_date, number_of_days):
    task_status = {}
    for day_index in range(number_of_days):
        task_status[day_index]={}
        day_date=start_date+timedelta(days=day_index)
        for task in tasks:
            status=TaskStatus.query.filter_by(task_id=task.id, date=day_date).first()
            task_status[day_index][task.id] = status.completed if status else False
    return task_status

@tasks_bp.route('/')
def home():
    tasks = Tasks.query.all()
    today = date.today()
 
    existing=Day.query.filter_by(date=today).first()
    if not existing:
        date_today=Day(date=today)
        db.session.add(date_today)
        db.session.commit()

    task_status_today = TaskStatus.query.filter_by(date=today).all()
    completed_count = sum(1 for t in task_status_today if t.completed)
    total_count = len(tasks)

    progress_percent = int((completed_count / total_count) * 100) if total_count > 0 else 0

    number_of_days=get_number_of_days() 
    first_day = Day.query.order_by(Day.date.asc()).first()
    task_status = get_task_status(tasks, first_day.date, number_of_days)

    return render_template("index.html", tasks=tasks, number_of_days=number_of_days,task_status=task_status,progress_percent=progress_percent)


@tasks_bp.route('/task/add',methods=['POST'])
def add_task():

    tasks = Tasks.query.all()
    today = date.today()
    task_add=request.form['task']
    existing_task = Tasks.query.filter(Tasks.task_name.ilike(task_add)).first()
    if(existing_task):
        message="This task already exists in tasks!"
    else:
        new_task=Tasks(task_name=task_add)
        db.session.add(new_task)
        db.session.commit()
        message="Task added successfully!"
    number_of_days = get_number_of_days()

    task_status_today = TaskStatus.query.filter_by(date=today).all()
    completed_count = sum(1 for t in task_status_today if t.completed)
    total_count = len(tasks)

    progress_percent = int((completed_count / total_count) * 100) if total_count > 0 else 0

    tasks=Tasks.query.all()
    first_day=Day.query.order_by(Day.date.asc()).first()
    last_day=Day.query.order_by(Day.date.desc()).first()
    number_of_days=(last_day.date - first_day.date).days + 1

    task_status = get_task_status(tasks, first_day.date, number_of_days)
    return render_template('index.html',tasks=tasks, message=message,number_of_days=number_of_days,task_status=task_status,progress_percent=progress_percent)
    

@tasks_bp.route('/task/save', methods=['POST'])
def save_task():
    tasks = Tasks.query.all()
    today = date.today()
    selected = request.form.getlist("progress")
    
    today_date = date.today()

    all_statuses = TaskStatus.query.filter_by(date=today_date).all()
    for status in all_statuses:
        status.completed = False

    for item in selected:
        day_str, task_str = item.split("_")
        task_id = int(task_str.replace("task", ""))

        task_existing = TaskStatus.query.filter_by(task_id=task_id, date=today_date).first()
        if task_existing:
            task_existing.completed = True
        else:
            task_existing = TaskStatus(task_id=task_id, date=today_date, completed=True)
            db.session.add(task_existing)

    db.session.commit()
    task_status_today = TaskStatus.query.filter_by(date=today).all()
    completed_count = sum(1 for t in task_status_today if t.completed)
    total_count = len(tasks)

    progress_percent = int((completed_count / total_count) * 100) if total_count > 0 else 0

    tasks = Tasks.query.all()
    first_day = Day.query.order_by(Day.date.asc()).first()
    last_day = Day.query.order_by(Day.date.desc()).first()
    number_of_days = (last_day.date - first_day.date).days + 1
    task_status = get_task_status(tasks, first_day.date, number_of_days)

    return render_template("index.html", tasks=tasks, number_of_days=number_of_days, task_status=task_status,progress_percent=progress_percent)

@tasks_bp.route('/task/edit')
def task_edit():
    tasks = Tasks.query.all()
    return render_template("task_edit.html", tasks=tasks)


@tasks_bp.route('/task/update/<int:task_id>', methods=['POST', 'GET'])
def task_update(task_id):
    task = Tasks.query.filter_by(id=task_id).first_or_404()

    if request.method == 'GET':
        return render_template('task_update.html', task=task)

    task_name = request.form['task_name']
    existing_task = Tasks.query.filter(Tasks.task_name.ilike(task_name), Tasks.id != task_id).first()
    if existing_task:
        message = "Task with this name already exists!"
        return render_template('task_update.html', task=task, message=message)

    task.task_name = task_name
    db.session.commit()
    return redirect('/task/edit')


@tasks_bp.route('/task/delete/<int:task_id>')
def task_delete(task_id):
    task = Tasks.query.filter_by(id=task_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return redirect('/task/edit')
