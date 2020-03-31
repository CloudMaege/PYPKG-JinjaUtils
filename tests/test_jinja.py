# Run PyTest:
# `poetry run pytest tests -v`
# Run single test file instead of entire test suite:
# `poetry run pytest tests/test_jinja.py -v`
# Run single test from a single test file
# `poetry run pytest tests/test_jinja.py::{testname} -v`

# Run Coverage Report:
# poetry run coverage run -m --source=. pytest tests/test_jinja.py
# poetry run coverage html --omit=tests/* -i
################
# Imports:     #
################

# Pip Installed Imports:
from cloudmage.jinjautils import JinjaUtils

# Base Python Module Imports:
import pytest
import os
import shutil
# import sys


######################################
# Define Set and Teardown Fixtures:  #
######################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    """ JinjaUtils Class PyTest Environment Setup and Teardown Fixture

    Setup the test environment for the JinjaUtils class unit tests.
    This fixture will create a new test directory, create a test
    jinja template, and write the template to the test directory during
    the setup phase. It will then allow the test to yield or execute, and
    finally once the test has completed, it will tear down the setup
    by removing the test directory and its contents.
    """
    # Define the test directory
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Test Template
    pytest_template = """
    name = {{ name }}
    verbose = {{ debug }}
    {% for k,v in context.items() %}
    {{ k }} = {{ v }}
    {% endfor %}
    """

    # Create a fresh test directory
    if not os.path.exists(test_template_directory):
        os.mkdir(test_template_directory)

    # Write a testing template to the testing template directory
    pytest_jinja_template = open(
        os.path.join(
            test_template_directory, 'test_tpl.j2'
            ),
        "w"
    )
    pytest_jinja_template.write(pytest_template)
    pytest_jinja_template.close()

    # Setup, Yield the test, and when finished, tear down the test directory.
    yield
    if os.path.exists(test_template_directory):
        shutil.rmtree(test_template_directory)


######################################
# Test Init Defaults:                #
######################################
def test_init():
    """ JinjaUtils Class Constructor Init Test

    This test will instantiate a new JinjaUtils object and test to ensure
    that the object attributes match the expected instantiation values that
    should be set by the class init constructor.

    Expected Result:
      Constructor values should be set to their default settings.
    """

    # Instantiate a JinjaUtils object
    # Test object instance attributes are set to the expected default values.
    Jinja = JinjaUtils()
    assert(isinstance(Jinja, object))

    # Test Verbose Setting
    assert(not Jinja._verbose)
    assert(not Jinja.verbose)

    # Test Log Setting
    assert(Jinja._log is None)
    assert(Jinja._log_context == "CLS->JinjaUtils")

    # Test Trim Blocks Setting
    assert(Jinja._trim_blocks)
    assert(Jinja.trim_blocks)

    # Test LStrip Blocks Setting
    assert(Jinja._lstrip_blocks)
    assert(Jinja.lstrip_blocks)

    # Test Configured Template Directory
    assert(Jinja._template_directory is None)
    assert(Jinja.template_directory == "A template directory has not yet \
been configured.")

    # Test Available Templates Settings
    assert(isinstance(Jinja._available_templates, list))
    assert(not Jinja._available_templates)
    assert(len(Jinja._available_templates) == 0)
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)
    assert(len(Jinja.available_templates) == 0)

    # Test Load Method
    assert(Jinja._loaded_template is None)
    assert(Jinja.load == "No template has been loaded!")

    # Test Render Method
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)
    assert(Jinja._rendered_template is None)
    assert(Jinja.rendered == "No template has been rendered!")

    # Test Write Method
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)


######################################
# Test Verbose:                      #
######################################
def test_verbose_init_enabled():
    """ JinjaUtils Class Verbose Property Init Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to True
    during object instantiation, using the class constructor.

    Expected Result:
      Verbose property should be set to True.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test verbose is set to True
    assert(Jinja._verbose)
    assert(Jinja.verbose)


def test_verbose_setter_enabled():
    """ JinjaUtils Class Verbose Property Setter Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to True
    using the class verbose setter method.

    Expected Result:
      Verbose property should be set to True.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils()
    assert(isinstance(Jinja, object))

    # Test verbose is set to default False
    assert(not Jinja._verbose)
    assert(not Jinja.verbose)

    # Call the Setter to enable verbose and test the property value is True
    Jinja.verbose = True
    assert(Jinja._verbose)
    assert(Jinja.verbose)


def test_verbose_init_invalid():
    """ JinjaUtils Class Verbose Property Init Invalid Value Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    during object instantiation, using the class constructor.

    Expected Result:
      Verbose property should be set to False, ignoring the invalid value.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=42)
    assert(isinstance(Jinja, object))

    # Test verbose is False default value, ignoring invalid input value
    assert(not Jinja._verbose)
    assert(not Jinja.verbose)


