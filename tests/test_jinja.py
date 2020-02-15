# Run test suite with `poetry run pytest tests -v`
# Run only this test with `poetry run pytest tests/test_jinja.py -v`
# Run only a single test with `poetry run pytest tests/test_jinja.py::{testname} -v`
# Coverage: poetry run coverage run -m --omit=tests/* --source=. pytest tests/test_jinja.py
# Coverage: run coverage html --omit=tests/* -i
################
# Imports:     #
################
from jinjautils import JinjaUtils
import pytest, os, sys, shutil, glob


######################################
# Define Set and Teardown Fixtures:  #
######################################
@pytest.fixture(scope='session', autouse=True)
def setup():
    """JinjaUtils Class PyTest Setup 
    Setup the test environment for the JinjaUtils class unit tests.
    """
    # Define the test directory
    current_directory = os.getcwd()
    test_template_directory = os.path.join(current_directory, 'pytest_template_directory')

    # Test Template
    pytest_template = """
    name = {{ name }}
    verbose = {{ debug }}
    context = {{ context }}
    """

    # Create a fresh test directory
    if not os.path.exists(test_template_directory):
        os.mkdir(test_template_directory)
    
    # Write a testing template to the testing template directory
    pytest_jinja_template = open(os.path.join(test_template_directory, 'test_tpl.j2'), "w")
    pytest_jinja_template.write(pytest_template)
    pytest_jinja_template.close()

    # Yield the setup, and when finished, tear down the test directory.
    yield
    if os.path.exists(test_template_directory):
        shutil.rmtree(test_template_directory)


######################################
# Test GitHubAPI Repository Object:  #
######################################
def test_init():
    """JinjaUtils Class Constructor Test
    This test will instantiate a new JinjaUtils object and test to ensure the object attributes match the
    expected instantiation values.
    """

    # Instantiate a JinjaUtils object, and test the returned object instance for default values.
    Jinja = JinjaUtils()
    assert(isinstance(Jinja, object))

    # Test default instantiation values
    assert(Jinja._verbose == False)
    assert(Jinja._log is None)
    assert(Jinja._log_context == "CLS->JinjaUtils")
    assert(Jinja._trim_blocks == True)
    assert(Jinja._lstrip_blocks == True)
    assert(Jinja._template_directory is None)
    assert(isinstance(Jinja._available_templates, list))
    assert(len(Jinja._available_templates) == 0)
    assert(Jinja._loaded_template is None)
    assert(Jinja._rendered_template is None)
    assert(Jinja._jinja_loader is None)
    assert(Jinja._jinja_template_library is None)
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)


def test_log(capsys):
    """JinjaUtils Class Log Test
    This test will test the log method to ensure that logs are written to stdout, stderr
    """

    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test verbose setting
    assert(Jinja._verbose == True)

    # Write a test log entry
    Jinja.log("Pytest debug log write test", 'debug', 'test_log')
    Jinja.log("Pytest info log write test", 'info', 'test_log')
    Jinja.log("Pytest warning log write test", 'warning', 'test_log')
    Jinja.log("Pytest error log write test", 'error', 'test_log')

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.test_log: -> Pytest debug log write test" in out
    assert "INFO    CLS->JinjaUtils.test_log: -> Pytest info log write test" in out
    assert "WARNING CLS->JinjaUtils.test_log: -> Pytest warning log write test" in out
    assert "ERROR   CLS->JinjaUtils.test_log: -> Pytest error log write test" in err


