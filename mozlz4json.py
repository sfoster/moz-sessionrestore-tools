#!/usr/bin/env python
#
# Based on mozlz4a.py, by Tilman Blumenbach, via https://gist.github.com/kaefer3000/73febe1eec898cd50ce4de1af79a332a
# Modified by Sam Foster to parse the decompressed input as JSON and output a pretty-printed JSON document 
#
# Decompressor/compressor for files in Mozilla's "mozLz4" format. Firefox uses this file format to
# compress e. g. bookmark backups (*.jsonlz4).
#
# This file format is in fact just plain LZ4 data with a custom header (magic number [8 bytes] and
# uncompressed file size [4 bytes, little endian]).
#
# This Python 3 script requires the LZ4 bindings for Python, see: https://pypi.python.org/pypi/lz4
#
#
# Copyright (c) 2015, Tilman Blumenbach
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
#    and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of
#    conditions and the following disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import lz4.block
import sys
import json

from argparse import ArgumentParser


class MozLz4aError(Exception):
    pass


class InvalidHeader(MozLz4aError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def decompress(file_obj):
    if file_obj.read(8) != b"mozLz40\0":
        raise InvalidHeader("Invalid magic number")

    return lz4.block.decompress(file_obj.read())

def compress(file_obj):
    compressed = lz4.block.compress(file_obj.read())
    return b"mozLz40\0" + compressed

def compress_json(data):
    json_str = json.dumps(data, separators=(',', ':'))
    compressed = lz4.block.compress(json_str.encode())
    return b"mozLz40\0" + compressed

if __name__ == "__main__":
    argparser = ArgumentParser(description="MozLz4a compression/decompression utility")
    argparser.add_argument(
            "-d", "--decompress", "--uncompress",
            action="store_true",
            help="Decompress the input file instead of compressing it."
        )
    argparser.add_argument(
            "--rawcompress",
            action="store_true",
            help="Compress the input file without first parsing it as JSON."
        )
    argparser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print decompressed output."
        )
    argparser.add_argument(
            "in_file",
            help="Path to input file."
        )
    argparser.add_argument(
            "out_file",
            nargs="?",
            help="Path to output file.",
        )

    parsed_args = argparser.parse_args()
    output_string = parsed_args.decompress

    try:
        in_file = open(parsed_args.in_file, "rb")
    except IOError as e:
        print("Could not open input file `%s' for reading: %s" % (parsed_args.in_file, e), file=sys.stderr)
        sys.exit(2)
    
    if parsed_args.out_file: 
        try:
            out_file = open(parsed_args.out_file, "w" if output_string else "wb")
        except IOError as e:
            print("Could not open output file `%s' for writing: %s" % (parsed_args.out_file, e), file=sys.stderr)
            sys.exit(3)
    else:
        out_file = sys.stdout 

    if parsed_args.rawcompress:
        data = compress(in_file)

    elif parsed_args.decompress:
        try:
            raw = decompress(in_file)
            if raw[0] == 'b':
                raw = raw[1:]
        except Exception as e:
            print("Could not decompress file `%s': %s" % (parsed_args.in_file, e), file=sys.stderr)
            sys.exit(4)

        try:
            data = json.loads(raw)
        except Exception as e:
            print("Couldn't parse file as JSON `%s': %s" % (parsed_args.in_file, e), file=sys.stderr)
            # print(raw, file=sys.stdout)
            sys.exit(4)

        if parsed_args.pretty:
            data = json.dumps(data, indent=2) + "\n"
        else:
            data = json.dumps(data)

    else:
        try: 
            data = json.loads(in_file.read())
        except Exception as e:
            print("Couldn't parse input file as JSON `%s': %s" % (parsed_args.in_file, e), file=sys.stderr)
            sys.exit(4)
        try:
            data = compress_json(data)
        except Exception as e:
            print("Could not compress JSON from `%s': %s" % (parsed_args.in_file, e), file=sys.stderr)
            sys.exit(4)

    try:
        out_file.write(data)
    except IOError as e:
        print("Could not write to output file `%s': %s" % (parsed_args.out_file, e), file=sys.stderr)
        sys.exit(5)
    finally:
        out_file.close()