def test_verbose_setter_invalid(capsys):
    """ JinjaUtils Class Verbose Property Setter Invalid Value Test

    This test will test the verbose getter and setter property methods.
    Default value tested during init test, test setting value to invalid value
    using the property setter method.

    Expected Result:
      Verbose property should be set to False, ignoring the invalid value.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils()
    assert(isinstance(Jinja, object))

    # Test verbose setting was defaulted to False
    assert(not Jinja._verbose)
    assert(not Jinja.verbose)

    # Set verbose to an invalid value using property settter and test the
    # value ensuring that the invalid value was ignored, and is set False.
    Jinja.verbose = 42
    assert(not Jinja._verbose)
    assert(not Jinja.verbose)

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.verbose: \
-> verbose argument expected bool but received" in err


######################################
# Test Logging:                      #
######################################
def test_logs_verbose_disabled(capsys):
    """ JinjaUtils Class Verbose Disabled Log Test

    This test will test to ensure that when verbose mode is disabled
    that no logs other then errors are output.

    Expected Result:
      Logged events are silent, Error messages are output to the console.
    """

    # Instantiate a JinjaUtils object
    # Test the returned object verbose attribute for expected values.
    Jinja = JinjaUtils(verbose=False)
    assert(isinstance(Jinja, object))

    # Test verbose setting
    assert(not Jinja._verbose)

    # Write a test log entry
    Jinja.log("Pytest debug log write test", 'debug', 'test_log')
    Jinja.log("Pytest info log write test", 'info', 'test_log')
    Jinja.log("Pytest warning log write test", 'warning', 'test_log')
    Jinja.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.test_log: \
-> Pytest debug log write test" not in out
    assert "INFO    CLS->JinjaUtils.test_log: \
-> Pytest info log write test" not in out
    assert "WARNING CLS->JinjaUtils.test_log: \
-> Pytest warning log write test" not in out
    assert "ERROR   CLS->JinjaUtils.test_log: \
-> Pytest error log write test" in err


def test_logs_verbose_enabled(capsys):
    """ JinjaUtils Class Verbose Enabled Log Test

    This test will test to ensure that when verbose mode is enabled
    that all logs are written to stdout, stderr

    Expected Result:
      Logged events are written to stdout, stderr. Verbose enabled.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test verbose setting was correctly set to input True value
    assert(Jinja._verbose)
    assert(Jinja.verbose)

    # Write a test log entry to each log level
    Jinja.log("Pytest debug log write test", 'debug', 'test_log')
    Jinja.log("Pytest info log write test", 'info', 'test_log')
    Jinja.log("Pytest warning log write test", 'warning', 'test_log')
    Jinja.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.test_log: \
-> Pytest debug log write test" in out
    assert "INFO    CLS->JinjaUtils.test_log: \
-> Pytest info log write test" in out
    assert "WARNING CLS->JinjaUtils.test_log: \
-> Pytest warning log write test" in out
    assert "ERROR   CLS->JinjaUtils.test_log: \
-> Pytest error log write test" in err


def test_logs_logger_object(capsys):
    """ JinjaUtils Class Log Object Test

    This test will test the log method to ensure that if the class constructor
    is passed a logger object object to write to that all class logs will be
    written to that provided object instead of stdout, stderr.

    Expected Result:
      Logged events are written to the provided log object. Verbose enabled.
    """

    # Create a test log object that will just collect logs and add them to a
    # list, which we can check for produced log messages
    class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.warning_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Info Messages"""
            self.info_logs.append(message)

        def warning(self, message):
            """Log Warning Messages"""
            self.warning_logs.append(message)

        def error(self, message):
            """Log Error Messages"""
            self.error_logs.append(message)

    # Instantiate a new log object to collect test logs.
    LogObj = Log()

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True, log=LogObj)
    assert(isinstance(Jinja, object))
    assert(isinstance(Jinja._log, object))
    assert(isinstance(Jinja.log, object))

    # Test verbose setting
    assert(Jinja._verbose)
    assert(Jinja.verbose)
    assert(Jinja._log is not None)

    # Test the Log object to make sure the expected object attributes exist
    assert(hasattr(Jinja._log, 'debug'))
    assert(hasattr(Jinja._log, 'info'))
    assert(hasattr(Jinja._log, 'warning'))
    assert(hasattr(Jinja._log, 'error'))
    assert(hasattr(Jinja._log, 'debug_logs'))
    assert(hasattr(Jinja._log, 'info_logs'))
    assert(hasattr(Jinja._log, 'warning_logs'))
    assert(hasattr(Jinja._log, 'error_logs'))

    # Write test log entries for each of the different types of logs
    Jinja.log("Pytest log debug test", 'debug', 'test_log_object')
    Jinja.log("Pytest log info test", 'info', 'test_log_object')
    Jinja.log("Pytest log warning test", 'warning', 'test_log_object')
    Jinja.log("Pytest log error test", 'error', 'test_log_object')

    # Test that the Log object debug_logs, info_logs, warning_logs and
    # error_logs properties are lists
    assert(isinstance(Jinja._log.debug_logs, list))
    assert(isinstance(Jinja._log.info_logs, list))
    assert(isinstance(Jinja._log.warning_logs, list))
    assert(isinstance(Jinja._log.error_logs, list))

    # Test that each of the log_lists have items written into them
    assert(len(LogObj.debug_logs) >= 1)
    assert(len(LogObj.info_logs) >= 1)
    assert(len(LogObj.warning_logs) >= 1)
    assert(len(LogObj.error_logs) >= 1)

    # Test the log messages to make sure they match the written logs
    assert(
        LogObj.debug_logs[-1] == "CLS->JinjaUtils.test_log_object: \
-> Pytest log debug test"
    )
    assert(
        LogObj.info_logs[-1] == "CLS->JinjaUtils.test_log_object: \
-> Pytest log info test"
    )
    assert(
        LogObj.warning_logs[-1] == "CLS->JinjaUtils.test_log_object: \
-> Pytest log warning test"
    )
    assert(
        LogObj.error_logs[-1] == "CLS->JinjaUtils.test_log_object: \
-> Pytest log error test"
    )


def test_logs_invalid_object(capsys):
    """ JinjaUtils Class Invalid Log Object Test

    This test will test the log method to ensure that
    if the logs constructor object is provided an invalid log object
    to write to that the invalid object will be ignored, resulting in
    all class logs being written to stdout, stderr.

    Expected Result:
      Invalid object ignored. Logged events are written to stdout, stderr.
    """

    # Test to ensure that passing a non valid log object is properly caught.
    Jinja = JinjaUtils(verbose=True, log=42)
    assert(isinstance(Jinja, object))
    assert(Jinja._log is None)

    # Write a test log entry to each log level
    Jinja.log("Pytest debug log write test", 'debug', 'test_log')
    Jinja.log("Pytest info log write test", 'info', 'test_log')
    Jinja.log("Pytest warning log write test", 'warning', 'test_log')
    Jinja.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.test_log: \
-> Pytest debug log write test" in out
    assert "INFO    CLS->JinjaUtils.test_log: \
-> Pytest info log write test" in out
    assert "WARNING CLS->JinjaUtils.test_log: \
-> Pytest warning log write test" in out
    assert "ERROR   CLS->JinjaUtils.test_log: \
-> Pytest error log write test" in err


######################################
# Test trim_blocks property methods: #
######################################
def test_trim_blocks_property_getter():
    """ JinjaUtils Class Trim Blocks Default Value Test

    This test will test the trim_blocks getter property method.
    Test to ensure property has default value of True set on instantiation.

    Expected Result:
      Object trim_blocks property will have default setting of True set.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test trim_blocks property value.
    assert(Jinja._trim_blocks)
    assert(Jinja.trim_blocks)