def test_log_object(capsys):
    """JinjaUtils Class Log Object Test
    This test will test the log method to ensure that logs are to a provided log object
    """

    # Create a test log object that will just collect logs and add them to a list, which we can check for produced log messages
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

    # Instantiate a log object
    LogObj = Log()
    
    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True, log=LogObj)
    assert(isinstance(Jinja, object))
    assert(isinstance(Jinja.log, object))

    # Test verbose setting
    assert(Jinja._verbose == True)
    assert(Jinja._log is not None)

    # Test the Log object to make sure the expected attributes exist
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

    # Test that the Log object debug_logs, info_logs, warning_logs and error_logs properties are lists
    assert(isinstance(Jinja._log.debug_logs, list))
    assert(isinstance(Jinja._log.info_logs, list))
    assert(isinstance(Jinja._log.warning_logs, list))
    assert(isinstance(Jinja._log.error_logs, list))

    # Test that each of the log_lists have items written into them
    assert(len(LogObj.debug_logs) == 1)
    assert(len(LogObj.info_logs) == 1)
    assert(len(LogObj.warning_logs) == 1)
    assert(len(LogObj.error_logs) == 1)

    # Test the log messages to make sure they match the written logs
    assert(LogObj.debug_logs[-1] == "CLS->JinjaUtils.test_log_object: -> Pytest log debug test")
    assert(LogObj.info_logs[-1] == "CLS->JinjaUtils.test_log_object: -> Pytest log info test")
    assert(LogObj.warning_logs[-1] == "CLS->JinjaUtils.test_log_object: -> Pytest log warning test")
    assert(LogObj.error_logs[-1] == "CLS->JinjaUtils.test_log_object: -> Pytest log error test")

    # Test to ensure that passing a non object to the log is properly caught.
    JinjaBadLog = JinjaUtils(verbose=True, log=42)
    assert(isinstance(JinjaBadLog, object))
    assert(JinjaBadLog._log is None)


def test_trim_blocks(capsys):
    """JinjaUtils Class Trim Blocks Test
    This test will test the trim_blocks getter and setter property methods.
    """

    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test trim_blocks setting
    assert(Jinja._trim_blocks == True)
    assert(Jinja.trim_blocks == True)

    # Call the Setter to update the property value
    Jinja.trim_blocks = False
    assert(Jinja._trim_blocks == False)
    assert(Jinja.trim_blocks == False)

    # Call the Setter and provide it with a non bool value to test the error condition
    Jinja.trim_blocks = 42

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.trim_blocks: -> trim_blocks property update requested." in out
    assert "INFO    CLS->JinjaUtils.trim_blocks: -> trim_blocks property requested." in out
    assert "ERROR   CLS->JinjaUtils.trim_blocks: -> Property trim_blocks argument expected bool but received type: <class 'int'>. Aborting update!" in err


def test_lstrip_blocks(capsys):
    """JinjaUtils Class LStrip Blocks Test
    This test will test the lstrip_blocks getter and setter property methods.
    """

    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Test lstrip_blocks setting
    assert(Jinja._lstrip_blocks == True)
    assert(Jinja.lstrip_blocks == True)

    # Call the Setter to update the property value
    Jinja.lstrip_blocks = False
    assert(Jinja._lstrip_blocks == False)
    assert(Jinja.lstrip_blocks == False)

    # Call the Setter and provide it with a non bool value to test the error condition
    Jinja.lstrip_blocks = 42

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.lstrip_blocks: -> lstrip_blocks property update requested." in out
    assert "INFO    CLS->JinjaUtils.lstrip_blocks: -> lstrip_blocks property requested." in out
    assert "ERROR   CLS->JinjaUtils.lstrip_blocks: -> Property lstrip_blocks argument expected bool but received type: <class 'int'>. Aborting update!" in err


def test_verbose(capsys):
    """JinjaUtils Class Verbose Test
    This test will test the verbose getter and setter property methods.
    """

    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils()
    assert(isinstance(Jinja, object))

    # Test verbose setting
    assert(Jinja._verbose == False)
    assert(Jinja.verbose == False)

    # Call the Setter to update the property value
    Jinja.verbose = True
    assert(Jinja._verbose == True)
    assert(Jinja.verbose == True)

    # Call the Setter and provide it with a non bool value to test the error condition
    Jinja.verbose = 42

    # Capture stdout, stderr to test log messages
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.verbose: -> verbose property update requested." in out
    assert "INFO    CLS->JinjaUtils.verbose: -> verbose property requested." in out
    assert "ERROR   CLS->JinjaUtils.verbose: -> Property verbose argument expected bool but received type: <class 'int'>. Aborting update!" in err

    Jinja2 = JinjaUtils(verbose=42)
    assert(Jinja2._verbose == False)
    assert(Jinja2.verbose == False)


