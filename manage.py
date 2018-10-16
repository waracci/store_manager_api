# Test runner to be included here
import os
import unittest
import nose
import logging

from flask_script import Manager

from app import create_app

logging.basicConfig()
app = create_app(config_name=os.getenv('APP_SETTINGS'))

manager = Manager(app)

@Manager.command
def test_runner_unit():
    """Test Runner unittest. No coverage"""
    app_tests = unittest.TestLoader().discover('./app/tests/v1', pattern='test*.py')
    test_result = unittest.TextTestRunner(verbosity=2).run(app_tests)
    if test_result.wasSuccessful():
        return 0
    return 1

@Manager.command
def test_runner_nose():
    """Tests Runner Nose. No coverage"""
    nose.run()

if __name__=='__main__':
    manager.run()