def test_trim_blocks_property_setter():
    """ JinjaUtils Class Trim Blocks Property Setter Test

    This test will test the trim_blocks setter property method.
    Test to ensure property has expected value of False when set using
    the properties setter method.

    Expected Result:
      Object trim_blocks property will have setter defined value of False.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test trim_blocks default setting
    assert(Jinja._trim_blocks)
    assert(Jinja.trim_blocks)

    # Call the Setter to update the property value to False and test values.
    Jinja.trim_blocks = False
    assert(not Jinja._trim_blocks)
    assert(not Jinja.trim_blocks)


def test_trim_blocks_property_invalid(capsys):
    """ JinjaUtils Class Trim Blocks Invalid Value Test

    This test will test the trim_blocks setter property method.
    Test to ensure property has default value of True when set using
    the properties setter method and a bad type or invalid value is passed
    or used in the setter method call.

    Expected Result:
      Object trim_blocks will ignore bad value, and set default value of True.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test trim_blocks default setting
    assert(Jinja._trim_blocks)
    assert(Jinja.trim_blocks)

    # Call the Setter and provide it with a non bool value
    Jinja.trim_blocks = 42

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.trim_blocks: \
-> trim_blocks property update requested." in out
    assert "INFO    CLS->JinjaUtils.trim_blocks: \
-> trim_blocks property requested." in out
    assert "ERROR   CLS->JinjaUtils.trim_blocks: \
-> trim_blocks argument expected bool but received type:" in err

    # Retest trim_blocks default setting
    assert(Jinja._trim_blocks)
    assert(Jinja.trim_blocks)


########################################
# Test lstrip_blocks property methods: #
########################################
def test_lstrip_blocks_property_getter():
    """ JinjaUtils Class LStrip Blocks Default Value Test

    This test will test the lstrip_blocks getter property method.
    Test to ensure property has default value of True set on instantiation.

    Expected Result:
      Object lstrip_blocks property will have default setting of True set.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test lstrip_blocks setting
    assert(Jinja._lstrip_blocks)
    assert(Jinja.lstrip_blocks)


def test_lstrip_blocks_property_setter():
    """ JinjaUtils Class LStrip Blocks Property Setter Test

    This test will test the lstrip_blocks setter property method.
    Test to ensure property has expected value of False when set using
    the properties setter method.

    Expected Result:
      Object lstrip_blocks property will have setter defined value of False.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test lstrip_blocks default value setting
    assert(Jinja._lstrip_blocks)
    assert(Jinja.lstrip_blocks)

    # Call the Setter to update the property value and test value.
    Jinja.lstrip_blocks = False
    assert(not Jinja._lstrip_blocks)
    assert(not Jinja.lstrip_blocks)


def test_lstrip_blocks_property_invalid(capsys):
    """ JinjaUtils Class LStrip Blocks Invalid Value Test

    This test will test the lstrip_blocks setter property method.
    Test to ensure property has default value of True when set using
    the properties setter method and a bad type or invalid value is passed
    or used in the setter method call.

    Expected Result:
      Object lstrip_blocks will ignore invalid value, and set default True.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test lstrip_blocks default setting
    assert(Jinja._lstrip_blocks)
    assert(Jinja.lstrip_blocks)

    # Call the Setter and provide it with a non bool value
    # to test the error condition
    Jinja.lstrip_blocks = 42

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.lstrip_blocks: \
-> lstrip_blocks property update requested." in out
    assert "INFO    CLS->JinjaUtils.lstrip_blocks: \
-> lstrip_blocks property requested." in out
    assert "ERROR   CLS->JinjaUtils.lstrip_blocks: \
-> lstrip_blocks argument expected bool but received type:" in err

    # Retest lstrip_blocks default setting
    assert(Jinja._lstrip_blocks)
    assert(Jinja.lstrip_blocks)


####################################
# Test Exception handler method:   #
####################################
def test_exception_handler(capsys):
    """ JinjaUtils Class Exception Handler Test

    This test will test the class wide exception handler.

    Expected Result:
      When an exception condition is encountered,
      exceptions will output in correct format to stderr.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils()
    assert(isinstance(Jinja, object))

    # Write a log with a bad value to trigger an exception.
    Jinja.log('Message', 42, 2)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.log: \
