import os  # standard library module for working with environment variables and filesystem paths
import re  # regular expressions used for SQL processing
from flask import Flask, render_template, request, redirect, url_for  # Flask components for web handling
from flask_mysqldb import MySQL  # Flask MySQL extension for request-scoped DB connection
import MySQLdb  # direct MySQL DBAPI client for schema initialization

app = Flask(__name__)  # create the Flask app instance

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')  # DB host fallback
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')  # DB user fallback
_mysql_password = os.environ.get('MYSQL_PASSWORD', 'toor')  # read password from env or default
app.config['MYSQL_PASSWORD'] = _mysql_password if _mysql_password else None  # None if the password is blank
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'todo_db')  # database name fallback
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))  # DB port fallback
app.config['SQL_SCHEMA_FILE'] = os.path.join(app.root_path, 'todo.sql')  # path to the SQL schema file

mysql = MySQL(app)  # initialize MySQL extension with Flask


def load_sql_schema():
    """Load SQL statements from the schema file and return them as a list."""
    schema_path = app.config['SQL_SCHEMA_FILE']  # locate schema file path
    if not os.path.exists(schema_path):  # ensure file is present
        raise RuntimeError(f"Schema file not found: {schema_path}")

    with open(schema_path, 'r', encoding='utf-8') as schema_file:  # open schema file in text mode
        sql = schema_file.read()  # read entire schema contents into a string

    statements = []  # parsed SQL statements will be collected here
    statement = ''  # current statement under construction
    for line in sql.splitlines():  # iterate over each file line
        line = line.strip()  # trim whitespace
        if not line or line.startswith('--'):  # skip blank lines and full-line comments
            continue
        if '--' in line:  # strip inline comments from SQL lines
            line = line.split('--', 1)[0].strip()
        statement += ' ' + line  # append the cleaned line to the current statement
        if line.endswith(';'):  # statement terminator found
            statements.append(statement.strip()[:-1].strip())  # remove trailing semicolon
            statement = ''  # reset for the next SQL statement
    if statement.strip():  # if an unfinished statement remains, include it too
        statements.append(statement.strip())

    return statements  # return the list of SQL statements


def init_db():
    """Initialize the MySQL database using the schema file."""
    statements = load_sql_schema()  # get SQL statements from schema file
    connection_kwargs = {
        'host': app.config['MYSQL_HOST'],  # MySQL server host
        'user': app.config['MYSQL_USER'],  # MySQL user name
        'port': app.config['MYSQL_PORT'],  # MySQL port number
        'charset': 'utf8mb4',  # use UTF-8 character set
        'use_unicode': True,  # return unicode strings
    }
    if app.config['MYSQL_PASSWORD'] is not None:  # only supply password when set
        connection_kwargs['passwd'] = app.config['MYSQL_PASSWORD']

    try:
        conn = MySQLdb.connect(**connection_kwargs)  # connect to MySQL directly
    except MySQLdb.OperationalError as err:  # handle connection/auth failures
        raise RuntimeError(
            "Unable to connect to MySQL. Verify MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, "
            "and that your MySQL service is running."
        ) from err

    cur = conn.cursor()  # create a cursor to execute SQL statements
    for stmt in statements:  # execute every statement from the schema file
        cur.execute(stmt)
    conn.commit()  # commit schema changes
    cur.close()  # close the cursor
    conn.close()  # close the direct connection


@app.route('/')
def index():
    """Render the main todo list page."""
    cur = mysql.connection.cursor()  # open a database cursor for the current request
    cur.execute("SELECT * FROM todos ORDER BY id DESC")  # query all todos in reverse order
    todos = cur.fetchall()  # fetch all rows from the query result
    cur.close()  # close the cursor after use

    return render_template('index.html', todos=todos)  # render the template with the todo items


@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo item submitted from the form."""
    task = request.form.get('task')  # retrieve submitted task text

    if task:  # only insert a new row when the task is not empty
        cur = mysql.connection.cursor()  # open a MySQL cursor
        cur.execute(
            "INSERT INTO todos(task) VALUES(%s)",  # parameterized insert statement
            [task]
        )
        mysql.connection.commit()  # save the change to the database
        cur.close()  # close the cursor

    return redirect(url_for('index'))  # redirect back to the todo list page


@app.route('/delete/<int:id>')
def delete_todo(id):
    """Delete a todo item by its database ID."""
    cur = mysql.connection.cursor()  # open a MySQL cursor for the request

    cur.execute(
        "DELETE FROM todos WHERE id=%s",  # delete the row with the given ID
        [id]
    )

    mysql.connection.commit()  # commit the delete operation
    cur.close()  # close the cursor

    return redirect(url_for('index'))  # redirect back to the list page


if __name__ == '__main__':
    init_db()  # create or update the database schema before starting the app
    app.run(host='0.0.0.0', port=5000, debug=True)  # run the Flask development server