def test_exception_handler(capsys):
    """JinjaUtils Class Exception Handler Test
    This test will test the class wide exception handler.
    """

    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Write a log with a bad value to trigger an exception.
    Jinja.log('Message', 42, 2)
    
    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.log: -> An EXCEPTION has occurred in 'CLS->JinjaUtils.log'" in err


def test_template_directory(capsys):
    """JinjaUtils Class Template Directory Handler Test
    This test will test the getters and setter methods for the template_directory property.
    """

    ###################
    # Success Test    #
    ###################
    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(current_directory, 'pytest_template_directory')

    # Write a log with a bad value to trigger an exception.
    Jinja.template_directory = test_template_directory
    assert(Jinja.template_directory == test_template_directory)
    assert(Jinja._template_directory == test_template_directory)
    assert(isinstance(Jinja.available_templates, list))
    assert(isinstance(Jinja._available_templates, list))
    assert(len(Jinja.available_templates) == 1)
    assert(len(Jinja._available_templates) == 1)
    assert(Jinja._jinja_loader is not None)
    assert(Jinja._jinja_template_library is not None)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.template_directory: -> template_directory property update requested." in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: -> Template directory path set to: {}".format(test_template_directory) in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: -> Updated template_directory property with: ['test_tpl.j2']" in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: -> Jinja loaded the provided template_directory successfully!" in out
    assert "DEBUG   CLS->JinjaUtils.template_directory: -> Added to_json filter to Jinja Environment object." in out

    ###############################################
    # Invalid template directory type (nonstring) #
    ###############################################
    # To clear the environment for max fail conditions, instantiate a new object
    JinjaTestFail = JinjaUtils(verbose=True)
    assert(isinstance(JinjaTestFail, object))

    # Test if a bad value is passed for the template directory
    JinjaTestFail.template_directory = 42

    assert(JinjaTestFail.template_directory == "No setting found!. Set this property with object.template_directory = 'valid/path/to/template/directory'.")
    assert(JinjaTestFail._template_directory is None)
    assert(isinstance(JinjaTestFail.available_templates, list))
    assert(isinstance(JinjaTestFail._available_templates, list))
    assert(len(JinjaTestFail.available_templates) == 0)
    assert(len(JinjaTestFail._available_templates) == 0)
    assert(JinjaTestFail._jinja_loader is None)
    assert(JinjaTestFail._jinja_template_library is None)

    # Re-write to stderr to capture the error logs
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.template_directory: -> Provided directory path expected type str but received: <class 'int'>" in err
    assert "ERROR   CLS->JinjaUtils.template_directory: -> Aborting property update..." in err

    
    ###############################################
    # Invalid template directory non path string  #
    ###############################################
    # Test if a bad string is passed
    JinjaTestFail.template_directory = "I Love Pancakes!"

    assert(JinjaTestFail.template_directory == "No setting found!. Set this property with object.template_directory = 'valid/path/to/template/directory'.")
    assert(JinjaTestFail._template_directory is None)
    assert(isinstance(JinjaTestFail.available_templates, list))
    assert(isinstance(JinjaTestFail._available_templates, list))
    assert(len(JinjaTestFail.available_templates) == 0)
    assert(len(JinjaTestFail._available_templates) == 0)
    assert(JinjaTestFail._jinja_loader is None)
    assert(JinjaTestFail._jinja_template_library is None)

    # Re-write to stderr to capture the error logs
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.template_directory: -> Provided directory path doesn't exit." in err
    assert "ERROR   CLS->JinjaUtils.template_directory: -> Aborting property update..." in err

    ###############################################
    # Empty Directory Test  #
    ###############################################
    # Set and create an empty directory to test the loader with.
    test_empty_template_directory = os.path.join(test_template_directory, 'empty')
    
    if not os.path.exists(test_empty_template_directory):
        os.mkdir(test_empty_template_directory)
    JinjaTestFail.template_directory = test_empty_template_directory

    assert(JinjaTestFail.template_directory == test_empty_template_directory)
    assert(JinjaTestFail._template_directory == test_empty_template_directory)
    assert(isinstance(JinjaTestFail.available_templates, list))
    assert(isinstance(JinjaTestFail._available_templates, list))
    assert(len(JinjaTestFail.available_templates) == 0)
    assert(len(JinjaTestFail._available_templates) == 0)
    assert(JinjaTestFail._jinja_loader is not None)
    assert(JinjaTestFail._jinja_template_library is not None)

    # Re-write to stderr to capture the error logs
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "Jinja loaded the provided template_directory successfully!" in out
    assert "Template directory path set to: {}".format(test_empty_template_directory) in out


    ####################################################
    # Set available templates to None and call getter  #
    ####################################################
    # Set and create an empty directory to test the loader with.
    JinjaTestFail._available_templates = None
    assert(isinstance(JinjaTestFail.available_templates, list))
    assert(len(JinjaTestFail.available_templates) == 0)


