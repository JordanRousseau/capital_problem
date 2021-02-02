# Capital Problem

Compare two climate datasets to find the european capital for which temperatures are provided in the file `Climate.xlsx`.
We will use the file `Savukoskikirkonkyla.xlsx` from open data as a reference.

Many steps were developed on this project

### Step 1: Climate SI Sheet summary.

First one was to establish a mean, a standard deviation and identify Maximum and Minimum in temperature data.
We used the library numpy functions to do those different calculations

### Step 2: Climate SI Sheet Graphs.
The second One was to do Two different graphs:
 - A monthly graph, to watch the temperature evolution for all months
 - An annual graph, to watch the temperature evolution on the year

To do that, we used the library Dash, made to made interfaces and host a local web server. This library includes Plotly, a perfect solution for graph generation. 
We modified the dataframe, the goal was to get a dataframe where each row will represent a date and a temperature. So we used the pandas melt function. It allowed us to create the day, month and Temperature columns.
Then we aggregated the date in a full-date. So we could use it in a graph.

### Step 3 : Setup a 30 days zoom.
We made the mentioned graphs, and thanks to the Dash callbacks we setup a special zoom on annual graphs. We zoomed on a selected point and the 15 days before and after that date.

### Step 4: Same ways on SI-Erreur sheet.
And we did the same process on SI-erreur spreadsheet.

### Step 5: Fix the SI-Erreur wrong values.

But, we had to clean the differents errors values as "0xFFFF" or "sun" which are incorrect temperature.
To achieve this goal, we used the method to_numeric from panda library. This method allowed us to convert each temperature value in a numeric one, and the non-numeric are automatically convert in NaN (Not a number). Then we could use a magic function from panda `interpolate`. Which fill the NaN values with a new calculated value coinciding with the previous and next values. We did used the base mode (Linear), because we didn't need a complex calculated value as temperature vary by a few degrees.

Some values were still strange, as 48 degrees the day before and the day after were 15 degrees.
Its one of the Outliers we saw. To fix them, there are few methods we can use. We simply Checked if the Temperature difference, between the month and the current temperature was more than the threshold we fixed. We fixed it at 10 degrees for the moment.
We're not expert in climate analysis, but we fought it was a too high difference to consider it as a true value.

### Step 6 : Determine the climate of the SI / SI-Erreur sheets.
Next step was to determine the climate in comparison with Savukoski kirkonliya's climate data.
We did an algorithm to do dynamic time wrapping(dtw). It's a good solution when we need to measure similarities between two temporal sequences. 

First of all we did the comparision between SI and SI-Erreur sheets to get a reference. We determine a dtw score of aproximatively, `4,5`. That proves the dtw is accurate, we got some differences on some values between both sheets. We can as well control it throught the comparision graphs.

The second things we did was to make this dtw indicator on Savukoski kirkonliya's data. We got approximatively a dtw score of 147,6. Which is a small score, we made a graph to check the evolution of the Differents curve (SI, SI-erreur and Savukoski), so we were able to see the curves were similar but many temperatures are different the same days, nevertheless it is only a few degrees. So we could establish that the SI data came from a `cold climate` country, as Scandinavian countries or Russia.

### Step 7: Compare with European capitals, and find the best candidate.

Then to prove our feelings and thoughts, we tried to do the same process with different cities in Europe to determinate the best candidate. 
We found a dataset on [Kaggle](https://www.kaggle.com/sudalairajkumar/daily-temperature-of-major-cities) which was containing many cities temperature over many years.

First of all we filter the data on the columns we needed, City, Temperature, Year, Month and Day. Then we only selected data on the Year 2018 and Some Cities we chose (capitals in Europe).

Then we could do the same process as before. We calculated, in an automated way, the dtw score for every Cities, and establish the graphs.

So we could determine the closest dtw score was Moscow with approximatively 99. Followed by Oslo, Riga, Helsinki and Stockholm. (We took the cities with maximum 20 score more)

DTW results: 
- Moscow: 99
- Oslo: 104
- Riga: 109
- Helsinki: 111
- Stockholm: 115 

`Moscow` is the best candidate with dtw but the results are really close and we should confirm this assumption, with another method as calculating the area between curves or using PCM (Partial Curve Mapping).

When using PCM method we found that `Moscow` had a much Higher score than `Helsinki` or `Stockholm`(Moscow: 0,66 , Helsinki: 0,41). 

PCM results : 
- Riga: 0,62
- Oslo: 0,68 
- Helsinki: 0,41
- Moscow: 0,66
- Stockholm: 0,37

It can therefore be concluded that the most likely European capital for the origin of climate data is one of the following cities: `Helsinki`, `Oslo`, `Riga`, `Stockholm` or `Moscow`. Based on the equilibrium of Dtw and the PCM and PCM `Helsinki` and `Stockholm` are the best candidates.

When doing standard deviation differences between city and SI sheet, Helsinki is the lowest score.

STD difference score: 
- Helsinki: 0,11 
- Oslo: 0,12

`Helsinki` and `Oslo` seems to be good candidates to be the capital when analysing STD differences

Finally with these score (DTW, PCM and STD) we mapped them between 0 and 1 and we did the sum. 
0 is the basis curve and 3 is the worst curve possible. 
By doing that we assure a correlation between our different calculations, to get the best result possible (the lower one). Area under curve and frechet distance were skipped of this calculation because there redundant with DTW and PCM.

According to this different tests, we can guess that `Helsinki` is probably the origin of the climate data with a score of 0,41.

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
   python setup.py install
   ```

   or:

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

   You need to set a file `.env` with secrets and variables of the project at his root _(`invoice process\`)_. Here is the OSX and linux sample:

   ```sh
   # files path
   CLIMATE_PATH = .data/Climat.xlsx
   REFERENCE_CLIMATE_PATH = .data/Savukoski kirkonkyla.xlsx
   ```
7. **Set up the files**
   
   Put the Climate and Savukoski xlsx files in a .data directory in the root directory.

   And add in the same directory the csv file from [Kaggle](https://www.kaggle.com/sudalairajkumar/daily-temperature-of-major-cities)

8. **Running the app**
   ```sh
   python src/capital_problem/core.py
   ``` 
## Running the tests

You can run the tests with the command:

```sh
python setup.py test
```

## Generate Documentation

Generate documentation with the command:

```sh
python setup.py docs
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
