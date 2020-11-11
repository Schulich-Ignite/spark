import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="schulich-ignite",
    version="0.1.0",
    author="Schulich Ignite",
    author_email="info@shulichignite.com",
    description="Spark library for Shulich Ignite sessions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Schulich-Ignite/spark",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: IPython",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'ipywidgets',
        'ipycanvas',
        'ipyevents'
    ]
)