def test_load(capsys):
    """JinjaUtils Class Jinja Load Getter/Setter Test
    This test will test the getters and setter methods for the object load property.
    """ 
    
    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(current_directory, 'pytest_template_directory')

    # Write a log with a bad value to trigger an exception.
    Jinja.template_directory = test_template_directory
    
    ######################################################
    # Try non existant template from template directory: #
    ######################################################
    Jinja.load = 'test_tpl.j3'
    assert(Jinja.load == "No template has been loaded!")

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "WARNING CLS->JinjaUtils.load: -> Requested template not found in template directory:" in out


    ####################################################
    # Load Template from Loaded template directory:    #
    ####################################################
    # Load the first template and test the things.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.filename.endswith('test_tpl.j2'))
    assert(Jinja._loaded_template.filename.endswith(Jinja.load))
    
    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: -> Loaded template file from template_directory" in out


    ####################################################
    # Load Template from File:                         #
    ####################################################
    # Create a secondary file thats not loaded in the jinja loaded template library, and try to load it.
    file_template = "hello {{ world }}"
    jinja_test_template_filename = os.path.join(test_template_directory, 'test_file_tpl.j2')
    jinja_test_file_template = open(jinja_test_template_filename, "w")
    jinja_test_file_template.write(file_template)
    jinja_test_file_template.close()
    assert(os.path.exists(jinja_test_template_filename))

    # Load the file template.
    Jinja.load = jinja_test_template_filename
    assert('template' in Jinja._loaded_template.filename)
    assert(Jinja.load == 'test_file_tpl.j2')

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: -> Loaded template file from path:" in out
    assert "DEBUG   CLS->JinjaUtils.load: -> Loaded template name set to: {}".format(os.path.basename(jinja_test_template_filename)) in out


    #####################################################
    # Load Template With Number to try and bork things: #
    #####################################################
    Jinja.load = 42
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.load: -> load expected template of type str but received type:" in err


    #####################################################
    # Load Template With Object to try and bork things: #
    #####################################################
    Jinja.load = Jinja
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.load: -> An EXCEPTION has occurred in 'CLS->JinjaUtils.load', on line" in err


