"""
Auto Archive Bulk Downloader Script v1.0.0

Downloads automatic archives from the Learn Content System and stores them either locally or streams them to S3.
"""

import argparse
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import re
import sys
import getpass
import urllib.parse
import datetime
import os

STDOUT_TIME_FORMAT = "%Y/%m/%d"
COURSE_CREATION_TIME_FORMAT = "%Y%m%d"

OUTPUT_DIR = r"/outbox"
COURSE_LIST_FILE = r"list.txt"

debug = False


# Grabs the hrefs from DASL response
def extract_hrefs(xml):
    hrefs = []
    for response in ET.fromstring(xml):
        for entry in response:
            if entry.tag == '{DAV:}href':
                hrefs.append(entry.text)

    return hrefs


def replace_right(source, target, replacement, replacements=None):
    return replacement.join(source.rsplit(target, replacements))


def get_inputs():
    parser = argparse.ArgumentParser(description='Archive downloader')
    parser.add_argument('-u', '--user', help='User to authenticate with', required=True)
    parser.add_argument('-f', '--file', help='File containing course ids, one per each line. Not pk1s. Required if --beginDate and --endDate are not present',
                        required='-b' not in sys.argv and '--beginDate' not in sys.argv)
    # parser.add_argument('-b', '--beginDate',
                        # help='Date in the format YYYY/MM/DD. If present, includes course ids of courses created from the specified date\n' +
                             # 'to the specified date in --endDate. Required if --endDate is present', required='-e' in sys.argv or '--endDate' in sys.argv)
    # parser.add_argument('-e', '--endDate',
                        # help='Date in the format YYYY/MM/DD. If present, includes all course ids of courses created until the specified date\n' +
                              # 'in --beginDate. Required if --beginDate is present', required='-b' in sys.argv or '--beginDate' in sys.argv)
    if len(sys.argv) > 1:
        return parser.parse_args()
    else:
        parser.print_help()

        print('Running with developer settings, see correct settings above')
        return argparse.Namespace(**{
            'site': 'https://mylearn.int.bbpd.io',
            'user': 'administrator',
            'file': '/tmp/feed.txt',
            'output': '/tmp/',
            'debug': False
        })


# Takes a given URL and streams to either a local file or to S3
def write_output_response(input_url, output_location):
    file_response = session.get(input_url, stream=True)

    if 4 == 6:
        pass
    else:
        with open(output_location, 'wb') as new_file:
            for chunk in file_response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    new_file.write(chunk)

    # Close since we streamed
    file_response.close()


# Performs a directory listing (aka PROPFIND) on the item
def prop_find(url, auth, session):
    if debug:
        print('Performing PROPFIND on ' + url)
    response = session.request('PROPFIND', url, auth=auth,
                               headers={'Depth': '1', 'Content-Type': 'application/xml'})

    if debug:
        print(response)
        print(response.headers)
        print(response.text)

    return extract_hrefs(response.text)


# This is a little brittle, could get dates from webdav, dealing with XML is a pain
auto_archive_timestamp = re.compile(
    '^https://.*/internal/autoArchive/(?P<course_id>.*)_\\d{8}/(?P<package_type>.*)_(?P<timestamp>\\d{13}).*zip\\Z')


def find_latest_zip(course_url, auth, session):
    candidate_hrefs = prop_find(course_url, auth, session)
    current_max = 0
    current_candidate = None
    for href in candidate_hrefs:
        timestamp_match = auto_archive_timestamp.search(href)
        if timestamp_match:
            timestamp = int(timestamp_match.group('timestamp'))
            course_id = timestamp_match.group('course_id')
            package_type = timestamp_match.group('package_type')
            if timestamp > current_max and package_type.startswith(course_id):
                current_max = timestamp
                current_candidate = href

    print(current_candidate)
    return current_candidate

def terminate_learn_session(base_url, session):
    response = session.get(base_url + '/webapps/login/?action=logout')

    if debug:
        print('Terminating Learn Session')
        print(response)
        print(response.headers)


