from hotelreservation.model.address import Address
from hotelreservation.model.guest import Guest

if __name__ == '__main__':
    address = Address("test address", "kajs", "3422")

    guest = Guest("test", "test", "test", address)