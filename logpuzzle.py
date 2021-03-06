#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1;
en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++

    # split image name by -
    # if split is long enough, switch long_string to True
    # if long_string is True
    # Sort the url strings by the last four characters before .jpg

    long_string = False
    file_object = open(filename, "r")
    url_strings = []

    for line in file_object:
        if re.search(r'puzzle', line):
            url_search = re.search(r'(?<=GET\s)(.*)(?=\sHTTP)', line).group()
            img_name = url_search.split('/')[-1]
            print img_name
            split_lst = img_name.split('-')
            if len(split_lst) > 2:
                long_string = True
            url_string = 'http://code.google.com' + url_search
            url_strings.append(url_string)

    if long_string:
        url_lst = sorted(url_strings, key=lambda x: x[-7:-3])
    else:
        url_lst = sorted(set(url_strings))

    for url in url_lst:
        print url
    return url_lst


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    html_file = open(dest_dir + '/index.html', 'w')
    open_html = """<html><head></head><body>"""
    message = ""
    closing_html = """</body></html>"""

    for i, img in enumerate(img_urls):
        print 'Retrieving'
        # Grab image and add it to local destination
        img_dest = './' + dest_dir + '/img' + str(i) + '.png'
        urllib.urlretrieve(img, img_dest)

        # Add image destination to image tags for html
        img_tag = "<img src='" + img + "'>"
        message += img_tag

    full_html = open_html + message + closing_html
    html_file.write(full_html)
    html_file.close()
    return


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