-> EXCEPTION occurred in: 'CLS->JinjaUtils.log'" in err


#############################################
# Test template_directory property methods: #
#############################################
def test_template_directory_property_getter_default():
    """ JinjaUtils Class Template Directory Property Getter Default Value Test

    This test will test template_directory property getter method
    to ensure that upon instantiation the proper default values are
    set to the expected None/Blank List values.

    Expected Result:
      Object template_directory returns a blank list, and that
      _template_directory is set to None.
    """

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test the template_directory, available_templates, jinja_loader,
    # and jinja_tpl_library instantiation values.
    assert(Jinja._template_directory is None)
    assert(isinstance(Jinja.template_directory, str))
    assert(Jinja.template_directory == "A template directory \
has not yet been configured.")
    assert(isinstance(Jinja._available_templates, list))
    assert(not Jinja._available_templates)
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)


def test_template_directory_property(capsys):
    """ JinjaUtils Class Template Directory Property Getter/Setter Test

    This test will test template_directory property getter and setter methods
    to ensure that when the template directory is properly set that the
    expected valid list value is returned. When provided a valid file path,
    the template_directory setter method also sets the available_templates,
    and jinja loader methods, so those values will be set as well.

    Expected Result:
      Object template_directory directory path is set to provided value,
      _template_directory is also set to the valid provided directory path
      available_templates is set to 1 as the test directory has a template
      written to it during test setup. Finally Jinja Loader value should
      also be set and have the existing template already loaded into the
      jinja loader template library.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test the template_directory instantiation default value.
    assert(Jinja._template_directory is None)
    assert(isinstance(Jinja.template_directory, str))
    assert(Jinja.template_directory == "A template directory has not yet \
been configured.")
    assert(isinstance(Jinja._available_templates, list))
    assert(not Jinja._available_templates)
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)

    # Set the template directory using the property setter method.
    Jinja.template_directory = test_template_directory

    # Test for expected return values configured using the property setter.
    assert(Jinja._template_directory == test_template_directory)
    assert(isinstance(Jinja.template_directory, str))
    assert(Jinja.template_directory == test_template_directory)
    assert(isinstance(Jinja._available_templates, list))
    assert(Jinja._available_templates)
    assert(len(Jinja._available_templates) == 1)
    assert(isinstance(Jinja.available_templates, list))
    assert(Jinja.available_templates)
    assert(len(Jinja.available_templates) == 1)
    assert(Jinja._jinja_loader is not None)
    assert(Jinja._jinja_tpl_library is not None)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.template_directory: \
-> template_directory property update requested." in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: \
-> Template directory path set to: {}".format(
        test_template_directory
    ) in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: \
-> Updated template_directory property with: ['test_tpl.j2']" in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: \
-> Jinja successfully loaded:" in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: \
-> Added to_json filter to Jinja Environment object." in out


def test_template_directory_property_invalid_value(capsys):
    """ JinjaUtils Class Template Directory Property Invalid Value Test

    This test will test the getter and setter methods of the
    template_directory property to ensure that if an invalid value is passed
    to the property setter method, that error is handled and reported
    correctly, and that the invalid values do not cause an exception.

    Expected Result:
      Object template_directory bad argument value is ignored causing the
      property value to remain at the default values. Error is thrown to log.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test if a bad value is passed for the template directory
    Jinja.template_directory = 42

    assert(Jinja._template_directory is None)
    assert(Jinja.template_directory == "A template directory has not yet \
been configured.")
    assert(isinstance(Jinja._available_templates, list))
    assert(not Jinja._available_templates)
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)

    # Re-write to stderr to capture the error logs
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.template_directory: \
-> Provided path expected type str but received:" in err
    assert "ERROR   CLS->JinjaUtils.template_directory: \
-> Aborting property update..." in err


def test_template_directory_property_invalid_path(capsys):
    """ JinjaUtils Class Template Directory Property Invalid Path Test

    This test will test the getter and setter methods of the
    template_directory property to ensure that if an invalid or non existing
    path is passed to the property setter method, that error is handled and
    reported correctly, and that the invalid path does not cause an exception.

    Expected Result:
      Object template_directory bad path argument is ignored causing the
      property value to remain at the default values. Error is thrown to log.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test if a bad value is passed for the template directory
    Jinja.template_directory = "I Love Pancakes!"

    assert(Jinja._template_directory is None)
    assert(Jinja.template_directory == "A template directory has not yet \
been configured.")
    assert(isinstance(Jinja._available_templates, list))
    assert(not Jinja._available_templates)
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)

    # Re-write to stderr to capture the error logs
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.template_directory: \
-> Provided directory path doesn't exit." in err
    assert "ERROR   CLS->JinjaUtils.template_directory: \
-> Aborting property update..." in err


def test_template_directory_property_empty_dir(capsys):
    """ JinjaUtils Class Template Directory Property Empty Directory Test

    This test will test the getter and setter methods of the
    template_directory property to ensure that if an empty directory path is
    provided, that the directory path is loaded, but available_templates gets
    set to an empty list.

    Expected Result:
      Object template_directory set to provided path, available_templates
      property is returned as empty list.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Set and create an empty directory to test the loader with.
    test_empty_template_directory = os.path.join(
        test_template_directory,
        'empty'
    )

    # If the test empty directory does not exist, then create it,
    if not os.path.exists(test_empty_template_directory):
        os.mkdir(test_empty_template_directory)

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set the template directory to the test directory created previously.
    Jinja.template_directory = test_empty_template_directory

    # Test for expected property values.
    assert(Jinja._template_directory == test_empty_template_directory)
    assert(Jinja.template_directory == test_empty_template_directory)
    assert(isinstance(Jinja._available_templates, list))
    assert(not Jinja._available_templates)
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)
    assert(Jinja._jinja_loader is not None)
    assert(Jinja._jinja_tpl_library is not None)

    # Re-write to stderr to capture the error logs
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "Jinja successfully loaded: {}".format(
        Jinja.template_directory
    ) in out
    assert "Added to_json filter to Jinja Environment object" in out


