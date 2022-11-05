import argparse
import requests
from bs4 import BeautifulSoup
import csv
import json

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.
    
    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers=''
    for char in text:
        if char in '1234567890':
            numbers+=char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_price(text):
    '''
    >>>parse_price('$50.01')
    5001
    >>>parse_price('See price')

    >>>parse_price('$0.99 to $79.86')
    99
    '''
    price=''
    if text[0]=='$':
        for p in text:
            if p in '1234567890':
                price+=p
            elif p=='':
                break
        return int(price)
    else:
        return None

def parse_shipping(text):
   
    '''
    >>> parse_shipping('Free shipping')
    0
    >>> parse_shipping('+$10.60 shipping')
    1060
    >>> parse_shipping('+$5.99 shipping')
    599
    '''
    price=''
    if text[0]=='+':
        for p in text:
            if p in '1234567890':
                price+=p
            elif p==' ':
                break
        return int(price)
    else:
        return 0

if __name__=='__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('search_term')
    parser.add_argument('--num_pages',default=10)
    parser.add_argument('--csv',action='store_true')
    args=parser.parse_args()

    items=[]

    for page_number in range(1,int(args.num_pages)+1):

        url='https://www.ebay.com/sch/i.html?_from=R40&_nkw='
        url+=args.search_term
        url+='&_sacat=0&LH_TitleDesc=0&_pgn='
        url+=str(page_number)
        url+='&rt=nc'
        print('url=',url)

        r=requests.get(url)
        status=r.status_code
        print('status=',status)
        html=r.text

        soup=BeautifulSoup(html, 'html.parser')

        tags_items=soup.select('.s-item')
        for tag_item in tags_items[1:]:

            tags_name=tag_item.select('.s-item__title')
            name= None
            for tag in tags_name:
                name=tag.text

            freereturns=False
            tags_freereturns=tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns=True

            items_sold= None
            tags_itemssold=tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold=parse_itemssold(tag.text)
            
            tags_price=tag_item.select('.s-item__price')
            price=None
            for tag in tags_price:
                price=parse_price(tag.text)

            tags_status=tag_item.select('.SECONDARY_INFO')
            status=None
            for tag in tags_status:
                status=tag.text
            
            tags_shipping=tag_item.select('.s-item__shipping, .s-item__freeXDays')
            shipping=None
            for tag in tags_shipping:
                shipping=parse_shipping(tag.text)

            item={
                'name':name,
                'free_returns':freereturns,
                'items_sold':items_sold,
                'price': price,
                'status':status,
                'shipping':shipping,
            }
            items.append(item)

    if args.csv==True:
        field_names=list(items[0].keys())
        filename=args.search_term+'.csv'
        with open(filename,'w',encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(items)
    else:
        filename=args.search_term+'.json'
        with open(filename,'w',encoding='ascii')as f:
            f.write(json.dumps(items))