def test_render(capsys):
    """JinjaUtils Class Jinja Render Getter/Setter Test
    This test will test the getters and setter methods for the object render property.
    """ 

    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(current_directory, 'pytest_template_directory')

    # Write a log with a bad value to trigger an exception.
    Jinja.template_directory = test_template_directory

    ####################################################
    # Load and Render Loaded template directory Tpl:   #
    ####################################################
    # Load the first template and test the things.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.filename.endswith('test_tpl.j2'))
    assert(Jinja._loaded_template.filename.endswith(Jinja.load))
    
    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: -> Loaded template file from template_directory" in out

    # Before attempting to render the template make sure the no rendered template response comes back
    assert(Jinja.rendered == "No template has been rendered!")
    assert(Jinja._rendered_template is None)
    
    # Render the Template file!
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})
    assert(Jinja._rendered_template is not None)
    test_rendered_template = Jinja.rendered.title()
    test_rendered_template = test_rendered_template.strip()
    assert('Name = Pytest' in test_rendered_template)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.render: -> render of loaded template requested." in out
    assert "INFO    CLS->JinjaUtils.render: -> <Template 'test_tpl.j2'> rendered successfully!" in out

    ####################################################
    # Load and Render Template from File:              #
    ####################################################
    # Create a secondary file thats not loaded in the jinja loaded template library, and try to load it.
    file_template = "hello {{ world }}"
    jinja_test_template_filename = os.path.join(test_template_directory, 'test_file_tpl.j2')
    jinja_test_file_template = open(jinja_test_template_filename, "w")
    jinja_test_file_template.write(file_template)
    jinja_test_file_template.close()
    assert(os.path.exists(jinja_test_template_filename))

    # Load the file template.
    Jinja.load = jinja_test_template_filename
    assert('template' in Jinja._loaded_template.filename)
    assert(Jinja.load == 'test_file_tpl.j2')
    
    # Render the template
    Jinja.render(world="PyTest")
    assert(str(Jinja.rendered) == "hello PyTest")

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: -> Loaded template file from path:" in out
    assert "DEBUG   CLS->JinjaUtils.load: -> Loaded template name set to: {}".format(os.path.basename(jinja_test_template_filename)) in out

    ############################################################
    # Try to set the loaded Template to None to hit Exception: #
    ############################################################
    Jinja._loaded_template = None
    Jinja.render(world='PyTest')

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.render: -> No template loaded, Aborting render!" in err

    ##############################################################
    # Try to set the loaded Template to an int to hit Exception: #
    ##############################################################
    Jinja._loaded_template = 42
    Jinja.render(world='PyTest')

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.render: -> No template loaded, Aborting render!" in err

    ##############################################################
    # Try to set the loaded Template to a Jinja Object:          #
    ##############################################################
    Jinja._loaded_template = Jinja
    Jinja.render(world='PyTest')

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.render: -> No template loaded, Aborting render!" in err