def test_available_templates_property_invalid(capsys):
    """ JinjaUtils Class Available Templates Property Invalid Value Test

    This test will ensure that if the _available_templates property is set
    to a non expected value type that a blank list instead is returned.

    Expected Result:
      Object _available_templates set to invalid value, available_templates
      property is returned as empty list.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set the _available_templates property to None and test return.
    Jinja._available_templates = None
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)

    # Set the _available_templates property to invalid value and test return.
    Jinja._available_templates = "FailTest"
    assert(isinstance(Jinja.available_templates, list))
    assert(not Jinja.available_templates)


##############################
# Test Load template method: #
##############################
def test_load_template(capsys):
    """ JinjaUtils Class Load Template Method Test

    This test will test the getters and setter methods for the
    object template load class method. This test will load a valid
    template directory, then load a valid template and ensure that the
    template has been loaded and is available as expected.

    Expected Result:
      Valid template will be loaded and available for future actions such as
      render and write.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set the template directory to the test directory.
    assert(Jinja.load == "No template has been loaded!")

    # Load any templates found in the template directory
    Jinja.template_directory = test_template_directory

    # Load the first template using the setter and test the loaded template.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template is not None)
    assert(Jinja.load is not None)
    assert(Jinja._jinja_loader is not None)
    assert(Jinja._jinja_tpl_library is not None)
    assert(isinstance(Jinja._jinja_tpl_library, object))
    assert(isinstance(Jinja._available_templates, list))
    assert(Jinja._available_templates[0] == 'test_tpl.j2')
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    assert(Jinja.load == 'test_tpl.j2')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: \
-> Loaded template file from:" in out


def test_load_template_invalid_template(capsys):
    """ JinjaUtils Class Load Invalid Template Method Test

    This test will test the getters and setter methods for the
    object template load class method. This test will attempt to load a non
    existant template from the loaded template directory, and ensure that the
    improper template error is handled correctly.

    Expected Result:
        No template will be loaded, error will reflect that the requested
        template does not exist.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set the template directory to the test directory.
    assert(Jinja.load == "No template has been loaded!")
    Jinja.template_directory = test_template_directory

    # Load the first template using the setter and test the loaded template.
    Jinja.load = 'test_tpl.j3'
    assert(Jinja._loaded_template is None)
    assert(Jinja.load == "No template has been loaded!")
    assert(Jinja._jinja_loader is not None)
    assert(Jinja._jinja_tpl_library is not None)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "WARNING CLS->JinjaUtils.load: \
-> Requested template not found in:" in out


def test_load_template_file(capsys):
    """ JinjaUtils Class Load Template File Method Test

    This test will test the getters and setter methods for the
    object template load class method. This test will load a valid
    template from a file, and then test the loaded template to ensure
    that the request file load occurred successfully.

    Expected Result:
      Valid template file will be loaded and available for future actions
      such as render and write.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Create a secondary file thats not loaded in the
    # jinja template library, write it to disk, and then try to load it.
    file_template = "hello {{ world }}"

    jinja_test_template_filename = os.path.join(
        test_template_directory,
        'test_file_tpl.j2'
    )

    jinja_test_file_template = open(jinja_test_template_filename, "w")
    jinja_test_file_template.write(file_template)
    jinja_test_file_template.close()

    # Test to make sure the file was written correctly
    assert(os.path.exists(jinja_test_template_filename))

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Load the file template and test for expected values.
    Jinja.load = jinja_test_template_filename

    # Test to ensure template directory, jinja_loader and jinja_tpl_library
    # are not set, but the template file itself is still loaded.
    assert(Jinja._loaded_template is not None)
    assert(Jinja.load is not None)
    assert(Jinja.template_directory == 'A template directory has not yet \
been configured.')
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)
    assert(Jinja._loaded_template.name == 'test_file_tpl.j2')
    assert(Jinja.load == 'test_file_tpl.j2')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: \
-> Loaded template file from path:" in out
    assert "DEBUG   CLS->JinjaUtils.load: \
-> Loaded template name set to: {}".format(
        os.path.basename(jinja_test_template_filename)
    ) in out


