#!/usr/bin/env python

import argparse
import os

def read_output_file(file):
    with open(file, 'r') as read_handler:
        for line in read_handler:
            line = line.strip()
            if not line:
                continue
            yield line


def convert(paths, output_file):
    files = os.listdir(paths)
    file_list=[]
    for file in files:
        if file.find('.')>=0:
            file_list.append(file)
    with open(output_file, 'w') as write_handler:
        for bin_id, file in enumerate(file_list):
            for sequence_id in read_output_file(paths+'/'+file):
                write_handler.write("%s,%s\n" % (sequence_id, bin_id))


def main():
    parser = argparse.ArgumentParser(description="Convert bins file to one result file")
    parser.add_argument("--paths", help="output files path")
    parser.add_argument("-o", "--output_file", required=False, help="Output file")
    args = parser.parse_args()
    convert(args.paths, args.output_file)


if __name__ == "__main__":
    main()
