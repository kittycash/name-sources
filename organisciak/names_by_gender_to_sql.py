#!/usr/bin/python3

import sys
import csv
import json

source = "https://github.com/organisciak/names/blob/master/data/us-names-by-gender.csv"
alphabet = "Latin"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("bad args")
        print("")
        print("Usage: %(base)s input_csv" % {
            'base': sys.argv[0]
        })
        exit(1)
    with open(sys.argv[1]) as csvfile:
        items = csv.reader(csvfile)
        for row in items:
            gender, name, count = row
            print("insert into names values(%(alphabet)s, %(source)s, %(name)s);" % {
                'name': json.dumps(name),
                'source': json.dumps(source),
                'alphabet': json.dumps(alphabet)
            })
