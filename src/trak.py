#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import uuid
import argparse
from datetime import datetime


filename = '/Users/torn/.trak'

def record(args):
    '''
    Add a new record to file
    '''

    if args.date is not None:
        #try:
        date = datetime.strptime(args.date, '%d%m%y')
        #except ValueError:
        #    print('Could not parse date')
        #    sys.exit()
    else:
        date = datetime.today()

    identifier = uuid.uuid4()
    datestring = date.strftime('%Y-%m-%d')

    with open(filename, 'a') as file:
        file.write(f'{datestring};{args.exercise_type};{args.number};{args.sets};{args.weight};{identifier};{args.comment}\n')

def plot(args):
    '''
    Make a plot of progress from file
    '''
    import plotext as plt
    from pandas import read_csv
    df = read_csv(filename, delimiter=';', parse_dates=['Date'])
    mask = df['Exercise'] == args.exercise_type
    today = datetime.today()
    days = [int((d - today).total_seconds() / (24*3600)) for d in df['Date'][mask]]
    plt.plot(days, df['Number'][mask], fillx=True)
    plt.xlabel('Days before present')
    plt.ylabel('Number')
    plt.ylim(lower=0)
    plt.show()

if __name__ == '__main__':

    # Read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('exercise_type', metavar='exercise type')
    parser.add_argument('number', nargs='?', type=int)
    parser.add_argument('-s', '--sets', dest='sets', default=1, type=int)
    parser.add_argument('-w', '--weight', dest='weight', default=0, type=int)
    parser.add_argument('-d', '--date', dest='date', default=None)
    parser.add_argument('-c', '--comment', dest='comment', default='')
    parser.add_argument('-p', '--plot', dest='plot', action='store_true')
    args = parser.parse_args()

    # Decide what to do based on arguments:
    if args.plot:
        plot(args)
    else:
        record(args)