def test_load_template_invalid_type(capsys):
    """ JinjaUtils Class Load Invalid Type Method Test

    This test will test the getters and setter methods for the
    object template load class method. This test will attempt to
    issue the load operation on a non template bad data type to
    ensure that the improper template error is handled correctly.

    Expected Result:
        No template will be loaded, error will reflect that the requested
        template does not exist.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set the template directory to the test directory.
    assert(Jinja.load == "No template has been loaded!")

    # Attempt to call the load method with an invalid data type.
    Jinja.load = 42
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.load: \
-> load expected str template but received" in err

    # Check for expected object state
    assert(Jinja._loaded_template is None)
    assert(Jinja.load == "No template has been loaded!")
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)


def test_load_template_invalid_type2(capsys):
    """ JinjaUtils Class Load Invalid Type 2 Method Test

    This test will test the getters and setter methods for the
    object template load class method. This test will attempt to
    issue the load operation with an object to ensure that the
    improper template error is handled correctly.

    Expected Result:
        No template will be loaded, error will reflect that the requested
        template does not exist.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set the template directory to the test directory.
    assert(Jinja.load == "No template has been loaded!")

    # Attempt to call the load method with an invalid data type.
    Jinja.load = Jinja
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.load: \
-> EXCEPTION occurred in: 'CLS->JinjaUtils.load', on line" in err

    # Check for expected object state
    assert(Jinja._loaded_template is None)
    assert(Jinja.load == "No template has been loaded!")
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_tpl_library is None)


