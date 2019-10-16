#!/usr/bin/env python

import argparse
import os


def add_header_fags(input_file, SampleID, output_file):
    with open(output_file, 'w') as write_handler:
        write_handler.write("@Version:0.9.0"+'\n')
        write_handler.write("@SampleID:"+SampleID+'\n')
        write_handler.write("@@SEQUENCEID"+'\t'+"BINID"+ '\n')
        with open(input_file, 'r') as read_handler:
            for line in read_handler:
                write_handler.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--input_file",  help="Iutput files path")
    parser.add_argument("-f", help="Input the SampleID")
    parser.add_argument("-o", "--output_file", help="Output file")
    args = parser.parse_args()
    add_header_fags(args.input_file, args.f, args.output_file)


if __name__ == "__main__":
    main()
