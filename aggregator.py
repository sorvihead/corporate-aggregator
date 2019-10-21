import os

import click
from flask_migrate import Migrate

from app import create_app
from app import db
from app.models import User
from app.models import Role
from app.models import Permission
from app.models import Shop
from app.models import Department
from app.models import Request

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Role=Role,
        Permission=Permission,
        Shop=Shop,
        Department=Department,
        Request=Request
    )


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests"""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

