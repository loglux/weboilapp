import requests
import requests_cache
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html


class Oil:
    def __init__(self, company, url, method):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla / 5.0 (Linux; Android  6.0)'})
        self.url = url
        self.company = company
        self.method = method
        #self.catalogue = []
        if self.method == 'hannah_start()':
            self.hannah_start()
        if self.method == 'fast_start()':
            self.fast_start()
        if self.method == 'bangor_start()':
            self.bangor_start()
        if self.method == 'patterson_start()':
            self.patterson_start()

    def oil_connect(self):
        """ TODO: Create an exception if the website is unavailable. """
        requests_cache.install_cache('spy',  backend='sqlite', expire_after=3600)
        try:
            r = self.session.get(self.url)
        except requests.exceptions.RequestException:
            return None
        # for the future revision, study p.56 Web Scraping
        soup = BeautifulSoup(r.text, features="lxml")
        return soup

    """ Hannas, Patterson, DAndrews """
    def wp_soup(self, soup):
        page = soup.find_all('form', class_='variations_form')
        page = str(page)
        return page

    """ Bangor Oil """
    def bangor_soup(self, soup):
        page = soup.find_all('p', class_='product woocommerce add_to_cart_inline')
        page = str(page)
        return page

    """ Fast Oil """
    def fast_soup(self, soup):
        small = soup.find('table', attrs={"id": "SmallFillsGridView"})
        large = soup.find('table', attrs={"id": "LargeFillsGridView"})
        return small, large

    """ Hannah, DAndriews, Patterson, Bangor as they use the same e-commerce plugin for WordPress """
    def wp_parser(self, page):
        wp_prices = []
        """ pattersonoil hannas deandrews """
        text_prices = re.findall(r'[0-9]{2,3}[.][0-9]{2}\&', page)
        if not text_prices:
            """ bangor fuels """
            text_prices = re.findall(r'[0-9]{2,3}[.][0-9]{2}', page)
            """ Removing duplicates: """
            text_prices = list(dict.fromkeys(text_prices))
        """ pattersonoil (hannas) """
        text_litres = re.findall(r'litres[":]*[0-9]{2,4}', page)
        #text_litres = list(dict.fromkeys(text_litres))
        if not text_litres:
            """ DAndrews and Hannas """
            text_litres = re.findall(r'[0-9]{2,4}\s[Ll][Ii][Tt][Rr][Ee][Ss]', page)
            if not text_litres:
                text_litres = re.findall(r'[0-9]{2,4}[Ll]', page)
        text_litres = list(dict.fromkeys(text_litres))
        litres = []
        for e in text_litres:
            e = str(e).replace('litres":"', '')
            e = str(e).replace(' LITRES', '')
            e = str(e).replace(' Litres', '')
            e = str(e).replace('L', '')
            litres.append(e)
        prices = []
        for b in text_prices:
            b = str(b).replace('&', '')
            prices.append(b)
        for l, p in zip(litres, prices):
            d = {'Litres': l, 'Price': p}
            wp_prices.append(d)
        #print(wp_prices)
        return wp_prices

    """ Fast Oil """
    def fast_parser(self, small, large):
        headers = ['Litres', 'Price']
        union = [small, large]
        full_table = []
        for e in union:
            fast_data = e.find_all("tr")
            fast_oil = []
            for tr in fast_data:
                td = tr.find_all('td')
                row = [i.text for i in td]
                if len(row) == 3:
                    del row[-1]
                """ Removing £ sign """
                clear_row = []
                for e in row:
                    e = e.replace('£', '')
                    clear_row.append(e)
                row_dict = dict(zip(headers, clear_row))
                fast_oil.append(row_dict)
            del fast_oil[0]
            full_table = full_table + fast_oil
            """ Removing duplicate for 500.
                res_list = [i for n, i in enumerate(test_list) if i not in test_list[n + 1:]]
            """
            # full_table = [i for n, i in enumerate(full_table) if i not in full_table[n + 1:]]
        # print(full_table)
        #self.catalogue = full_table
        return full_table

    """ Fast Oil. Could be part of fast_parser """
    def remove_dups(self, full_table):
        full_table = [i for n, i in enumerate(full_table) if i not in full_table[n + 1:]]
        return full_table

    def save_to_csv(self, catalogue, file_name):
        # file_name = "oil"
        """ TODO: create an exception if file is not exists or busy """
        columns = list(catalogue[0].keys())
        csv_file = file_name + ".csv"
        try:
            with open(csv_file, 'w') as csvfile:
                self.writer = csv.DictWriter(csvfile, fieldnames=columns)
                self.writer.writeheader()
                [self.writer.writerow(data) for data in catalogue]
                # for data in self.car_catalogue:
                #   self.writer.writerow(data)
        except IOError:
            print("I/O error")

    def print_table(self, catalogue):
        """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
        If column names (colList) aren't specified, they will show in random order.
        Author: Thierry Husson - Use it as you want but don't blame me.
        """
        # https://stackoverflow.com/questions/17330139/python-printing-a-dictionary-as-a-horizontal-table-with-headers
        # table_catalogue = []
        columns = list(catalogue[0].keys())
        my_list = [columns]  # 1st row = header
        for item in catalogue:
            my_list.append([str(item[col] if item[col] is not None else '') for col in columns])
        col_size = [max(map(len, col)) for col in zip(*my_list)]
        format_str = ' | '.join(["{{:<{}}}".format(i) for i in col_size])
        my_list.insert(1, ['-' * i for i in col_size])  # Separating line
        for item in my_list:
            print(format_str.format(*item))

    def pd_table(self, catalogue):
        """ TODO: Check value for Litres and make a list. """
        """ TODO: unite different tables using Litres as index """
        # https://kite.com/python/answers/how-to-add-a-column-to-a-pandas-dataframe-as-the-index-in-python
        #for e in catalogue:
        #    print("<td>" + e['Litres'] + "<\\td>")
        #columns = list(catalogue[0].keys())
        df = pd.DataFrame(catalogue)
        df['Price'] = df['Price'].astype(float).round(2)
        df['Litres'] = df['Litres'].astype(int)
        df['Ratio £/L'] = df['Price'] / df['Litres']
        df['Ratio £/L'] = df['Ratio £/L'].round(2)
        df = df.set_index("Litres")
        df = df.T  # or df.transpose()
        pd.set_option('display.width', None)
        #print(df)
        self.text_table = df
        columns = [100, 200, 300, 500]
        for i in catalogue:
            if i['Litres'] == '900':
                columns.append(900)
        self.html = df.to_html(columns=columns, classes="supplier-table table table-striped border text-center")
        #< h3 > < a class ='btn btn-link' href='#' > back < / a > < / h3 >
        #self.company = "<h3><a href=\"" + self.url + " >" + self.compnay + "</a></h3"
        self.company = f"<h3><a href=\"{self.url}\">{self.company}</a></h3>"
        self.html = self.company + self.html
        return self.html

    """ Bangor Fuels """
    def bangor_start(self):
        r = self.oil_connect()
        page = self.bangor_soup(r)
        catalogue = self.wp_parser(page)
        #print(catalogue)
        #file_name = "bangorfuels"
        #self.save_to_csv(catalogue, file_name)
        #self.print_table(catalogue)
        self.pd_table(catalogue)
        return catalogue

    """ Patterson Oil """
    def patterson_start(self):
        r = self.oil_connect()
        page = self.wp_soup(r)
        catalogue = self.wp_parser(page)
        #print(type(catalogue))
        catalogue.reverse()
        #catalogue.sort(key='Litres')
        #print(catalogue)
        #file_name = "patterson"
        #print(catalogue)
        self.pd_table(catalogue)
        #self.html_table(df, catalogue)
        #self.save_to_csv(catalogue, file_name)
        #self.print_table(catalogue)
        return catalogue

    """ Hannah, DAndrews """
    def hannah_start(self):
        r = self.oil_connect()
        page = self.wp_soup(r)
        catalogue = self.wp_parser(page)
        #print(catalogue)
        #file_name = "hannah"
        #self.save_to_csv(catalogue, file_name)
        #self.print_table(catalogue)
        self.pd_table(catalogue)
        return catalogue

    """ Fast Oil """
    def fast_start(self):
        r = self.oil_connect()
        small, large = self.fast_soup(r)
        full_table = self.fast_parser(small, large)
        catalogue = self.remove_dups(full_table)
        #file_name = "fastoil"
        #print(full_table)
        #self.save_to_csv(catalogue, file_name)
        #self.print_table(catalogue)
        self.pd_table(catalogue)
        # self.pd_table(catalogue)
        return catalogue


