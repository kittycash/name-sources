#!/usr/bin/python3

import sys
import csv
import json
import hashlib

alphabet = "Latin"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("bad args")
        print("")
        print("Usage: %(base)s input_csv" % {
            'base': sys.argv[0]
        })
        exit(1)
    source_filename = sys.argv[1]
    source_hash = ""
    with open(source_filename, 'rb') as f:
        m = hashlib.sha256()
        m.update(f.read())
        source_hash = m.hexdigest()
    source = source_filename + ":" + source_hash
    with open(source_filename) as csvfile:
        items = csv.reader(csvfile)
        for row in items:
            alphabet, name = row[0:2]
            print("insert into names values(%(alphabet)s, %(source)s, %(name)s, true);" % {
                'name': json.dumps(name),
                'source': json.dumps(source),
                'alphabet': json.dumps(alphabet)
            })
