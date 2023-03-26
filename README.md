# COMPSCI 235 Repository for Assignment 3
Group Members: JCHU634

## Description

This repository contains an implementation of Assignment 3. 
It contains unit tests which can be run through pytest. 
It contains a Flask application which includes several units (Search Pages, List of all books, Book Viewing and Reviews)

## NOTE
The logout button only appears if the user is logged-in

## Python version

This Application was developped and tested in Python version 3.9.5


## Installation

**Installation via requirements.txt**

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm for requirements installation, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 


## Testing with the pytest unit tests

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call
```shell
python -m pytest test_folder
```
PyCharm also provides a built-in terminal, which uses the configured virtual environment. 


## Execution of the web application

**Running the Flask application**

From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Data sources 

The image is made by AlekseyP8 licensed via CC4
https://creativecommons.org/licenses/by-sa/4.0/deed.en

The data in the excerpt files were downloaded from (Comic & Graphic):
https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

We would like to acknowledge the authors of these papers for collecting the datasets by extracting them from Goodreads:

*Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.*

*Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19.*