################################
# Test Render template method: #
################################
def test_render_template(capsys):
    """ JinjaUtils Class Jinja Render Template Method Test

    This test will test the class render method, by attempting to load and
    render a valid template from the configured template directory.

    Expected Result:
        Valid template will be loaded and rendered from the loaded jinja
        template library/directory.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Load template library.
    Jinja.template_directory = test_template_directory

    # Load a valid template that can be used to test the render method.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    assert(Jinja.load == 'test_tpl.j2')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: \
-> Loaded template file from:" in out

    # Before attempting to render the template make sure that
    # no existing rendered template response comes back
    assert(Jinja.rendered == "No template has been rendered!")
    assert(Jinja._rendered_template is None)

    # Render the Template file!
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})
    assert(Jinja._rendered_template is not None)
    test_rendered_template = Jinja.rendered.title()
    test_rendered_template = test_rendered_template.strip()
    assert('Name = Pytest' in test_rendered_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.render: \
-> render of loaded template requested." in out
    assert "INFO    CLS->JinjaUtils.render: \
-> <Template 'test_tpl.j2'> rendered successfully!" in out


def test_render_template_file(capsys):
    """ JinjaUtils Class Jinja Render Template File Method Test

    This test will test the class render method, by attempting to define a
    template variable, write that variable to disk as a template file, load
    the written template, and then attempt to render the written template file

    Expected Result:
        Valid template file will be loaded and rendered successfully.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Define a template variable that will be used to test the variable render
    file_template = "hello {{ world }}"

    # Define the new template file path
    jinja_test_template_filename = os.path.join(
        test_template_directory,
        'test_file_tpl.j2'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Attempt to load the variable template and perform the render operation.
    jinja_test_file_template = open(jinja_test_template_filename, "w")
    jinja_test_file_template.write(file_template)
    jinja_test_file_template.close()
    assert(os.path.exists(jinja_test_template_filename))

    # Load the template
    Jinja.load = jinja_test_template_filename
    assert(Jinja._loaded_template.name == 'test_file_tpl.j2')
    assert(Jinja.load == 'test_file_tpl.j2')

    # Render the template
    Jinja.render(world="PyTest")
    assert(str(Jinja.rendered) == "hello PyTest")

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: \
-> Loaded template file from path:" in out
    assert "DEBUG   CLS->JinjaUtils.load: \
-> Loaded template name set to: {}".format(
        os.path.basename(jinja_test_template_filename)
    ) in out


def test_render_exception_invalid_variable(capsys):
    """ JinjaUtils Class Jinja Render Method Invalid Variable Exception Test

    This test will test the class render method, and attempt to execute the
    render method on a template with undefined variables assigned during the
    render method call. This should trigger an expected Exception of undefined
    variable type within the render operation, and gracefully handle the
    expected exception condition.

    Expected Result:
        Expected Exception conditions should be hit and handled appropriately.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Load template library.
    Jinja.template_directory = test_template_directory

    # Load the first template and test the things.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    assert(Jinja.load == 'test_tpl.j2')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: \
-> Loaded template file from:" in out

    # Render the Template file without passing the referenced context variable
    Jinja.render(debug=True)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.render: \
-> EXCEPTION occurred in: 'CLS->JinjaUtils.render', on line 650: \
-> 'context' is undefined" in err


def test_render_exception_template_none(capsys):
    """ JinjaUtils Class Jinja Render Method No Template Exception Test

    This test will test the class render method, and attempt to execute the
    render method on a template that is defined of type None. This condition
    should hit an expected exception condition that will be handled
    appropriately.

    Expected Result:
        Expected Exception conditions should be hit and handled appropriately.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test the environment to ensure that loaded template is none
    assert(Jinja._loaded_template is None)

    # Attempt to render the Nonetype template
    Jinja.render(world='PyTest')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.render: \
-> No template loaded, Aborting render!" in err


def test_render_exception_template_type(capsys):
    """ JinjaUtils Class Jinja Render Method Invalid Template Exception Test

    This test will test the class render method, and attempt to execute the
    render method on a template that is defined of type int or invalid. This
    condition should hit an expected exception condition that will be handled
    appropriately.

    Expected Result:
        Expected Exception conditions should be hit and handled appropriately.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test the environment to ensure that loaded template is none
    assert(Jinja._loaded_template is None)

    # Set a bad loaded template type and attempt to render the template.
    Jinja._loaded_template = 42
    Jinja.render(world='PyTest')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.render: \
-> No template loaded, Aborting render!" in err


def test_render_exception_template_object(capsys):
    """ JinjaUtils Class Jinja Render Method Invalid Template Object Test

    This test will test the class render method, and attempt to execute the
    render method on a template that is defined as an object. This condition
    should hit an expected exception condition that will be handled
    appropriately.

    Expected Result:
        Expected Exception conditions should be hit and handled appropriately.
    """
    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test the environment to ensure that loaded template is none
    assert(Jinja._loaded_template is None)

    # Set a bad loaded template type and attempt to render the template.
    Jinja._loaded_template = Jinja
    Jinja.render(world='PyTest')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.render: \
-> No template loaded, Aborting render!" in err


###############################
# Test Write template method: #
###############################
def test_write_not_rendered(capsys):
    """ JinjaUtils Class Jinja Write No Template Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the object write method against an instance that does not have a
    rendered template object. This operation should fail gracefully.

    Expected Result:
        No rendered template available error.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Test for any previously rendered templates in memory.
    assert(Jinja.rendered == "No template has been rendered!")
    Jinja.render()

    # Attempt to write the template.
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='test.txt'
    )
    assert(not write_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "WARNING CLS->JinjaUtils.rendered: \
-> Render method not called or failed to render." in out
    assert "WARNING CLS->JinjaUtils.rendered: \
-> No rendered template available for write request!" in out


def test_write_output_none(capsys):
    """ JinjaUtils Class Jinja Write Output None Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method with invalid None type values set for the output
    directory and output file name.

    Expected Result:
        Template write method will error gracefully on write attempt.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load the test template and test expected environment.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: \
-> Loaded template file from:" in out

    # With the template loaded, attempt to render the template.
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})
    assert(Jinja._rendered_template is not None)
    test_rendered_template = Jinja.rendered.title()
    test_rendered_template = test_rendered_template.strip()
    assert('Name = Pytest' in test_rendered_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.render: \
-> render of loaded template requested." in out
    assert "INFO    CLS->JinjaUtils.render: \
-> <Template 'test_tpl.j2'> rendered successfully!" in out

    # Attempt the write operation setting both output values to None.
    write_template = Jinja.write(output_directory=None, output_file=None)
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)
    assert(not write_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: \
-> Invalid output directory specified in write call" in err


def test_write_output_invalid_directory(capsys):
    """ JinjaUtils Class Jinja Write Output Invalid Directory Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method with an invalid directory path specified for the
    output directory value.

    Expected Result:
        Template write method will error gracefully on write attempt.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load & Render the template, then proceed with write fail testing.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})

    # Attempt the write operation passing an invalid output directory value.
    write_template = Jinja.write(
        output_directory='/foo/bar/no/love',
        output_file='pytest_template'
    )
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)
    assert(not write_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: \
-> Invalid output directory specified in write call" in err


def test_write_output_invalid_dir_file(capsys):
    """ JinjaUtils Class Jinja Write Output Invalid Dir File Value Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method passing a file name for the output directory value.

    Expected Result:
        Template write method will error gracefully on write attempt.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load & Render the template, then proceed with write fail testing.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})

    # Attempt the write operation passing a filename as the output directory.
    write_template = Jinja.write(output_directory=os.path.join(
        test_template_directory,
        'test_tpl.j2'
        ),
        output_file='pytest_template'
    )
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)
    assert(not write_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: \
-> Invalid output directory specified in write call" in err


def test_write_output_invalid_filename(capsys):
    """ JinjaUtils Class Jinja Write Output Invalid Filename Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method with an invalid filename specified for the
    output file value.

    Expected Result:
        Template write method will error gracefully on write attempt.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load & Render the template, then proceed with write fail testing.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})

    # Attempt the write operation passing an invalid value for the output file
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file=42
    )
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file is None)
    assert(not write_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: \
-> Output expected str filename but received" in err


def test_write_output_file_path(capsys):
    """ JinjaUtils Class Jinja Write Output File Path Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method passing a directory path for the file output
    variable. The method should strip the path from the file name and
    write the file to the directory_output/file_base_name path.

    Expected Result:
        Template write method will write the template to the output directory
        / output file base name location.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load & Render the template, then proceed with write fail testing.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})

    # Attempt the write operation setting output file to path.
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='/my/foo/pytest/file.test'
    )
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file == 'file.test')
    assert(write_template)
    assert(
        os.path.isfile(
            os.path.join(
                Jinja._output_directory,
                Jinja._output_file
            )
        )
    )

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.write: \
-> Output file has been set to: {}!".format(Jinja._output_file) in out
    assert "DEBUG   CLS->JinjaUtils.write: \
-> Writing rendered template to output file: {}".format(
        os.path.join(
            Jinja._output_directory,
            Jinja._output_file
        )
    ) in out
    assert "INFO    CLS->JinjaUtils.rendered: \
-> {} written successfully!".format(
            os.path.join(
                Jinja._output_directory,
                Jinja._output_file
            )
        ) in out


def test_write_backup(capsys):
    """ JinjaUtils Class Jinja Write Backup Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method twice, to test the default behavior of the write
    method to backup any existing file found that would otherwise be
    automatically replaced or over written.

    Expected Result:
        Template write method will write the template to the output directory
        / file twice, creating a backup of the first file before over writing
        the file on the second pass.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load & Render the template, then proceed with write fail testing.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})

    # Attempt the write operation.
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='/my/foo/pytest/file.test'
    )

    # Now write the rendered file a second time to trigger the backup case
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='/my/foo/pytest/file.test'
    )
    # Find the backup file
    backup_file = None
    for root, dirs, files in os.walk(test_template_directory):
        for file in files:
            if file.endswith('.bak'):
                backup_file = file
                break
    # Test the environmet to ensure expected configuration
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file == 'file.test')
    assert(
        os.path.isfile(
            os.path.join(
                Jinja._output_directory,
                Jinja._output_file
            )
        )
    )
    assert(os.path.isfile(os.path.join(test_template_directory, backup_file)))
    assert(write_template)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.write: \
