import clink
from clink.com import find
from clink import Service


coms = find(clink.service, Service)
for com in coms:
    print(com.__name__)
