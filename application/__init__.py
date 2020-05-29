import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from application.oil import Oil
from application.oil import Infos

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    @app.route('/')
    def home():
        delivers = [{'company': 'Hannah\'s Town', 'url': 'https://hannahstownfuels.com/oil/home-heating-oil/',
                     'method': 'hannah_start()'},
                    {'company': 'D.E. Andrews', 'url': 'https://www.deandrews.co.uk/product/oil-price-checker/',
                     'method': 'hannah_start()'},
                    {'company': 'Fast Oils', 'url': 'http://fastoils.com/', 'method': 'fast_start()'},
                    {'company': 'Bangor Fuels', 'url': 'https://bangorfuels.com/order-oil/',
                     'method': 'bangor_start()'},
                    {'company': 'Patterson Oil',
                     'url': 'https://pattersonoil.co.uk/store/buy-home-heating-oil-uk/bt5-heating-oil-kerosene28/',
                     'method': 'patterson_start()'}]
        storage = Infos()
        for deliver in delivers:
            obj = Oil(deliver['company'], deliver['url'], deliver['method'])
            t = obj.html
            #print(deliver['url'])
            #print(obj.text_table)
            storage.html_tables.append(t)
        table = storage.html_tables
        #print(table)
        return render_template('table.html', table=table)
    return app