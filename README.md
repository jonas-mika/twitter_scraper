# README: Twitter Scraper

## Description

This Repository was initially created to automate the webscraping process for the exam paper in the course DSiRBS in the first year of the Data Science course.
The Repository currently only contains code to scrape twitter data, but should be expanded to also scrape the web, instagram and other platforms.

## TODO

- [ ] Further implement Classes in Python Script
- [ ] Separate the twitter_scraper.py to make it more readable (maybe create a separate folder containing all those files)
- [ ] Implement Web Scraper
- [ ] Implement Instagram Scraper (might not be useful though, as it is more picture based)
- [ ] Think of other platforms to scrape

## To Run

For the scripts to work you need some libraries. most of them come pre-installed with python. the selenium library, which is primarily used for navigating the browser and scraping, needs to be installed, if it is not already:
In shell type:
'pip install selenium'

To Run the Scripts:
1. Jupyter Notebook (you need to install the jupyter package in order to work with .ipynb files): 
In Shell Type:
'jupyter notebook'
to start a temporary server to access the jupyter notebooks on your local machine. 

In the automatically opened webbrowser, navigate to where the '.ipynb' file is located and open it. You should now be able to work with the Notebook.

2. Script:
Navigate to the directory your '.py' is located and type:
'python twitter_scraper.py' *(ie. Twitter Scraper)*
to run the code. If you have all the necessary downloads, the code should work.

## Note!
Webscraping projects need high maintenance, since the script won't work, if changes are made to the structure of a website. If one of the scripts fails to work, please open an Issue or correct the code yourself and send a pull request. I will happily review your code and implement it, if I find it to be good.


Happy Scraping!
