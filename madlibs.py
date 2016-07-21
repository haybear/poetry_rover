#!/usr/bin/env python3

# Copyright (C) 2016 Haybear
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import csv
import os
import random
import sqlite3
import sys


PARTS_OF_SPEECH = ['template', 'verb', 'noun']


def create_db(db_filepath):
    """Create the db.

    See https://pymotw.com/2/sqlite3/ , seems like a good idea.

    """
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()
    for part_of_speech in PARTS_OF_SPEECH:
        sql = 'create table {part_of_speech}s ({part_of_speech} text)'.format(
            part_of_speech=part_of_speech)
        cursor.execute(sql)
    conn.commit()


def import_csv_to_db(db_filepath, csv_filepath, part_of_speech):
    """Import csv to db, to table of name part_of_speech."""
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()
    with open(csv_filepath, 'rt') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        sql = ('insert into {part_of_speech}s '
               'values (:{part_of_speech})').format(
                   part_of_speech=part_of_speech)
        cursor.executemany(sql, csv_reader)
    conn.commit()


def import_csvs_to_db(db_filepath):
    """Load initial data csvs into the db.

    NOTE that we assume the csvs are shipped in the same dir as __name__.

    """
    for part_of_speech in PARTS_OF_SPEECH:
        import_csv_to_db(
            db_filepath,
            os.path.join(os.path.dirname(__file__), part_of_speech+'s.csv'),
            part_of_speech)


class Word:

    def __init__(self, db_filepath):
        if not os.path.exists(db_filepath):
            create_db(db_filepath)
            import_csvs_to_db(db_filepath)
        self.conn = sqlite3.connect(db_filepath)
        self.cursor = self.conn.cursor()

    def get_number_of_words(self, part_of_speech):
        """Part of speech word count in our db."""
        result = self.cursor.execute(
            "select count(*) from {}s".format(part_of_speech))
        return result.fetchone()[0]

    def get_random_word(self, part_of_speech):
        """Retrieve a random word of the given part of speech from the db."""
        count = self.get_number_of_words(part_of_speech)
        random_rowid = random.randint(1, count)
        sql = ('select {part_of_speech} from {part_of_speech}s '
               'where rowid={random_rowid}').format(
                   part_of_speech=part_of_speech,
                   random_rowid=random_rowid)
        return self.cursor.execute(sql).fetchone()[0]


class Noun(Word):

    def __str__(self):
        return self.get_random_word('noun')


class Verb(Word):

    def __str__(self):
        return self.get_random_word('verb')


class Template(Word):
    # A template is a kind of word in that we store it in a db and
    # need to retrieve a random one occasionally ;) .

    def __str__(self):
        return self.get_random_word('template')

    def format(self, *args, **kwargs):
        # I admit this is kind-of evil :)
        return str(self).format(**kwargs)


def substitute(db_filepath, template):
    """Render the given template with words from the given db.

    The template must bear markers for substitution:

        These weapons {verb} a computerized {noun} fire control system

    . . . and corresponding tables must exist in given db.

    """
    if template is None:
        template = Template(db_filepath)
    return template.format(
        noun=Noun(db_filepath),
        verb=Verb(db_filepath),
    )


def _parse_arguments():
    parser = argparse.ArgumentParser(
        "Substitute a given template with random verbs and nouns.")
    parser.add_argument(
        help='Sqlite3 database filepath.',
        type=str,
        dest='db_filepath',
    )
    parser.add_argument(
        '-t',
        '--template',
        help='Template with {verb} and {noun} substitution markers.',
        type=str,
        required=False,
    )
    return parser.parse_args()


def main():
    args = _parse_arguments()
    print(substitute(args.db_filepath, args.template))


if __name__ == "__main__":
    sys.exit(main())
