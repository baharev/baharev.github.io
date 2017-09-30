#!/usr/bin/env python3
# Copyright (C) 2016, 2017 by Ali Baharev <ali.baharev@gmail.com>
# All rights reserved.
# BSD license.

from os import listdir
from os.path import isdir

def main():
    ignore = set(('__pycache__', 'images', 'nyuszi_template'))
    dirs = sorted(e for e in listdir('.') if isdir(e) and e not in ignore)
    print(', '.join(dirs))
    links = '\n'.join(to_link(d) for d in dirs)
    with open('index.html', 'w') as f:
        f.write(PREAMBLE)
        f.write(links)
        f.write(POSTAMBLE)

def to_link(d):
    return '    <li><a href="{0}">{0}</a></li>'.format(d)


PREAMBLE = \
'''<!doctype html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sandbox projects</title>
    <style type="text/css">
        html, body {
            background-color: lightgray;
            width: 100%;
            height: 100%;
            padding: 0;
            margin: 0;
        }
        ul {
            list-style-type: none;
        }
        li {
            margin-bottom: 3ex;
        }
    </style>
</head>
<body>
    <ul>
'''

POSTAMBLE = \
'''
    </ul>
</body>
</html>
'''

if __name__ == '__main__':
    main()
