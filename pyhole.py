import pypihole


queries = pypihole.parse_log('pihole.log')

print(pypihole.counts_query(queries))
print(pypihole.counts_client(queries))
print(pypihole.counts_query(queries, exclude=['unifi'], include=['openvpn']))
print(pypihole.counts_query(queries, exclude=['unifi']))
print(pypihole.counts_query(queries, include=['openvpn']))

client_counts = pypihole.queries_per_client(queries)
for client, queries in client_counts.items():
    print(client, queries)
