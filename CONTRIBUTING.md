# Development Documentation

*This file contains everything you should need to get started developing*

## Table of contents

- [Setting up a local dev environment](#setting-up-a-local-dev-environment)
- [File structure breakdown](#file-structure-breakdown)
- [Contributing to docs](#contributing-to-docs)
  - [Prerequisites](#prerequisites)
  - [Previewing updates](#preview-updates)
  - [Docs site config](#docs-site-config) 
- [Preview updates](#preview-updates)
- [Contributing to API](#contributing-to-api)
  - [Prerequisite knowledge](#prerequisite-knowledge)
  - [Utility Decorators](#utility-decorators)
      - [@validate_args](#validate_args)
      - [@ignite_global](#ignite_global)
      - [@extern](#extern)
  - [Writing Tests](#writing-tests)
  - [Vendoring Functions](#vendoring-functions)
  - [Creating New Functions](#creating-new-functions)
      - [Making User Definable Functions](#making-user-definable-functions)
- [CI/CD pipeline details](#cicd-pipeline-details)
- [Release steps](#release-steps)
- [Glossary](#glossary)

## Setting up a local dev environment

Follow the instructions in the [Installation script repository](https://github.com/Schulich-Ignite/installation-script) they will be the most up to date. You can also download a binary installer from the [releases page](https://github.com/Schulich-Ignite/installation-script/releases) of that repo (if available).

## File structure breakdown

Below is a simple breakdown of the current file structure, the format is ```[file or folder emoji] name - description```. 

```
├── 📁 .github - All files related to github specific features (actions, pull request templates etc.)
│   └── 📁 workflows - All CI/CD pipeline files
├── 📁 docs - Source markdown for docs site
│   └── 📁 img - All images used in docs site
├── 📁 spark - All source code for spark functionality
│   ├── 📁 util - Contains utility functions like decorators, errors etc.
│   └── 📄 core.py - Primary logic invoked when package is called in jupyter
├── 📁 test - All automated test files
├── 📝 CONTRIBUTING.md - File containing development docs (this file)
├── 📝 CONTRIBUTORS.md - File containing list of developers
├── 📄 mkdocs.yml - Config for the docs site static site generator
└── 📄 setup.py - Config for pypi deployment and package installation maifest
```

*Note only important development files are mentioned here, extranious metadata files like ```.gitignore``` and ```LISCENSE``` are ignored.*

## Contributing to docs

Contributing to the documentation is very simple, all the documentation files are in the ```/docs``` folder. They are just simple markdown files that can be edited with a text editor.

### Prerequisites

- Knowledge of [markdown syntax](https://guides.github.com/features/mastering-markdown/)
- Python 3.8 + installed
- mkdocs; ```pip install mkdocs```
- mkdocs material theme; ```pip install mkdocs-material```

### Preview updates

To preview updates run ```mkdocs serve``` in the root directory (where ```mkdocs.yml``` is), and then go to [https://localhost:8000](https://localhost:8000) in your browser. The preview features livereload so you can make changes and then save the file and see it automatically reload in browser with the new changes.

### Docs site config

All the configuration for the documentation site is stored in ```mkdocs.yml```, the site is hosted in the git repo under the gh-pages branch and is automatically built on every push to the main branch by the [docs pipeline](#docs-pipeline).

## Contributing to API

Below are details about contributing the the spark api (the actual code that runs when you import the module).

### Prerequisite knowledge

Below is a list of highly recommended topics to read up on before diving into the codebase. Many of the techniques employed are somewhat complicated, but if you have a base of knowledge about the following you should be able to start:

**Python knowledge**
- Basic python syntax
- A good understanding of scope
- Basic data structures (ints, floats, str, collections etc.)
- [Classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes)
- [Decorators](https://www.datacamp.com/community/tutorials/decorators-python)
- Modules (how to create, and work with internal & external modules)
- [Unpacking](https://www.geeksforgeeks.org/packing-and-unpacking-arguments-in-python/) (*args, **kwargs)

If any of the above topics are fuzzy, it's a good idea to research them first. Additionally if you haven't worked with python before I would recommend completing [the course on w3schools](https://www.w3schools.com/python/default.asp) and [this youtube course](https://www.youtube.com/watch?v=HGOBQPFzWKo)

**Jupyter Knowledge**

- An understanding of how to use jupyter notebooks (you need to test somehow)

**Other nice to haves**:

- Experience with web development; this is handy because jupyter is essentially python baked into a browser, so some vendor code (like ipyevents) interacts with the browser directly. 


### Utility Decorators

In the spark library there are several utility decorators that exist to simplify development

#### @validate_args

This decorator is used to validate both the number of arguments, as well as the types of the arguments.

```python
validate_args(*fmts, has_self=True)
```

**Parameters**

- \*fmts (list); an arbitrary number of positional lists of types the function can accept
- has_self (bool); Whether a function has a self argument (a method of a class), defaults to True

For example let's imaging a function called ```foo()``` that has two arguments that **must** be integers, and the function is not part of a class. We would define ```foo()``` like so:
```python
from util.decorators import validate_args

# Allows for foo(int) and specifies not part of a class
@validate_args([int], has_self=False) 
def foo(*args):
    ... # Do stuff
```

Now lets imagine we have another function ```bar()``` that can **either** take in two ints, or one string, and is a method of a class:
```python
from util.decorators import validate_args

class foo:
    ... # Other code in the class

    # allows for foo(int, int) or foo(str), and that function is a method in a class implicitly
    @validate_args([int, int], [str]) 
    def bar(self, *args):
        ... # Do stuff
```


#### @ignite_global

Specifies a function should be added to the global namespace (able to call directly inside a cell)

```python
ignite_global(_func=None, *, mutable=False)
```

**Parameters**

- _func (); 
- \*; this is a python addage that allows for an arbitrary number of parameters to be passed along
- mutable (bool); Whether a function is a user defined function (like ```setup()```), or an imutable function (like ```rect()```), defaults to False (function is imutable)

**Notes**
- 99% of the time you will want to use this with [validate_args()](#validate_args)

**Examples**

Creating a function called ```foo()``` that is imutable, and takes 2 Real numbers (ints or floats) as arguments:

```python
from numbers import Real # A type that means int or float
from util.decorators import validate_args, ignite_global

# Allows for foo(Real, Real) and specifies not part of a class
@validate_args([Real, Real], has_self=False) 
@ignite_global # Set function to be global and immutable
def foo(*args):
    ... # Do stuff
```

creating a function called ```bar()``` that is user definable:

```python
from util.decorators import ignite_global

@ignite_global(mutable=True)
def bar():
    ... # This will be ignored
```

#### @extern

Extern primarily exists to make the accessing of globally scoped functions easier. If you define a function with [@ignite_global](#ignite_global) in a file outside of ```core.py```, you will also need to add it to the ```core.py``` file in the ```Core``` object and decorate it with ```@extern```. 

For example, let's say we have a function we want to add called ```foo()``` that takes in 2 floats or ints. We define the logic in a file called ```/util/helper_functions/bar.py```, and it is defined as:

```python
from numbers import Real # A type that means int or float
from util.decorators import validate_args, ignite_global

# Allows for foo(Real, Real) and specifies not part of a class
@validate_args([Real, Real]) 
@ignite_global # Set function to be global and immutable
def helper_foo(self, *args):
    ... # Do stuff
```

Now in ```core.py``` we add:

```python
class Core:
    ... # other class code
    @extern
    def foo(self, *args): pass
```

The ```foo()``` method is overridden at runtime with the ```util.helper_functions.bar.helper_foo``` code, and added to the global scope.


### Writing Tests

*TODO: Waiting on testing methodology to populate*

### Vendoring Functions

To vendor any functions you will need to do the following steps:

1. Decorate the function with the ```util.decorators.validate_args``` function (typically imported in existing files)
2. Decorate the function with the ```util.decorators.ignite_global``` function (typically imported in existing files)
3. Name the function with ```helper_function_name```

So for example to vendor [randint](https://docs.python.org/3/library/random.html#random.randint) from the [random](https://docs.python.org/3/library/random.html) module you would do:

```python
import random
from util.decorators import validate_args, ignite_global

@validate_args([int])
@ignite_global
def helper_randint(self, *args):
    return random.randint(0, args[0])
```

### Creating New Functions

For any new functions create the function in a file in ```/helper_functions``` or ```/util```. Avoid adding things to ```core.py``` unless necessary. If you are adding new functions that you want to be globally available please see [Utility Decorators](#utility-decorators) for details of the necessary decorators. 

But let's look at a basic example of adding a ```rect()``` function that takes 4 real numbers as arguments:

1. Add the logic to a function that follows the pattern ```helper_<func_name>()``` to one of the files in ```/util/helper_functions```. In our case we will add ```helper_rect()``` to ```/util/helper_functions/rect_functions.py```:
```python
from ..decorators import *
from numbers import Real


@validate_args([Real, Real, Real, Real])
@ignite_global
def helper_rect(self, *args):
    self.canvas.fill_rect(*args)
    self.canvas.stroke_rect(*args)
```
2. Next we add the function name with an ```@extern``` signature to the Core object in ```core.py```:
```python
class Core:
    ... # Other class code
    @extern
    def rect(self, *args): pass
```

Now at runtime we will be able to do:

```python
%%ignite

def setup():
    size(500,500)
    rect(150.5, 150, 200.2, 200)
```

#### Making User Definable Functions

To create a user definable function you will need to use the ```@ignite_global()``` decorator. Usage details can be found [here](#ignite_global)

## CI/CD pipeline details

Below are the details for all the existing CI/CD pipelines in place. They are all implemented using github actions.

### Docs pipeline

The configuration file can be found under ```.github/workflows/docs.yml```. It triggers on any pushes to the main branch and has 2 steps:
1. Checkout the main branch
2. Deploy using [mhausenblas/mkdocs-deploy-gh-pages](https://github.com/mhausenblas/mkdocs-deploy-gh-pages)

### PyPi pipeline

The configuration file can be found under ```.github/workflows/main.yml```. It triggers on pushes to main and has 5 steps:
1. Checkout main
2. Setup a python environment
3. Install ```setuptools``` and ```wheel``` to the python environment
4. Build an source dist and a binary dist (with wheel)
5. Publish the package to PyPi under ```schulich-ignite``` using [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)

### Testing/validation pipeline

*TODO: Waiting on final implementation details for test suite, and coverage checks*

## Release steps

*TODO: Get details about release steps*

## Glossary

- Vendoring; Taking existing code and adding it to the project i.e. [randint](https://docs.python.org/3/library/random.html#random.randint) from the [random](https://docs.python.org/3/library/random.html) module works [natively](https://schulichignite.com/spark/utilities/#create-a-random-int) in spark
- Notebook; A notebook file in the context of spark, is any .ipynb file that is intended to be opened in jupyter lab
- Jupyter Lab; This is the platform that spark is **explicitly written for**, details can be found [here](https://jupyterlab.readthedocs.io/en/stable/)
- PyPi; the python package index, this is what allows spark to be installed using ```pip install schulich-ignite```
- CI/CD Pipeline; A series of automated tasks that are triggered by a certain event i.e. releases to [PyPi](https://pypi.org/project/schulich-ignite/) when a release is published, or the docs site updating itself on a push to main
- Unit Tests; A peice of code written to validate that a certain function operates as you would expect
- Automated tests; All the unit tests or [visual regression tests](https://medium.com/loftbr/visual-regression-testing-eb74050f3366) that are run automatically to validate the package is working as expected on updates
- API; Stands for application programming interface, in our case this is synonymous with a package it is what you would classify spark as
- Agile;
- Kanban;
- User definable functions; functions that are intentionally overwritten by whoever is using the library i.e. ```setup()``` and ```draw()```