-> Output file has been set to: {}!".format(Jinja._output_file) in out
    assert "DEBUG   CLS->JinjaUtils.write: \
-> Writing rendered template to output file: {}".format(
        os.path.join(
            Jinja._output_directory,
            Jinja._output_file
        )
    ) in out
    assert "INFO    CLS->JinjaUtils.write: \
-> file.test backed up to: {}".format(
        os.path.join(
            Jinja._output_directory,
            backup_file
        )
    ) in out
    assert "INFO    CLS->JinjaUtils.rendered: \
-> {} written successfully!".format(
        os.path.join(
            Jinja._output_directory,
            Jinja._output_file
        )
    ) in out


def test_write_backup_disabled(capsys):
    """ JinjaUtils Class Jinja Write Backup Disabled Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method twice, disabling backups on the second write attempt
    and then checking the contents of the written file to ensure that the file
    was over written as intended and that no backup of the file was taken.

    Expected Result:
        Template write method will write the template to the output directory
        / file twice, disabling backups, causing the original file to simply
        be overwritten with no backup taken.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load & Render the template, then proceed with write fail testing.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})

    # Attempt the write operation.
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='test_tpl.html'
    )

    # Test the file to ensure it was written as expected
    test_rendered_file = None
    test_rendered_file = os.path.join(test_template_directory, 'test_tpl.html')
    if test_rendered_file is not None:
        test_rendered_file = test_rendered_file.strip()
        load_file = open(test_rendered_file, "r")
        test_rendered_file = load_file.read()
        test_rendered_file = test_rendered_file.strip()
        load_file.close()
    assert('name = PyTest' in test_rendered_file)

    # Re-Render the file, and overwrite the existing copy
    Jinja.render(name="OverWrite", debug=True, context={'key': 'value'})
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='test_tpl.html',
        backup=False
    )
    # Find the backup file
    backup_file = None
    for root, dirs, files in os.walk(test_template_directory):
        for file in files:
            if file.startswith('test_') and file.endswith('.bak'):
                backup_file = file
                break
    # Test to ensure that no backup of the file was taken.
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file == 'test_tpl.html')
    assert(
        os.path.isfile(
            os.path.join(
                Jinja._output_directory,
                Jinja._output_file
            )
        )
    )
    assert(backup_file is None)
    assert(write_template)

    # Test the Jinja template to verify that it has been overwritten.
    test_rendered_file = None
    test_rendered_file = os.path.join(test_template_directory, 'test_tpl.html')
    if test_rendered_file is not None:
        test_rendered_file = test_rendered_file.strip()
        load_file = open(test_rendered_file, "r")
        test_rendered_file = load_file.read()
        test_rendered_file = test_rendered_file.strip()
        load_file.close()
    assert('name = OverWrite' in test_rendered_file)

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.write: \
-> Output file has been set to: {}!".format(Jinja._output_file) in out
    assert "DEBUG   CLS->JinjaUtils.write: \
-> Writing rendered template to output file: {}".format(
        os.path.join(
            Jinja._output_directory,
            Jinja._output_file
        )
    ) in out
    assert "WARNING CLS->JinjaUtils.write: \
-> File backup is disabled, overwritting: {}!".format(
        Jinja._output_file
    ) in out
    assert "INFO    CLS->JinjaUtils.rendered: \
-> {} written successfully!".format(
        os.path.join(
            Jinja._output_directory,
            Jinja._output_file
        )
    ) in out


def test_write_backup_invalid(capsys):
    """ JinjaUtils Class Jinja Write Backup Invalid Method Test

    This test will test JinjaUtils write method. This test will attempt to
    call the write method twice, passing an invalid non bool value for the
    backup setting on the second write call. The write function should ignore
    the bad value, and set the backup mode to its default enabled setting.

    Expected Result:
        Template write method will write the template to the output directory
        / file twice. The invalid backup value should be ignored, and backup
        should be set to the default setting of true, which will create the
        expected backup file on the second write operation.
    """
    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(
        current_directory,
        'pytest_template_directory'
    )

    # Instantiate a JinjaUtils object, and test for expected test values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Set up the Class object template directory.
    Jinja.template_directory = test_template_directory

    # Ensure that no template is currently rendered in memory
    assert(Jinja.rendered == "No template has been rendered!")

    # Load & Render the template, then proceed with write fail testing.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.name == 'test_tpl.j2')
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})

    # Attempt the write operation.
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='test_tpl.html'
    )

    # Re-Render the file, and passing a invalid backup value
    write_template = Jinja.write(
        output_directory=test_template_directory,
        output_file='test_tpl.html',
        backup=42
    )

    # Find the backup file
    backup_file = None
    for root, dirs, files in os.walk(test_template_directory):
        for file in files:
            if file.endswith('.bak'):
                backup_file = file
                break

    # Capture stdout, stderr to check the log messages
    # for the expected outputs.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "WARNING CLS->JinjaUtils.write: \
-> Backup expected bool value but received type:" in out
    assert "INFO    CLS->JinjaUtils.write: \
-> test_tpl.html backed up to:" in out
    assert "written successfully!" in out
    assert(backup_file)
    assert(write_template)