class Infos():
    def __init__(self):
        self.html_tables = []


if __name__ == '__main__':
    delivers = [{'company': 'Hannah\'s Town', 'url': 'https://hannahstownfuels.com/oil/home-heating-oil/',
                 'method': 'hannah_start()'},
                {'company': 'D.E. Andrews', 'url': 'https://www.deandrews.co.uk/product/oil-price-checker/',
                 'method': 'hannah_start()'},
                {'company': 'Fast Oils', 'url': 'http://fastoils.com/', 'method': 'fast_start()'},
                {'company': 'Bangor Fuels', 'url': 'https://bangorfuels.com/order-oil/', 'method': 'bangor_start()'},
                {'company': 'Patterson Oil',
                 'url': 'https://pattersonoil.co.uk/store/buy-home-heating-oil-uk/bt5-heating-oil-kerosene28/',
                 'method': 'patterson_start()'}]
    storage = Infos()
    for deliver in delivers:
        obj = Oil(deliver['company'], deliver['url'], deliver['method'])
        t = obj.html
        print(deliver['url'])
        print(obj.text_table)
        #print(obj.html)
        storage.html_tables.append(t)
    tables_in_post = storage.html_tables
    #print(tables_in_post)


# re.sub(' mytable', '" id="mytable', df.to_html(classes='mytable'))