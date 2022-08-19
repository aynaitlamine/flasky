import os
import shutil
from flask_migrate import Migrate # nopep8
from app import create_app, db # nopep8
from app.models import User, Role, Permission # nopep8

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def clear():
    shutil.rmtree("migrations", ignore_errors=True)
