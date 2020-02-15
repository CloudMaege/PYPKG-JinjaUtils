# CloudMage JinjaUtils Python3 Utility Package

<br>

![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/cloudmage/cloudmage-glow-banner.png)

<br>

![PyTests](https://github.com/TheCloudMage/PyPkgs-JinjaUtils/workflows/PyTests/badge.svg)

<br><br>

## Table of Contents

* [Description](#description)
* [Road Map](#road-map)
* [Python Version Support](#python-version-support)
* [Package Dependencies](#package-dependencies)
* [JinjaUtils Class](#jinjautils-class)
  * [JinjaUtils Object Arguments](#jinjautils-object-arguments)
  * [JinjaUtils Property Methods](#jinjautils-property-methods)
  * [JinjaUtils Properties](#jinjautils-properties)
  * [JinjaUtils Class Usage](#jinjautils-class-usage)
* [ChangeLog](#changelog)
* [Contacts and Contributions](#contacts-and-contributions)

<br><br>

## Description

This utility package was created to allow quick and easy access method to work with Jinja templates within a python environment. The package will give access to a class that can be imported and instantiated, creating a JinjaHelper instance that will allow the consumer the ability to quickly and easily set jinja options via object properties, load templates including custom templates, render those templates and write the template output to the configured output directory/file.

<br><br>

## Road Map

Beyond the initial capabilities of this library, new features will be evaluated and could be added with feature requests, or as additional processes that can be simplified are discovered.

<br><br>

## Python Version Support

This library is compatible with Python 3.6 and higher. It may work with earlier versions of Python3 but was not tested against anything earlier then 3.6. As Python 2.x is soon to be end of life, backward compatibility was not taken into consideration.

<br><br>

## Package Installation

This library has been published to [PyPi](https://pypi.org/project/cloudmage-jinjautils/) and can be installed via normal python package manager conventions such as [pip](https://pip.pypa.io/en/stable/) or [poetry](https://pypi.org/project/poetry/).

<br>

```python
pip3 install cloudmage-jinjautils
```

<br><br>










## Package Dependencies

This package installs and imports the following python modules during installation:

* requests

<br>

Additionally the package takes advantage of the following built in python modules:

* os
* sys
* json
* inspect

<br><br>

## JinjaUtils Class

The JinjaUtils class has the following described methods, properties and attributes accessable to it upon object instantiation. Object constructor arguments must be provided at the time that the object is instantiated. Object Get methods are accessed from the object in standard dot notation `Jinja.verbose, Jinja.template_directory, etc.` and Object Set methods are used by assigning a value to the object property `Jinja.template_directory = '/path/to/templates`. The class gives the object instance access to the following properties:

<br>

### JinjaUtils Object Constructor Arguments

-----

* `verbose`: Enables or disables verbose mode
  * `arg type`: bool
  * `optional argument`
  * `default value`: False (Disabled)
* `log`: Redirects standard class log messages to a provided log object.
  * `arg type`: object
  * `optional argument`
  * `default value`: None (Writes debug, info, and warnings to stdout, errors to stderr)

<br>

### JinjaUtils Property Set Methods

-----

* `trim_blocks = [bool]`: Enables or disables the Jinja trim_blocks setting used when loading template.
  * `expected value type`: `bool`
  * `default value`: `True`
  * Property must be set with a valid bool type argument.
* `lstrip_blocks = [bool]`: Enables or disables the Jinja lstrip_blocks setting used when loading template.
  * `expected value type`: `bool`
  * `default`: `True`
  * Property must be set with a valid bool type argument.
* `template_directory = [/jinja/templates]`: Sets the directory path where jinja templates are loaded from within the object.
  * `expected value type`: `str`
  * Must be valid directory path, checked with `os.path.exists()`
* `load = [/jinja/template | my_template.j2]`: Instructs the Jinja object environment loader to load the provided template.
  * `expected value type`: `str`
  * Value can be 1 of file path or file name.
  * If a valid file path is provided, then the provided file will be loaded into the Jinja object environment.
  * If a valid template file name is provided, the Jinja Environment will attempt to load the referenced template from the template_directory.

<br>

### JinjaUtils Property Get Methods

-----

* `trim_blocks`: Returns current object trim_blocks setting.
  * `return type`: bool
* `lstrip_blocks`: Returns current object lstrip_blocks setting.
  * `return type`: bool
* `template_directory`: Returns the currently set object template directory.
  * `type`: str
* `available_templates`: Returns list of files found in the configured template_directory. Value set when template_directory is configured.
  * `return type`: list(files)
* `load`: Returns the template loaded in the Jinja object environment.
  * `return type`: Loaded Jinja Template.
* `render`: Returns the template rendered from the Jinja object environment.
  * `return type`: Rendered Jinja Template.

<br>

### JinjaUtils Class Methods

-----

* `render(**kwargs)`: Instructs the Jinja object environment to render the loaded template passing the kwargs tuple.
  * `expected value type`: `tuple` of keyword=value arguments.
  * When the kwargs is unpacked, it will be in the form of key=value
  * `key` should be the variable or object that the loaded template will be looking for
  * `value` should contain the variable type that the loaded template will be looking for.
  * `example`: `Jinja.render(var1={'key': 'value'}, var2=['1', '2'], var3="John Smith")`

<br><br>

### JinjaUtils Class Usage

-----












```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Verbose Class Constructor Argument:__](Note) <br> When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.

<br>

```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Log Object:__](Note) <br> When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels (`log.debug()`, `log.info()`, `log.warning()`, `log.error()`) and printed to the passed respective logger object method.

<br>

```python
from cloudmage-gitutils import GitConfigParser

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True, log=GitLog)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

for items in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br><br>

## GitHubAPI Class

This class takes a git repository URL as input, and then uses that input to construct and send a request to the github api for the targeted repository /repos endpoint. When a response is received and tested for validity, the JSON formatted response object is stored in the .data property, and used to populate the other class object properties listed below.

<br>

### GitHubAPI Object Arguments

-----

* `repo_url`: The https or git formatted URL string of the target git repository
* `auth_token`: Optional git provider authentication token to be set in the API request headers to authenticate the API request.
* `verbose`: Optionally enable verbose class logging
* `log`: Optionally provide log object as argument, and all class logging will be re-routed to the logger object.

<br><br>

### GitHubAPI Object Properties

-----

* `verbose`: Verbose bool value that can be optionally passed to the class constructor
__Github Properties:__
* `name`: The name of the targeted Git Repository (derived from provided URL string)
* `namespace`: The namespace under which the repository is owned (derived from provided URL string)
* `id`: The repositories Github id
* `access`: Set to either `public` or `private` based on the github repository type
* `http_url`: The HTTPS url of the repository
* `git_url`: The GIT url of the repository
* `mirror`: Repository configured mirror (If configured)
* `description`: The repository description
* `created`: The repository creation date
* `updated`: The date the repository was last updated
* `last_push`: The the date of the last push to the repository
* `size`: The repository size
* `language`: The repository language
* `license`: The repository license
* `archived`: True or False depending on if the repository has been archived
* `disabled`: True or False depending on if the repository has been disabled
* `default_branch`: The repositories default branch, typically `master`
* `fork`: Indicator as to if the repository is a fork of another repository
* `forks`: Number of forks from the repository
* `watchers`: Number of repository watchers
* `stars`: Number of stars on the repository
* `issues`: Indicates if the repository has an issues section
* `open_issues`: Number of open issues in the repositories
* `homepage`: Value of repository homepage if configured
* `wiki`: Indicates if the repository has a wiki
* `pages`: Indicates if the repository has pages enabled
* `downloads`: Indicates if the repository has downloads enabled
* `projects`: Indicates if the repository has projects enabled.
* `owner`: Object containing owner attributes
  * `owner.id`: The github id of the repository owner
  * `owner.name`: The name of the repository owner (github username)
  * `owner.avatar`: The url of the repository owners avatar
  * `owner.url`: The github url for the repository user profile
* `state`: The state of the API request. Either `Success` or `Fail`
* `data`: A dictionary containing the original github JSON response object
* `log`: The class logger. It will either write directly to stdout, stderr, or to a lob object if one was passed into the object constructor.

<br><br>

### GitHubAPI Class Usage

-----

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Passing an Authentication Token:__](Note) <br> When instantiating the class, an option `auth_token` argument can be provided. The argument is a valid auth token issued from the platform provider. If provided, the auth_token will be passed to the request handler method, where the method will construct request headers including the authentication token for authenticated requests to private repositories.

<br>

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Verbose Class Constructor Argument:__](Note) <br> When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.repositories.

<br>

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL, verbose=True)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br><br>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Log Object:__](Note) <br> When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels (`log.debug()`, `log.info()`, `log.warning()`, `log.error()`) and printed to the passed respective logger object method.

<br>

```python
from cloudmage-gitutils import GitHubAPI

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL, verbose=True, log=GitLog)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}

for items in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br><br>

## Changelog

To view the project changelog see: [ChangeLog:](CHANGELOG.md)

<br><br>

## ![TheCloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/cloudmage/cloudmage-profile.png) &nbsp;&nbsp;Contacts and Contributions

This project is owned and maintained by: [@rnason](https://github.com/rnason)

<br>

To contribute, please:

* Fork the project
* Create a local branch
* Submit Changes
* Create A Pull Request
