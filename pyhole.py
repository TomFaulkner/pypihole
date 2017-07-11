import pypihole


# for line in pypihole.parse_log('pihole.log'):
#     print(line)

queries = pypihole.parse_log('pihole.log')

print(pypihole.counts_query(queries))
print(pypihole.counts_client(queries))
print(pypihole.counts_query(queries, exclude=['unifi'], include=['openvpn']))
print(pypihole.counts_query(queries, exclude=['unifi']))
print(pypihole.counts_query(queries, include=['openvpn']))
