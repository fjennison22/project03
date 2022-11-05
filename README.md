# project03

Welcome to the GitHub repository for project03 for the class Computing for the Web. The instructions/grading rubric that I followed for this project can be found [here](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03).

The file titled `ebay.dl` is the main code that converts an eBay search query into either a `.json` or `.csv` file depending on your command line. Within the outputted file you will see the name of the item (`name`), the price of the item - represented in cents - (`price`), the status of the condition of the item (`status`), the price of shipping - also represented in cents - (`shipping`), a True or False value depending on whether or not the item has free returns (`free_returns`), and lastly, the number of sales of that item as an integer (`items_sold`).

To run `ebay.dl`, use the following command line:
```
$ python3 ebay-dl.py '*the name of the item you're searching for*'
```
If the item you're searching for contains multiple words (e.g 'baseball hat'), be sure to use quotation marks around it! By deafult, the program downloads the first 10 pages of the eBay search query.

By deafult, the program downloads the search queries in `.json` format. However, I inserted code that allows the user to download the results in `.csv` format. If you want the downloaded file to be a csv, add the command line flag `--csv`. The new command line would look like so:
```
$ python3 ebay-dl.py 'baseball hat' --csv
```
