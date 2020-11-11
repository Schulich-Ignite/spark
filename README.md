# spark
Jupyter Lab ipython extension used for teaching the [Schulich Ignite sessions](https://schulichignite.com/).

## Table of contents
- [Documentation](#documentation)
    - [Files](#files)
    - [Building](#building)
- [Testing locally](#testing-locally)

### Documentation
The [user documentation](https://schulichignite.com/spark/) is built using mkdocs. To build locally you will need to pip install:

- mkdocs
- mkdocs-material

Developer documentation can be found in [CONTRIBUTING.md](https://github.com/Schulich-Ignite/spark/blob/main/CONTRIBUTING.md).

#### Files

All the files are built in pure markdown and can be found in ```/docs```, the site configuration (including nav links) can be found in ```mkdocs.yml```.

#### Building

To build a local copy run ```mkdocs --serve``` and you will have a local copy available at [https://localhost/8000](http://localhost:8000/)

A release will build every time new code is pushed to the gh-pages branch, but can also be manually triggered via github actions pipelines

### Testing locally
Install NodeJS using one of the methods below:
- If on Windows, you can download binaries from [their website](https://nodejs.org/en/), or install using a package manager such as choco.
- If on Linux/Mac, run the following:

    ```shell
    sudo apt-get install nodejs
    ```

- Or if using Conda, run the following:

    ```shell
    conda install -c conda-forge nodejs
    ```

Next, you must install the required jupyter lab extensions
```shell
jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas ipyevents
```

Now, either clone the repo and install a development version, or install the up-to-date version from PyPI
```shell
# Cloning and installing this repo
git clone git@github.com:Schulich-Ignite/spark.git
pip install -e spark

# Or, install latest version from PyPI
pip install --upgrade schulich-ignite
```

Finally, you can open JupyterLab and navigate to the test folder, and run any of the ipynb files.