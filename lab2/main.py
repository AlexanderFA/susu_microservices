from tabulate import tabulate
import timeit
import sys

message = '''d = {
    'PackageID' : 1539,
    'PersonID' : 33,
    'Name' : "MEGA_GAMER_2222",
    'Inventory': dict(("i" + str(i),i) for i in range(100)),
    'CurrentLocation': """
        Pentos is a large port city, more populous than Astapor on Slaver Bay,
        and may be one of the most populous of the Free Cities.
        It lies on the bay of Pentos off the narrow sea, with the Flatlands
        plains and Velvet Hills to the east.
        The city has many square brick towers, controlled by the spice traders.
        Most of the roofing is done in tiles. There is a large red temple in
        Pentos, along with the manse of Illyrio Mopatis and the Sunrise Gate
        allows the traveler to exit the city to the east,
        in the direction of the Rhoyne.
        """
    }'''

setup_pickle = '%s ; import pickle ; src = pickle.dumps(d)' % message
setup_json = '%s ; import json; src = json.dumps(d)' % message
setup_xml = '%s ; import xmltodict; src = xmltodict.unparse({"root": d})' % message

tests = [
    # (title, setup, enc_test, dec_test)
    ('native', setup_pickle, 'src = pickle.dumps(d)', 'pickle.loads(src)'),
    ('json', setup_json, 'src = json.dumps(d)', 'json.loads(src)'),
    ('xml', setup_xml, 'src = xmltodict.unparse({"root": d})', 'xmltodict.parse(src)'),
]

loops = 100
enc_table, dec_table = [], []

print('Running tests (%d loops each)' % loops)

for title, mod, enc, dec in tests:
    print(title)
    print(" [Encode]", enc)
    result = timeit.timeit(stmt=enc, setup=mod, number=loops)
    exec(mod)
    enc_table.append([title, result, sys.getsizeof(src)])

    print(" [Decode]", dec)
    result = timeit.timeit(dec, mod, number=loops)
    dec_table.append([title, result])

enc_table.sort(key=lambda x: x[1])
enc_table.insert(0, ['Package', 'Seconds', 'Size'])
dec_table.sort(key=lambda x: x[1])
dec_table.insert(0, ['Package', 'Seconds'])

print("Encoding Test (%d loops)" % loops)
print(tabulate(enc_table, headers="firstrow"))

print("\nDecoding Test (%d loops)" % loops)
print(tabulate(dec_table, headers="firstrow"))
