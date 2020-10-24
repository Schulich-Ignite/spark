# spark
Jupyter Lab ipython extension used for teaching the [Schulich Ignite sessions](https://schulichignite.com/).

### Documentation
Simple documentation for the library is provided in the [documentation.ipynb](https://github.com/Schulich-Ignite/spark/blob/main/documentation.ipynb) file.

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