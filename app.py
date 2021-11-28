from myapp import app, db
from myapp.models import User, Project, Item
from flask_bootstrap import Bootstrap


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run(debug=True) # Here
    Bootstrap(app)


# To turn on the debug mode write debug=True in the brackets above
