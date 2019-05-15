Scrapper.py is Python script which scraps data about flats to rent in Warsaw from http://www.gumtree.pl using beautifulsoup4.

Running the script (n is the number of sites which will be scrapped. By default it is set to 899):  
>>python3 scrapper.py n   

It creates flats_test.csv file in which scrapped data is stored.

In flats_analysis.ipynb you can find some plots and statistics about flats I collected using "scrapper.py". I have put on github csv file containing only selected columns.
