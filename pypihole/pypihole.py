import datetime
import glob
from collections import Counter
from functools import partial
from typing import NamedTuple

pihole_log_path = '/var/log'
pihole_log_name = 'pihole.log'


class Query(NamedTuple):
    dt: str
    record_type: str
    query: str
    client: str


def parse_log(log_fn: str) -> list:
    """ 
    Parse log file, returning list of Query namedtuples
    TODO: Add returns for other interesting types of entries
    :param log_fn: log file name / path
    :return: list of Query namedtuples
    """
    queries = []
    with open(log_fn) as log_file:
        for line in log_file:
            # Jul 10 23:35:23 dnsmasq[4260]: query[A] ddg.gg from 192.168.1.100
            if 'query[' in line:
                m, d, t, _, record_type, query, _, client = line.split()
                record_type = record_type.split('[')[1][:-1]
                # TODO: Find a better way: if dec 31 was yesterday then year
                #  would be wrong. Surely some library handles this.
                dt = datetime.datetime.strptime(
                    f"{datetime.datetime.now().year} {m} {d} {t}",
                    '%Y %b %d %H:%M:%S')
                queries.append(Query(dt, record_type, query, client))
            # TODO: Add parsing of other lines
    return queries


def _counts_generic(queries: list, include: list=None,
                    exclude: list=None, **kwargs) -> dict:
    """
    Count queries, using kwarg index_to_count, which is namedtuple
     Query named index such as 'query' or 'client'
    Return Counter object

    Best used by counts_client and counts_queries partials

    :param queries: list of Query objects
    :param include: list of strings to whitelist on, if None no
     whitelisting occurs
    :param exclude: list of strings to blacklist
    :param kwargs: index_to_count, what Query index to count
    :return: Counter keyed on Query.index_to_count
    """
    index_to_count = kwargs.get('index_to_count', 'query')
    counter = Counter()
    for entry in queries:
        if _query_filter(getattr(entry, index_to_count), include, exclude):
            counter[getattr(entry, index_to_count)] += 1
    return counter


counts_client = partial(_counts_generic, index_to_count='client')
counts_client.__doc__ = """Counts queries and returns a Counter of all domains queries

    Filters are literal and must match exactly
    
    >>> counts_client(queries, include=['192.168.1.100', '192.168.1.101'], 
                      exclude=['192.168.1.1'])

    :param queries: list of Query namedtuples
    :param include: list of items to include, works as whitelist
    :param exclude: list of items to exclude, works as blacklist
    :return: Counter keyed to dns query
    """


counts_query = partial(_counts_generic, index_to_count='query')
counts_query.__doc__ = """Counts client requests and returns a Counter of all clients

    Filters are literal and must match exactly
    
    >>> counts_query(queries, include=['duckduckgo.com'], 
                      exclude=['google.com'])

    :param queries: list of Query namedtuples
    :param include: list of items to include, works as whitelist
    :param exclude: list of items to exclude, works as blacklist
    :return: Counter keyed to client ip query
    """


def _query_filter(entry: str, include: list = None, exclude: list = None)\
        -> bool:
    """
    Include and exclude work as a whitelist and a blacklist.
    If include is not None, but is a list, then only whitelisted entries
     will be returned.
    If exclude is not None, but is a list, then anything blacklisted won't be 
     returned.
    Both include and exclude can be provided at the same time, however, it 
     the exclude list is redundant at that point, unless it overlaps with some
     of the whitelist, in which case whitelisted entries included in the
      blacklist will be excluded.
    
    :param entry: any string, intended for Query fields 
    :param include: list of items to match and include, must be exact match
    :param exclude: list of items to exclude, must be exact match
    :return: boolean, whether to include or not
    """
    # TODO: Add regex options with their own lists
    # TODO: Make generic and put in helpers file for own use in other projects
    if not include:
        include = []
    if not exclude:
        exclude = []

    if not include and not exclude:
        return True
    elif include:
        if entry in include and entry not in exclude:
            return True
    elif exclude and entry not in exclude:
        return True
    return False


def _get_log_file():
    for log in glob.glob(f'{pihole_log_path}/{pihole_log_name}'):
        yield log


def today_log():
    return f'{pihole_log_path}/{pihole_log_name}'
