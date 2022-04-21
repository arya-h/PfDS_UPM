# PfDS_UPM

## Running the Code

### General Requirements

The webscraping is done using the Firefox browser. In order to successfully scrape the data, ensure that the latest Gecko driver suitable for your machine is downloaded from: https://github.com/mozilla/geckodriver/releases and ensure it can be found on your system path.

Create a new python enviornment version 3.9 and install the required packages with listed in "requirements.txt" file.

### Web Scraping
From the root directory of the project, run: 
- `python3 data_scraper.py`

### Data Generation 
From the root directory of the project, run: 
- `python3 portfolio_allocations.py`
- `python3 portfolio_metrics.py`

### Data Analysis
From the root directory of the project, run: 
- `python3 analysis.py`

## File and folder overview

- MakeFile, File to run all the .py files at once.
- analysis.py, Code to create the graphs used for the analysis for the data analysis part.
- data_scraper.py, Code to scrape the data and write it to CSVs for the web scraping part.
- portfolio_allocations.py, Code to create all possible combinations of portfolios for the data generation.
- portfolio_metrics.py, Code to process the data and calculate return and volatility for the data generation.
- requirements.txt, Text file with the required libraries needed to run the code.
- analysis_plots*, Folder with the plots created for the analysis.
- data*, Folder with the scrapped data saved as CSVs.
- portfolios*, Folder with CSVs including the allocated portfolios and the portfolios with the calculated metrics.
- report.pdf, File containing the interpretation of the graphs and analysis of data.

.* folders are created and filled when running the code.

