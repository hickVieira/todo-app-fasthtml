from fasthtml.common import *


def render(todo):
    id = f'todo-{todo.id}'
    toggle = Input(
        type='checkbox',
        checked=todo.done,
        hx_get=f'/toggle/{todo.id}',
        hx_target=f'#{id}',
    )
    delete = A(
        'X',
        hx_delete=f'/{todo.id}',
        hx_target=f'#{id}',
        hx_swap='outerHTML',
    )
    return P(toggle, delete, todo.title, id=id)


app, rt, todos, Todo = fast_app(
    live=True,
    db_file='data/todos.db',
    render=render,
    id=int,
    title=str,
    done=bool,
    pk='id',
)


@rt('/')
def get():
    form = Form(
        Group(
            comp_todo_input_form(),
            Button(
                'Add',
                hx_post='/',
                hx_target='#todo-list',
                hx_swap='beforeend',
            ),
        ),
    )
    return Titled(
        'FastHTML Exploration Project',
        Card(Div(*todos(), id='todo-list'), header=form),
    )


def comp_todo_input_form():
    return Input(
        type='text',
        placeholder='Add a new todo',
        id='title',
        hx_swap_oob='true'
    )


@rt('/toggle/{id}')
def get(id: int):
    todo = todos[id]
    todo.done = not todo.done
    return todos.update(todo)


@rt('/{title}')
def create(todo: Todo):
    if not todo.title:
        return
    return todos.insert(todo), comp_todo_input_form()


@rt('/{id}')
def delete(id: int):
    todos.delete(id)


serve()