# This script works by doing the following:
# 1) Performs a full listing of the auto archive directory. This is a little heavy, but saves subsequent calls
#    and is relatively cheap for Xythos to do.
# 2) For each found directory extract the course id and see if we are looking for it
# 3) Find the latest zip for that directory and stream it and it's log file to the output location
with requests.Session() as session:
    inputs = get_inputs()
    print("WARNING: Executing multiple instances of this script at the same time may cause performance degradation.")
    print(inputs)
    base_url = "ENTER BASE URL HERE"
    user = inputs.user
    url = base_url + '/bbcswebdav/internal/autoArchive'
    password = getpass.getpass()
    auth = HTTPBasicAuth(user, password)
    # try:
        # beginDate = inputs.beginDate and datetime.datetime.strptime(inputs.beginDate, STDOUT_TIME_FORMAT)
        # endDate = inputs.endDate and datetime.datetime.strptime(inputs.endDate, STDOUT_TIME_FORMAT)
    # except:
        # raise Exception('Incorrect date format, the format should be YYYY/MM/DD')

    # if beginDate and endDate and beginDate > endDate:
        # raise Exception('The beginning date should be less or equal to the end date. The date range was {} - {}'
                        # .format(inputs.beginDate, inputs.endDate))

    if os.path.exists(COURSE_LIST_FILE):
    #if inputs.file:
        course_ids = set()
        with open(COURSE_LIST_FILE) as f:
            for course_id in f.readlines():
                course_id = course_id.strip().lower()
                course_ids.add(course_id)

    # This performs a full directory listing on /internal/autoArchive.
    # Other methods were used to more efficiently search and were not working in production
    auto_archive_listing = prop_find(url, auth, session)
    course_id_to_url = []
    course_id_url_regex = re.compile('^https://.*/internal/autoArchive/(?P<course_id>.*)_(?P<course_creation_date>\\d{8})/\\Z')
    errors = {}
    courses_not_in_date_range = set()
    for course_url in auto_archive_listing:
        matches = course_id_url_regex.search(course_url)
        if not matches:
            continue

        current_course_id = matches.group('course_id').lower()
        if COURSE_LIST_FILE and current_course_id not in course_ids:
            continue

        course_creation_date = datetime.datetime.strptime(matches.group('course_creation_date'), COURSE_CREATION_TIME_FORMAT)
        # if beginDate and endDate and (beginDate > course_creation_date or endDate < course_creation_date):
            # if inputs.file:
                # courses_not_in_date_range.add(current_course_id)
                # course_ids.remove(current_course_id)
            # continue

        try:
            print('Found course folder for course_id: ' + current_course_id + ' - file: ' + course_url)

            file_url = find_latest_zip(course_url, auth, session)

            print('Found file for course_id: ' + current_course_id + ' - file: ' + file_url)
            output_file_name = os.path.join(OUTPUT_DIR, urllib.parse.unquote(file_url.split('/')[-1]))

            write_output_response(file_url, output_file_name)

            # Attempt to grab the log file for this archive
            log_file_url = replace_right(file_url, '.zip', '.txt', 1)
            log_file_output = replace_right(output_file_name, '.zip', '.txt', 1)

            write_output_response(log_file_url, log_file_output)

            if COURSE_LIST_FILE:
                course_ids.remove(current_course_id)

        except Exception as e:
            errors[current_course_id] = e
            if COURSE_LIST_FILE:
                course_ids.remove(current_course_id)

    print(str(len(errors.items())) + ' courses with errors:')
    for course, error in errors.items():
        print('Error with course ' + course)
        print(error)

    if COURSE_LIST_FILE:
        print(str(len(course_ids)) + ' courses not found:')
        for not_found in course_ids:
            print(not_found)

    # if inputs.file and beginDate:
        # print(str(len(courses_not_in_date_range)) + ' courses found but not in date range:')
        # for not_in_date_range in courses_not_in_date_range:
            # print(not_in_date_range)

    terminate_learn_session(base_url, session)