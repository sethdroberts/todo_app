from uuid import uuid4

from flask import (
    flash,
    Flask, 
    redirect, 
    render_template, 
    request,
    session,
    url_for, 
)

from todos.utils import (
    error_for_list_title, 
    get_list_by_id, 
    get_todo_by_id, 
    mark_all_complete,
    todos_remaining,
    is_list_completed,
    is_todo_completed,
    sort_items,
)
# poetry run python app.py

app = Flask(__name__)
app.secret_key = 'secret1'

@app.context_processor
def list_utilities_processor():
    return dict(
        is_list_completed=is_list_completed
    )

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))
    
@app.route('/lists')
def get_lists():
    lists = sort_items(session['lists'], is_list_completed)
    return render_template('lists.html', lists=lists, todos_remaining=todos_remaining)
    
@app.route('/lists', methods=["POST"])
def create_list():
    title = request.form["list_title"].strip()
    
    error = error_for_list_title(title, session['lists'])
    
    if error:
        flash(error, 'error')
        return render_template('new_list.html', title=title)

    session['lists'].append({
                    'title' : title, 
                    'id' : str(uuid4()),
                    'todos': []
                    })
    flash('The list has been created', 'success')
    session.modified = True
    return redirect(url_for('get_lists'))
    
@app.route('/lists/new')
def add_todo_list():
    return render_template('new_list.html')
    
@app.route('/lists/<list_id>')
def get_list(list_id):
    lst = get_list_by_id(list_id, session['lists'])
    lst['todos'] = sort_items(lst['todos'], is_todo_completed)
    return render_template('list.html', lst=lst)
    
@app.route("/lists/<list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo = request.form["todo"].strip()
    lst = get_list_by_id(list_id, session['lists'])
    if not 1 <= len(todo) <= 100:
        flash('Todo name must be between 1 and 100 characters', 'error')
        return redirect(url_for('get_list', list_id=list_id), )
    
    lst['todos'].append({
        'title': todo,
        'completed': False,
        'id': str(uuid4()),
    })
    flash('The todo has been created', 'success')
    session.modified = True
    return redirect(url_for('get_list', list_id=list_id), )
    
    
@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=["POST"])
def update_todo(list_id, todo_id):
    lst = get_list_by_id(list_id, session['lists'])
    todo = get_todo_by_id(todo_id, lst['todos'])
    todo['completed'] = (request.form['completed'] == 'True')
    flash('The todo has been updated', 'success')
    session.modified = True
    return redirect(url_for('get_list', list_id = list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/delete', methods=['POST'])
def delete_todo(list_id, todo_id):
    lst = get_list_by_id(list_id, session['lists'])
    todo = get_todo_by_id(todo_id, lst['todos'])
    lst['todos'].remove(todo)
    flash('The todo has been deleted', 'success')
    session.modified = True
    return redirect(url_for('get_list', list_id = list_id))

@app.route('/lists/<list_id>/complete_all', methods=['POST'])
def complete_all(list_id):
    lst = get_list_by_id(list_id, session['lists'])
    mark_all_complete(lst['todos'])
    flash('All todos have been completed', 'success')
    session.modified = True
    return redirect(url_for('get_list', list_id = list_id))
    
@app.route('/lists/<list_id>/edit')
def edit_list(list_id):
    lst = get_list_by_id(list_id, session['lists'])
    return render_template('edit-list.html', lst=lst, list_name=lst['title'], list_id=list_id)
    
@app.route('/lists/<list_id>', methods=["POST"])
def new_list_name(list_id):
    list_name = request.form['list_title'].strip()
    lst = get_list_by_id(list_id, session['lists'])

    if not 1 <= len(list_name) <= 100:
        flash('Todo name must be between 1 and 100 characters', 'error')
        return render_template('edit-list.html', lst=lst, list_name=list_name, list_id=list_id)
    
    lst['title'] = list_name
    flash('The list name has been updated', 'success')
    session.modified = True
    return redirect(url_for('get_list', list_id=list_id))

@app.route('/lists/<list_id>/delete', methods=["POST"])
def delete_list(list_id):
    lst = get_list_by_id(list_id, session['lists'])
    session['lists'].remove(lst)
    flash('The list has been deleted', 'success')
    return redirect(url_for('get_lists'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)