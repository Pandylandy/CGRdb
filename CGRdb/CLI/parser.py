# -*- coding: utf-8 -*-
#
#  Copyright 2017 Boris Sattarov <brois475@gmail.com>
#  Copyright 2017, 2018 Ramil Nugmanov <stsouko@live.ru>
#  This file is part of CGRdb.
#
#  CGRdb is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from importlib.util import find_spec
from .main_create import create_core
from .main_init import init_core
from .main_populate import populate_core
from ..version import version


def populate(subparsers):
    parser = subparsers.add_parser('populate', help='fill reaction databases',
                                   formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', '-i', default='input.rdf', type=FileType(), help='RDF inputfile')
    parser.add_argument('--parser', '-p', default='none', choices=['reaxys', 'none'], type=str, help='Data Format')
    parser.add_argument('--chunk', '-c', default=1000, type=int, help='Chunks size')
    parser.add_argument('--n_jobs', '-n', default=4, type=int, help='Parallel jobs')
    parser.add_argument('--user', '-u', default=1, type=int, help='User id')
    parser.add_argument("--database", '-db', required=True, help='Database name for populate')
    parser.set_defaults(func=populate_core)


def init_db(subparsers):
    parser = subparsers.add_parser('init', help='initialize postgres db for cartridge using',
                                   formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--user', '-u', default='postgres', help='admin login')
    parser.add_argument('--password', '-p', required=True, help='admin pass')
    parser.add_argument('--host', '-H', default='localhost', help='host name')
    parser.add_argument('--port', '-P', default=5432, help='database port')
    parser.add_argument('--base', '-b', default='postgres', help='database name')
    parser.add_argument('--name', '-n', default='public', help='schema name')
    parser.set_defaults(func=init_core)


def create_db(subparsers):
    parser = subparsers.add_parser('create', help='create new reactions db',
                                   formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--user', '-u', default='postgres', help='admin login')
    parser.add_argument('--password', '-p', required=True, help='admin pass')
    parser.add_argument('--host', '-H', default='localhost', help='host name')
    parser.add_argument('--port', '-P', default=5432, help='database port')
    parser.add_argument('--base', '-b', default='postgres', help='database name')
    parser.add_argument('--name', '-n', help='schema name', required=True)
    parser.add_argument('--config', '-c', default=None, type=FileType(), help='database config in JSON format')
    parser.set_defaults(func=create_core)


def argparser():
    parser = ArgumentParser(description="CGRdb", epilog="(c) Dr. Ramil Nugmanov", prog='cgrdb')
    parser.add_argument("--version", "-v", action="version", version=version(), default=False)
    subparsers = parser.add_subparsers(title='subcommands', description='available utilities')

    create_db(subparsers)
    populate(subparsers)
    init_db(subparsers)

    if find_spec('argcomplete'):
        from argcomplete import autocomplete
        autocomplete(parser)

    return parser
