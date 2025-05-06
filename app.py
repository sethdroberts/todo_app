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

from todos.utils import error_for_list_title, get_list_by_id
from werkzeug.exceptions import NotFound

# poetry run python app.py

app = Flask(__name__)
app.secret_key = 'secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))
    
@app.route('/lists')
def get_lists():
    return render_template('lists.html', lists=session['lists'])
    
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
    if not lst:
        raise NotFound(description="List not found")
    return render_template('list.html', lst=lst)
    
@app.route("/lists/<list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo = request.form["todo"].strip()
    lst = get_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound('List not found')
        
    if not 1 <= len(todo) <= 100:
        flash('Todo name must be between 1 and 100 characters', 'error')
        return render_template('list.html', lst=lst)
    
    lst['todos'].append({
        'title': todo,
        'completed': False,
        'id': str(uuid4()),
    })
    flash('The todo has been created', 'success')
    session.modified = True
    return redirect(url_for('get_list', list_id=list_id), )
    

if __name__ == "__main__":
    app.run(debug=True, port=8080)