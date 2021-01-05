# Capital Problem

Compare two climate datasets to find the european capital for wich tamperatures are provided in the file `Climate.xlsx`.
We will use the file `Savukoskikirkonkyla.xlsx` from open data as a reference.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them. The project run on Python 3.8.5 or above. You will use pip, pyScaffold and virtualenv.

1. **Check your 3.8.5 or above Python version**

   You can check your python version with the following command on windows:

   ```sh
   python --version
   ```

   _If the version is incorrect, use the [python wizard](https://www.python.org/downloads/windows/). If the problem persist, check the path environnement variable for python._

2. **Install pyScaffold**

   To create an isolated python environnement, we will use the tool virtualenv. Enter this command:

   ```sh
   pip3 install virtualenv
   ```

   If pip return an error and can't connect to the download servers, use this command to trust the servers:

   ```sh
   pip3 install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org virtualenv
   ```

### Installing

A step by step series of examples that tell you how to get a development env running. We will set the virtual environnement and the local environnement variables needed.

1. **Clone the project**

   Follow the instructions on how to clone the project on the [Repos page](https://github.com/SimonHuet/capital_problem) by clicking on the upper-right `⊻ Code` button.

2. **Create a virtual python environnement**

   Using the `virtualenv` tool, we will create a virtual python environnement inside the project. Type this command in the project root folder _(`invoice process\`)_:

   ```sh
   virtualenv .venv
   ```

3. **Activate the virtual environnement**

   To activate the virtual environnement in our command line interface, use the command:

   ```sh
   .venv\Scripts\activate.bat
   ```

   For Mac OSX users, please type `source .venv/bin/activate` instead.

   This will add `(.venv)` before the prompt:

   ```
   (.venv) projectpath>
   ```

   _You can quit this mode by using the command `.venv\Scripts\deactivate.bat` at any time. Use `deactivate` command on Mac OSX._

4. **Install the dependencies**

   We need to use environnement variables, we can achieve that with the package python-decouple that can read `.env` files. Autonomous documentation is achieve with Sphinx. To use the Google APIs, we need the Google python client. Install all the project dependencies in the virtual python environnement with:

   ```sh
   pip install -r requirements.txt
   ```

   If pip return an error and can't connect to the download servers, use this command to trust the servers:

   ```sh
   pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt
   ```

5. **Open the project in Visual Studio Code**

   Bravo 🥳! You have installed everything, it's time to open the ide and with a few steps you will be ready to dev. You can open VS Code with the command:

   ```sh
   code .
   ```

6. **Set up environnement variables**

   You need to set a file `.env` with secrets and variables of the project at his root _(`invoice process\`)_. Here is a blank sample:

   ```sh
   # empty
   ```

## Running the tests

You can run the tests with the command:

```sh
```

## Generate Documentation

Generate documentation with the command:

```sh
```

## Deployment

Add additional notes about how to deploy this on a live system

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [branches on this repository](https://github.com/SimonHuet/capital_problem/tags).

## Authors

- **Simon Huet** - _Engineer Developer_

- **Theo Levalet** - _Engineer Developer_

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SimonHuet/capital_problem/blob/main/LICENSE) file for details

## Acknowledgments
