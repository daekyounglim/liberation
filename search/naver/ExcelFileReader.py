import pandas as pd
import pickle

import sys
sys.path.append('/root/liberation/search')
#sys.path.append('C:\\Users\\kang.y.5\\OneDrive - Procter and Gamble\\Documents\\GitHub\\liberation\\search')

print(sys.path)

from util.util import readPickle, writePickle

class ExcelFileReader:

    def read (filepath):
        #Above 10 rows should be skipped in template
        template = pd.read_excel(filepath, skiprows=10)
        writePickle(template, '../data/naver_url.pkl')

    def load (filepath):
        return readPickle(filepath)


if __name__ == "__main__":
    efr = ExcelFileReader
    efr.read('../data/Liberation_Price Tracker SKU list.xlsx')
    print(efr.load('../data/naver_url.pkl'))
