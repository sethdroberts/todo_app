from werkzeug.exceptions import NotFound

def error_for_list_title(title, lists):
    if any(lst['title'] == title for lst in lists):
            return 'The titles must be unique'
        
    elif not 1 <= len(title) <= 100:
        return 'The title must be between 1 and 100 characters'
    
    else:
        return None
        
def get_list_by_id(list_id, lists):
    for lst in lists:
        if lst['id'] == list_id:
            return lst
    raise NotFound('List not found')
    
def get_todo_by_id(todo_id, todo_list):
    for todo in todo_list:
        if todo['id'] == todo_id:
            return todo
    raise NotFound('Todo not found')
    
def mark_all_complete(todo_list):
    for todo in todo_list:
        todo['completed'] = True
        
def todos_remaining(lst):
    return sum(1 for todo in lst['todos'] if not todo['completed'])
    
def is_list_completed(lst):
    return len(lst['todos']) > 0 and todos_remaining(lst) == 0
    
def is_todo_completed(todo):
    return todo['completed']
    
def sort_items(lists, is_completed_func):
    sorted_list = sorted(lists, key=lambda lst: lst['title'].lower())
    
    incomplete_list = [lst for lst in sorted_list if not is_completed_func(lst)]
    complete_list = [lst for lst in sorted_list if is_completed_func(lst)]
    
    return incomplete_list + complete_list
    