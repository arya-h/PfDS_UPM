# PfDS_UPM

To run the code use python version 3.9 with the libraries found in the "requirements.txt" installed.

Before running add the Gecko driver suitable for your machine from: https://github.com/mozilla/geckodriver/releases

File and folder overview:

MakeFile, A file to run all the .py files at once.\
analysis.py, Code to create the graphs used for the analysis.\
data_scraper.py, Code to scrape the data and write it to CSVs.\
portfolio_allocations.py, Code to create all possible combinations of portfolios.\
portfolio_metrics.py, Code to process the data and calculate return and volatility.\
requirements.txt, Text file with the required libraries needed to run the code.\
analysis_plots*, folder with the plots created for the analysis.\
data*, folder with the data scrapped saved in CSVs.\
portfolios*, folder with CSVs including the allocated portfolios and the portfolios with the calculated metrics.\

* folders are created and filled when running the code.
