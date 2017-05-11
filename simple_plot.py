import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import psycopg2
import json
import seaborn as sns
import sys

def make_plot(calo_num):
    dbconf = None
    with open('dbconnection.json', 'r') as f:
        dbconf = json.load(f)

    cnx = psycopg2.connect(user=dbconf['user'], password=dbconf['password'],
                           host=dbconf['host'],
                           database=dbconf['dbname'], port=dbconf['port'])
    cursor=cnx.cursor()
    cursor.execute("select value, time from g2sc_values where channel='calo{}temps' and time > '2017-5-3'".format(calo_num))
    sipmnames = ['SiPM{}'.format(i) for i in range(54)] 
    temps, times = zip(*cursor)

    cursor.close()
    cnx.close()

    # build pandas dataframe
    tempframe = pd.DataFrame(np.array(temps), columns=sipmnames, index=np.array(times))
    # mask out failed reads
    tempframe = tempframe[(tempframe > 20) & (tempframe < 50)]

    tempframe.plot(legend=False)

    plt.savefig('calo{}temps.pdf'.format(calo_num))


def main():
    if len(sys.argv) < 2:
        print('requires calo num')
        sys.exit(0)

    calo_num = int(sys.argv[1])
    make_plot(calo_num)

if __name__ == '__main__':
    main()
