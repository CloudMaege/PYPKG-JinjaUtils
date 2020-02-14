##############################################################################
# CloudMage : Jinja Templating Helper Class to simplify using Jinja Templates
#=============================================================================
# CloudMage Jinja Helper Object Utility/Library
#   - Find, Load, and Render Jinja Templates with Simplicity.
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/13/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Pip Installed Modules:
from jinja2 import Template, Environment, FileSystemLoader

# Import Base Python Modules
import json, os, sys, inspect, ntpath

DefaultTemplateDir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

#####################
# Class Definition: #
#####################
class JinjaUtils(object):
    """CloudMage Jinja Helper Class
    This class is designed to make defining, loading, and rendering Jinja templates easily. It provides helper methods that will allow you to construct a Jinja object that will make loading, rendering and writing templates available through the instantiated object constructed by this class.
    """

    def __init__(self, verbose=False, log=None):
        '''JinjaHelper Class Constructor'''

        ##### Class Public Properties and Attributes ######
        self.verbose = verbose

        ##### Class Private Properties and Attributes ######
        # Getter and Setter propert vars
        self._trim_blocks = True
        self._lstrip_blocks = True
        self._template_directory = None  
        self._available_templates = []
        self._loaded_template = None
        self._rendered_template = None
        
        # Jinja Objects using Jinja FileSystemLoader, and Jinja Environment objects.
        self._jinja_loader = None
        self._jinja_template_library = None
        
       
        
        self._output_directory = None
        self._output_file = None

        ##### Method Properties ######
        # self.trim_blocks
        # self.lstrip_blocks
        # self.template_directory

        ##### Init and populate the return the requested object instance ######
        # self._parse_url()
        # self._repository_url()
        # self._repo_data = self._request_handler(self._repo_request_url)
        # self.data = self._repo_data


    ############################################
    # Class Logger:                            #
    ############################################
    def log(self, log_msg, log_type, log_id):
        """This class method provides the logging for this class. If the class caller
        instantiates the object with the verbose setting set to true, then the class 
        will log to stdout/stderr."""
        try:
            # Function variable assignments
            log_msg_caller = "{}.{}".format(self._log_context, log_id)
            # Set the message type offset, debug=3, info=4, warning=1, error=3
            log_msg_offset = 3
            log_msg_offset = 4 if log_type.lower() == 'info' else log_msg_offset
            log_msg_offset = 1 if log_type.lower() == 'warning' else log_msg_offset

            # Push the log to either the provided log or to stdout/stderr
            if self._log is not None:
                # Set the log message prefix
                log_message = "{}:   {}".format(log_msg_caller, log_msg)
                if log_type.lower() == 'error':
                    self._log.error(log_message)
                elif log_type.lower() == 'warning':
                    self._log.warning(log_message)
                elif log_type.lower() == 'info':
                    self._log.info(log_message)
                else:
                    self._log.debug(log_message)
            else:
                log_message = "{}{}{}:   {}".format(log_type.upper(), " " * log_msg_offset, log_msg_caller, log_msg)
                if log_type.lower() == 'error':
                    if self.verbose:
                        print(log_message, file=sys.stderr)
                else:
                    if self.verbose:
                        print(log_message, file=sys.stdout)
        except Exception as e:
            self._exception_handler('log', e)


    ############################################
    # Class Exception Handler:                 #
    ############################################
    def _exception_handler(self, caller_id, exception_object):
        """This class is constructed to handle any exceptions if an occurrance arises"""
        parse_exc_msg = "An Exception occurred during method {} exectution: {} in line: {}".format(
                caller_id,
                str(exception_object),
                sys.exc_info()[2].tb_lineno
            )
        self.log(parse_exc_msg, 'error', caller_id)


    ############################################
    # Jinja Option Getters and Setters:        #
    ############################################
    @property
    def trim_blocks(self):
        """Class Getter method for Jinja trim_blocks property. This method returns the current trim_blocks setting value."""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to retrieve trim_blocks setting: {}".format(self._trim_blocks), 'info', self.__id)
        return self._trim_blocks


    @trim_blocks.setter
    def trim_blocks(self, trim_blocks_setting=True):
        """Class Setter method for Jinja trim_blocks property. This method will only take a value of true or false as a valid value for the property."""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to set trim_blocks setting: {}".format(trim_blocks_setting), 'info', self.__id)
        # if the passed value is a valid bool value then set the value.
        if isinstance(trim_blocks_setting, bool):
            self._trim_blocks = trim_blocks_setting
            self.log("Successfully updated trim_blocks: {}".format(self._trim_blocks), 'debug', self.__id)
        else:
            self.log("Invalid type specified for trim_blocks.Expected bool but received {}".format(type(trim_blocks_setting)), 'warning', self.__id)


    @property
    def lstrip_blocks(self):
        """Class Getter method for Jinja lstrip_blocks property. This method returns the current lstrip_blocks setting value."""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to retrieve lstrip_blocks setting: {}".format(self._lstrip_blocks), 'info', self.__id)
        return self._lstrip_blocks


    @lstrip_blocks.setter
    def lstrip_blocks(self, lstrip_blocks_setting=True):
        """Class Setter method for Jinja lstrip_blocks property. This method will only take a value of true or false as a valid value for the property."""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to set lstrip_blocks setting: {}".format(lstrip_blocks_setting), 'info', self.__id)
        # if the passed value is a valid bool value then set the value.
        if isinstance(trim_blocks_setting, bool):
            self._lstrip_blocks = lstrip_blocks_setting
            self.log("Successfully updated lstrip_blocks: {}".format(self._lstrip_blocks), 'debug', self.__id)
        else:
            self.log("Invalid type specified for lstrip_blocks. Expected bool but received {}".format(type(lstrip_blocks_setting)), 'warning', self.__id)


    ############################################
    # Jinja Template Directory Getter/Setter:  #
    ############################################
    @property
    def template_directory(self):
        """This class Getter method will retreive the currently set value of the template directory and return
        it back to the method caller."""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to retrieve template_directory: {}".format(self._template_directory), 'info', self.__id)
        if self._template_directory is None:
            return "No setting found!. Set this property with object.template_directory = 'valid/path/to/template/directory'."
        else:
            return self._template_directory


    @property
    def available_templates(self):
        """Class property method that will return the self._available_templates property. The available_templates property is a list of all templates available in the configured template_directory. The template_directory setter method constructs the list of template files when a template_directory is updated."""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to retrieve available_templates", 'info', self.__id)
        if self._available_templates is not None and isinstance(self._available_templates, list):
            return self._available_templates
        else:
            return []


    @template_directory.setter
    def template_directory(self, template_directory_path):
        """Class Setter method that will take a valid directory path location and use that location to set the object
        template_directory property. Once validated this method will call the load method to load the template directory
        and populate the available_templates list property."""
        # Check the input value for validity, then set.
        try:
            # Define this method for functional logging
            self.__id = inspect.stack()[0][3]
            self.log("Call to set template_directory to path: {}".format(template_directory_path), 'info', self.__id)
            
            if template_directory_path is not None, and isinstance(template_directory_path, str):
                if os.path.exists(template_directory_path):
                    # Set the template_directory property.
                    self._template_directory = template_directory_path
                    self.log("Template directory path set to: {}".format(self._template_directory), 'debug', self.__id)
                    # Get a list of templates in the provided directory and set the file list property
                    template_list = [f for f in os.listdir(self._template_directory) if isfile(join(self._template_directory, f))]
                    if isinstance(template_list, list) and len(template_list) > 0:
                        for item in template_list:
                        self._available_templates = template_list
                        self.log("Availabe templates property to: {}".format(self.template_list), 'debug', self.__id)
                    try:
                        # Load the templates into Jinja
                        self._jinja_loader = FileSystemLoader(self._template_directory)
                        self._jinja_template_library = Environment(
                            loader=self._jinja_loader,
                            trim_blocks=self._trim_blocks,
                            lstrip_blocks=self._lstrip_blocks
                        )
                        self._jinja_template_library.filters['to_json'] = json.dumps
                        self.log("Jinja loaded the provided template_directory successfully!", 'debug', self.__id)
                        self.log("Added to_json filter to Jinja Environment object.", 'debug', self.__id)
                    except Exception as e:
                        self._exception_handler(self.__id, e)
                else:
                    self.log("Provided directory path doesn't exit.", 'error', self.__id)
                    self.log("Aborting property update...", 'error', self.__id)
            else:
                self.log("Provided directory path expected type str but received: {}".format(type(template_directory_path)), 'error', self.__id)
                self.log("Aborting property update...", 'error', self.__id)
        except Exception as e:
            self._exception_handler(self.__id, e)

    
    ############################################
    # Jinja Template Getter/Setter:            #
    ############################################
    @property
    def load(self):
        """Class Getter Method that returns the value of self._loaded_template back to the caller"""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to retrieve loaded template from Jinja Environment", 'info', self.__id)

        if self._loaded_template is not None:
            return self._loaded_template
        else:
            return "No template has been loaded!"

    @load.setter
    def load(self, template):
        """Class method to load the specified template. The template can be:
        
        * The name of a template already loaded in the jinja_loader from a template_directory
        * A file path to a valid jinja file on the filesystem
        """
        try:
            # Define this method for functional logging
            self.__id = inspect.stack()[0][3]
            self.log("Call to load template: {}".format(template), 'info', self.__id)
            
            # Check the value passed to determine what type of template was passed.
            if os.path.isfile(template):
                self._loaded_template = self._jinja_template_library.get_template(template)
                self.log("Loaded template file from path: {}".format(self._loaded_template), 'info', self.__id)
            else:
                self._loaded_template = self._jinja_template_library.get_template(template)
                self.log("Loaded template file from template_directory: {}".format(self._loaded_template), 'info', self.__id)
        except Exception as e:
            self.log("Attempt to load template file failed!", 'error', self.__id)
            self._exception_handler(self.__id, e)


    @property
    def render(self):
        """Class method that will return the current rendered template from the current loaded template."""
        # Define this method for functional logging
        self.__id = inspect.stack()[0][3]
        self.log("Call to retrieve rendered template from Jinja Environment", 'info', self.__id)

        if self._rendered_template is not None:
            return self._rendered_template
        else:
            return "No template has been rendered!"


    @render.setter
    def render(self, **kwargs):
        """Class method that will render the template loaded in the objects self._loaded_template property.
        This method will accept multiple dictionary objects as an input provided that they were provided
        in the format of keyword = dictionary where keyword is the variable in the Jinja template that will
        map to the dictionary object being passed.
        """
        try:
            # Define this method for functional logging
            self.__id = inspect.stack()[0][3]
            self.log("Call to render loaded template: {}".format(self._loaded_template), 'info', self.__id)
            
            # Render the template passing in the kwargs input.
            self._rendered_template = self._loaded_template.render(**kwargs)
            self.log("{} rendered successfully!".format(self._loaded_template), 'info', self.__id)
        except Exception as e:
            self.log("Attempt to render loaded template failed!", 'error', self.__id)
            self._exception_handler(self.__id, e)

    
    def write(self, output_directory, output_file, overwrite=False, Backup=True):
        """Class method that will write the rendered jinja template to a directory/path location."""
        try:
            # Define this method for functional logging
            self.__id = inspect.stack()[0][3]
            self.log("Call to write rendered template to: {}".format(os.path.join(output_directory, output_file)), 'info', self.__id)
            
            # Write the rendered template to disk.
            if output_directory is None or output_file is None:
                self.log("No output directory or file was specified!")
                return False
            if os.path.exists(output_directory):
                <<<<<<<-----HERE----------->>>>>
                # Check if file exists, if it does, backup if backup true, check overwrite, fail if overwrite false
                # Write the things!
            else:
                self.log("The provided output directory is not a valid path", "error", self.__id)
                return False





            self._rendered_template = self._loaded_template.render(**kwargs)
            self.log("{} rendered successfully!".format(self._loaded_template), 'info', self.__id)
        except Exception as e:
            self.log("Attempt to render loaded template failed!", 'error', self.__id)
            self._exception_handler(self.__id, e)









# <<<<<<<<-------HERE-------------->>>>>>> LOAD TEMPLATE, OR LOAD CUSTOM TEMPLATE AS VARIABLE. 
# NEEDED:
#   - load
#   - render
#   - write

