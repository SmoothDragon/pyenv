#!/usr/bin/env python3

description = '''Text manager
Add or remove the multiple line change from the given text file.
Intended use for makefiles that need to alter configuration files.
'''

JSON_template = {
    'lines':[
        '# Example first line',
        'export PATH=$(PATH)',
        '# Do you really need a third line?',
        ],
    'confirm':'y',  # Default will ask to confirm before file modification
    'action':'check',
    }


import argparse
import json
import logging
import os
import shutil
import sys
import time


def parse_arguments(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-v", "--verbose", 
        help="increase output verbosity",
        action="store_true")
    parser.add_argument(
        "--json",
        help="filename containig JSON information",
        type=str,
        default='TextFileModifier.json')
    parser.add_argument(
        "-a", "--action", 
        help="action to perform [toggle, add, delete]",
        type=str,
        default='check')
    args = parser.parse_args()
    if args.verbose:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level)
    return args

def file_check(filename, change):
    '''Check if lines are already present.
    '''
    if not os.path.exists(filename):
        logging.info(f'{filename} does not exist')
        return False
    with open(filename) as infile:
        data = infile.read()
    change_exists = change in data
    if change_exists:
        logging.info(f'{filename} contains lines')
    else:
        logging.info(f'{filename} does not contain lines')
    return change_exists

def file_backup_with_timestamp(filename):
    if not os.path.exists(filename):
        logging.info('No backup created since file does not exist.')
        return
    timestamp = time.time()
    backup = f'{filename}.{timestamp}'
    shutil.copy(filename, backup)
    logging.info(f'{backup} backup file created.')
    return backup

def file_add(filename, change):
    if file_check(filename, change):
        return  # Idempotent. Don't add lines if present
    file_backup_with_timestamp(filename)
    with open(filename, 'a') as outfile:
        outfile.write(change)
    logging.info(f"{filename} lines added")

def file_del(filename, change):
    if not file_check(filename, change):
        # logging.info(f"{filename} doesn't contain lines.")
        return  # Idempotent. Don't remove lines if not present
    file_backup_with_timestamp(filename)
    with open(filename, 'r') as infile:
        data = infile.read()
    outdata = data.replace(change, '')
    with open(filename, 'w') as outfile:
        outfile.write(outdata)
    logging.info(f"{filename} lines removed")

if __name__ == '__main__':
    args = parse_arguments(description)
    logging.debug(args)
    json_file = os.path.expanduser(args.json)
    json_dict = json.load(open(json_file))
    logging.debug(json_dict)
    change = '\n'.join(json_dict['lines'])
    filename = os.path.expanduser(json_dict['filename'])
    if args.action == 'check':
        file_check(filename, change)
    if args.action == 'add':
        file_add(filename, change)
    if args.action == 'delete':
        file_del(filename, change)
