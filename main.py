from app.business_layer.address_service import AddressService


def main():
    address_service = AddressService()

    print("Alle Addresse:")
    for address in address_service.get_all():
        print(f"{address.address_id}: {address.city} ({address.street})")

    address_service.create("test", "test", "test")
    print("Addresse erstellt!")


if __name__ == "__main__":
    main()
