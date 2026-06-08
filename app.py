import os
import re
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
_mysql_password = os.environ.get('MYSQL_PASSWORD', 'toor')
app.config['MYSQL_PASSWORD'] = _mysql_password if _mysql_password else None
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'todo_db')
app.config['SQL_SCHEMA_FILE'] = os.path.join(app.root_path, 'todo.sql')

mysql = MySQL(app)


def load_sql_schema():
    """Load SQL statements from the schema file and return them as a list."""
    schema_path = app.config['SQL_SCHEMA_FILE']
    if not os.path.exists(schema_path):
        raise RuntimeError(f"Schema file not found: {schema_path}")

    with open(schema_path, 'r', encoding='utf-8') as schema_file:
        sql = schema_file.read()

    statements = []
    statement = ''
    for line in sql.splitlines():
        line = line.strip()
        if not line or line.startswith('--'):
            continue
        if '--' in line:
            line = line.split('--', 1)[0].strip()
        statement += ' ' + line
        if line.endswith(';'):
            statements.append(statement.strip()[:-1].strip())
            statement = ''
    if statement.strip():
        statements.append(statement.strip())

    return statements


def init_db():
    """Initialize the MySQL database using the schema file."""
    statements = load_sql_schema()
    connection_kwargs = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'charset': 'utf8mb4',
        'use_unicode': True,
    }
    if app.config['MYSQL_PASSWORD'] is not None:
        connection_kwargs['passwd'] = app.config['MYSQL_PASSWORD']

    try:
        conn = MySQLdb.connect(**connection_kwargs)
    except MySQLdb.OperationalError as err:
        raise RuntimeError(
            "Unable to connect to MySQL. Verify MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, "
            "and that your MySQL service is running."
        ) from err

    cur = conn.cursor()
    for stmt in statements:
        cur.execute(stmt)
    conn.commit()
    cur.close()
    conn.close()


@app.route('/')
def index():
    """Render the main todo list page."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todos ORDER BY id DESC")
    todos = cur.fetchall()
    cur.close()

    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo item submitted from the form."""
    task = request.form.get('task')

    if task:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO todos(task) VALUES(%s)",
            [task]
        )
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_todo(id):
    """Delete a todo item by its database ID."""
    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM todos WHERE id=%s",
        [id]
    )

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
