import pypihole

# open and parse logs, be sure that path is right
queries_log = pypihole.parse_log('logs/pihole.log')

# or can use today_log() to get the most recent log if paths are standard
# this assumes /var/logs/pihole.log
# queries_log = pypihole.parse_log(pypihole.today_log())

# get queries or clients output, as well as example filters
# print(pypihole.counts_query(queries))
# print(pypihole.counts_client(queries))
# print(pypihole.counts_query(queries, exclude=['unifi'], include=['openvpn']))
# print(pypihole.counts_query(queries, exclude=['unifi']))
# print(pypihole.counts_query(queries, include=['openvpn']))

# get all queries per client
client_requests = pypihole.queries_per_client(queries_log)
for client, queries in client_requests.items():
    print(client, queries)

# get query counts per client, sorted by frequency
counts = pypihole.query_counts_per_client(queries_log)
for client, value in counts.items():
    print(client, value)
