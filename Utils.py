import json
import logging
import os
import time
import urllib.request
from os.path import exists, join

from bs4 import BeautifulSoup

import Config


def create_directory(directory, show_logging=False):
    if not exists(directory):
        if show_logging:
            logging.info(' Create All Directories in Path %s' % directory)
        os.makedirs(directory)


def get_json_filename(directory, filename):
    filename = str(filename).replace('.json', '')
    return join(directory, filename+'.json')


def save_json(directory, filename, dict_to_save, encoding='utf8', sort_keys=True):
    create_directory(directory)
    information_filename = get_json_filename(directory, filename)
    json_file = open(information_filename, 'w+', encoding=encoding)
    json_dumps = json.dumps(dict_to_save, ensure_ascii=False, indent=2, sort_keys=sort_keys)
    json_file.write(json_dumps)
    json_file.close()


def get_parsed_html_page(link):
    http_conn = urllib.request.urlopen(link)
    date = http_conn.headers['Date']
    epoch_time = convert_http_response_date_to_epoch_time(date)
    page = http_conn.read()
    parsed_page = BeautifulSoup(page, 'lxml')
    return parsed_page, epoch_time


def get_kg_tuple(sub, prd, obj, src, version):
    kg_tuple = dict()
    kg_tuple['subject'] = sub.strip() if sub else sub
    kg_tuple['predicate'] = prd
    kg_tuple['object'] = obj.strip() if obj else obj
    kg_tuple['source'] = src
    kg_tuple['version'] = version
    kg_tuple['module'] = 'web_table_extractor'
    kg_tuple['class'] = 'Professor'
    return kg_tuple


def convert_http_response_date_to_epoch_time(date):
    epoch_time = str(int(time.mktime(time.strptime(date, Config.http_response_date_template))))
    return epoch_time


def generate_each_faculty_tuples(full_name, faculty, website, link, version,
                                 first_name=None, last_name=None, group=None, grade=None,
                                 image=None, mail=None, address=None, phone=None, fax=None):
    faculty_tuples = list()
    if first_name:
        faculty_tuples.append(get_kg_tuple(full_name, 'نام', first_name, link, version))
    if last_name:
        faculty_tuples.append(get_kg_tuple(full_name, 'نام خانوادگی', last_name, link, version))
    faculty_tuples.append(get_kg_tuple(full_name, 'دانشکده', faculty, link, version))
    if group:
        faculty_tuples.append(get_kg_tuple(full_name, 'گروه', group, link, version))
    if grade:
        faculty_tuples.append(get_kg_tuple(full_name, 'رتبه دانشگاهی', grade, link, version))
    faculty_tuples.append(get_kg_tuple(full_name, 'website', website, link, version))
    if image:
        faculty_tuples.append(get_kg_tuple(full_name, 'تصویر', image, link, version))
    if mail:
        faculty_tuples.append(get_kg_tuple(full_name, 'پست الکترونیکی', mail, link, version))
    if address:
        faculty_tuples.append(get_kg_tuple(full_name, 'آدرس', address, link, version))
    if phone:
        faculty_tuples.append(get_kg_tuple(full_name, 'تلفن', phone, link, version))
    if fax:
        faculty_tuples.append(get_kg_tuple(full_name, 'فکس', fax, link, version))

    return faculty_tuples
