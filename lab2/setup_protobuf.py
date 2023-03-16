setup_protobuf = '''
import google.protobuf
import my_message_pb2

# Создание объекта MyMessage
my_message = my_message_pb2.MyMessage()
my_message.PackageID = 1539
my_message.PersonID = 33
my_message.Name = "MEGA_GAMER_2222"
my_message.Inventory.i0 = 0
my_message.Inventory.i1 = 1
my_message.Inventory.i2 = 2
my_message.Inventory.i3 = 3
my_message.Inventory.i4 = 4
my_message.Inventory.i5 = 5
my_message.Inventory.i6 = 6
my_message.Inventory.i7 = 7
my_message.Inventory.i8 = 8
my_message.Inventory.i9 = 9
my_message.Inventory.i10 = 10
my_message.Inventory.i11 = 11
my_message.Inventory.i12 = 12
my_message.Inventory.i13 = 13
my_message.Inventory.i14 = 14
my_message.Inventory.i15 = 15
my_message.Inventory.i16 = 16
my_message.Inventory.i17 = 17
my_message.Inventory.i18 = 18
my_message.Inventory.i19 = 19
my_message.Inventory.i20 = 20
my_message.Inventory.i21 = 21
my_message.Inventory.i22 = 22
my_message.Inventory.i23 = 23
my_message.Inventory.i24 = 24
my_message.Inventory.i25 = 25
my_message.Inventory.i26 = 26
my_message.Inventory.i27 = 27
my_message.Inventory.i28 = 28
my_message.Inventory.i29 = 29
my_message.CurrentLocation = """
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

src = my_message.SerializeToString()
'''