def test_write(capsys):
    """JinjaUtils Class Jinja Write Test
    This test will test JinjaUtils write method.
    """ 

    ####################################################
    # Instantiate the Environment:                     #
    ####################################################
    # Instantiate a JinjaUtils object, and test the returned object instance for expected values.
    Jinja = JinjaUtils(verbose=True)
    assert(isinstance(Jinja, object))

    # Declare the test template directory thats constructed during test setup
    current_directory = os.getcwd()
    test_template_directory = os.path.join(current_directory, 'pytest_template_directory')

    # Write a log with a bad value to trigger an exception.
    Jinja.template_directory = test_template_directory

    ####################################################
    # Load the template from the Jinja Environment:    #
    ####################################################
    # Load the first template and test the things.
    Jinja.load = 'test_tpl.j2'
    assert(Jinja._loaded_template.filename.endswith('test_tpl.j2'))
    assert(Jinja._loaded_template.filename.endswith(Jinja.load))
    
    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.load: -> Loaded template file from template_directory" in out

    ####################################################
    # Render the loaded template:                      #
    ####################################################
    Jinja.render(name="PyTest", debug=True, context={'key': 'value'})
    assert(Jinja._rendered_template is not None)
    test_rendered_template = Jinja.rendered.title()
    test_rendered_template = test_rendered_template.strip()
    assert('Name = Pytest' in test_rendered_template)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "INFO    CLS->JinjaUtils.render: -> render of loaded template requested." in out
    assert "INFO    CLS->JinjaUtils.render: -> <Template 'test_tpl.j2'> rendered successfully!" in out

    ####################################################
    # Write the template to disk:                      #
    ####################################################
    # Lets be different and go for some fail cases first

    #=========================
    # Test invalid input types
    #==========================
    write_template = Jinja.write(output_directory=None, output_file=None)
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)
    assert(write_template == False)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: -> Invalid output directory specified in {} request... Aborting request!".format('write') in err

    #==================================
    # Invalid directory path specified
    #==================================
    write_template = Jinja.write(output_directory='/foo/bar/no/love', output_file='pytest_template')
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)
    assert(write_template == False)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: -> Invalid output directory specified in {} request... Aborting request!".format('write') in err

    #==================================
    # Output directory set to file
    #==================================
    write_template = Jinja.write(output_directory=os.path.join(test_template_directory, 'test_tpl.j2'), output_file='pytest_template')
    assert(Jinja._output_directory is None)
    assert(Jinja._output_file is None)
    assert(write_template == False)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: -> Invalid output directory specified in {} request... Aborting request!".format('write') in err

    #==================================
    # Invalid output file name
    #==================================
    write_template = Jinja.write(output_directory=test_template_directory, output_file=42)
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file is None)
    assert(write_template == False)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert "ERROR   CLS->JinjaUtils.write: -> Output file name expected str value but received type" in err

    #==================================
    # Output file set to file path
    #==================================
    write_template = Jinja.write(output_directory=test_template_directory, output_file='/my/foo/pytest/file.test')
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file == 'file.test')
    assert(write_template == True)
    assert(os.path.isfile(os.path.join(Jinja._output_directory, Jinja._output_file)))

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.write: -> Output file has been set to: {}!".format(Jinja._output_file) in out
    assert "DEBUG   CLS->JinjaUtils.write: -> Writing rendered template to output file: {}".format(os.path.join(Jinja._output_directory, Jinja._output_file)) in out
    assert "INFO    CLS->JinjaUtils.write: -> {} written successfully!".format(os.path.join(Jinja._output_directory, Jinja._output_file)) in out

    #==================================
    # test existing file backup
    #==================================
    # File should already exist from the previous test.
    write_template = Jinja.write(output_directory=test_template_directory, output_file='/my/foo/pytest/file.test')
    # Find the backup file
    backup_file = None
    for root, dirs, files in os.walk(test_template_directory):
        for file in files:
            if file.endswith('.bak'):
                backup_file = file
                break
    # Assert the things.    
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file == 'file.test')
    assert(os.path.isfile(os.path.join(Jinja._output_directory, Jinja._output_file)))
    assert(os.path.isfile(os.path.join(test_template_directory, backup_file)))
    assert(write_template == True)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.write: -> Output file has been set to: {}!".format(Jinja._output_file) in out
    assert "DEBUG   CLS->JinjaUtils.write: -> Writing rendered template to output file: {}".format(os.path.join(Jinja._output_directory, Jinja._output_file)) in out
    assert "INFO    CLS->JinjaUtils.write: -> file.test backed up to: {}".format(os.path.join(Jinja._output_directory, backup_file)) in out
    assert "INFO    CLS->JinjaUtils.write: -> {} written successfully!".format(os.path.join(Jinja._output_directory, Jinja._output_file)) in out


    #==================================
    # test no backup
    #==================================
    # File should already exist from the previous test.
    write_template = Jinja.write(output_directory=test_template_directory, output_file='test_tpl.j2', backup=False)
    # Find the backup file
    backup_file = None
    for root, dirs, files in os.walk(test_template_directory):
        for file in files:
            if file.startswith('test_') and file.endswith('.bak'):
                backup_file = file
                break
    # Assert the things.    
    assert(Jinja._output_directory == test_template_directory)
    assert(Jinja._output_file == 'test_tpl.j2')
    assert(os.path.isfile(os.path.join(Jinja._output_directory, Jinja._output_file)))
    assert(backup_file is None)
    assert(write_template == True)
    
    # Test the Jinja template to verify that it has been overwritten.
    test_rendered_file = None 
    test_rendered_file = os.path.join(test_template_directory, 'test_tpl.j2')
    if test_rendered_file is not None:
        test_rendered_file = test_rendered_file.strip()
        load_file = open(test_rendered_file, "r")
        test_rendered_file = load_file.read()
        test_rendered_file = test_rendered_file.strip()
        load_file.close()
    assert('name = PyTest' in test_rendered_file)

    # Capture stdout, stderr to check the log messages for the expected exception.
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
    assert "DEBUG   CLS->JinjaUtils.write: -> Output file has been set to: {}!".format(Jinja._output_file) in out
    assert "DEBUG   CLS->JinjaUtils.write: -> Writing rendered template to output file: {}".format(os.path.join(Jinja._output_directory, Jinja._output_file)) in out
    assert "WARNING CLS->JinjaUtils.write: -> Existing file backup disabled, {} will be overwritten!".format(Jinja._output_file) in out
    assert "INFO    CLS->JinjaUtils.write: -> {} written successfully!".format(os.path.join(Jinja._output_directory, Jinja._output_file)) in out


