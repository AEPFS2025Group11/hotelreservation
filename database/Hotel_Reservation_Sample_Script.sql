CREATE TABLE Hotel
(
    -- Author: AEP
    hotel_id   INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    stars      INTEGER,
    address_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE SET NULL
);

CREATE TABLE Address
(
    -- Author: AEP
    address_id INTEGER PRIMARY KEY,
    street     TEXT NOT NULL,
    city       TEXT NOT NULL,
    zip_code   TEXT
);

CREATE TABLE Guest
(
    -- Author: AEP
    guest_id   INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT UNIQUE,
    address_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE SET NULL
);

CREATE TABLE Room_Type
(
    -- Author: AEP
    type_id     INTEGER PRIMARY KEY,
    description TEXT    NOT NULL UNIQUE, -- E.g., Single, Double, Suite
    max_guests  INTEGER NOT NULL
);

CREATE TABLE Room
(
    -- Author: AEP
    room_id         INTEGER PRIMARY KEY,
    hotel_id        INTEGER NOT NULL,
    room_number     TEXT    NOT NULL,
    type_id         INTEGER NOT NULL,
    price_per_night REAL    NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel (hotel_id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES room_type (type_id) ON DELETE CASCADE
);

-- one-to-many mapping with guest, hotel, room
-- one booking can have only one room, but one room can be part of multiple bookings
-- if two rooms are booked for the same dates, two bookings should be created
-- check availability using business logic
CREATE TABLE Booking
(
    -- Author: AEP
    booking_id     INTEGER PRIMARY KEY,
    guest_id       INTEGER NOT NULL,
    room_id        INTEGER NOT NULL,
    check_in_date  DATE    NOT NULL,
    check_out_date DATE    NOT NULL,
    is_cancelled   BOOLEAN NOT NULL DEFAULT 0, -- 0 = confirmed, 1 = cancelled
    total_amount   REAL,
    FOREIGN KEY (guest_id) REFERENCES guest (guest_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Room (room_id) ON DELETE CASCADE
);


CREATE TABLE Invoice
(
    -- Author: AEP
    invoice_id   INTEGER PRIMARY KEY,
    booking_id   INTEGER NOT NULL,
    issue_date   DATE    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL    NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES booking (booking_id) ON DELETE CASCADE
);

CREATE TABLE Facilities
(
    -- Author: AEP
    facility_id   INTEGER PRIMARY KEY,
    facility_name TEXT NOT NULL UNIQUE -- E.g., "Shower", "TV", "WiFi", "Air Conditioning"
);

CREATE TABLE Room_Facilities
(
    -- Author: AEP
    room_id     INTEGER NOT NULL,
    facility_id INTEGER NOT NULL,
    PRIMARY KEY (room_id, facility_id),
    FOREIGN KEY (room_id) REFERENCES Room (room_id) ON DELETE CASCADE,
    FOREIGN KEY (facility_id) REFERENCES facility (facility_id) ON DELETE CASCADE
);


INSERT INTO address (address_id, street, city, zip_code)
VALUES (1, 'Bahnhofstrasse 1', 'Zürich', '8001'),
       (2, 'Rue du Rhône 42', 'Genève', '1204'),
       (3, 'Pilatusstrasse 15', 'Luzern', '6003'),
       (4, 'Marktgasse 59', 'Bern', '3011'),
       (5, 'Freiestrasse 10', 'Basel', '4051');

INSERT INTO hotel (hotel_id, name, stars, address_id)
VALUES (1, 'Hotel Baur au Lac', 5, 1),
       (2, 'Four Seasons Hôtel des Bergues', 5, 2),
       (3, 'Grand Hotel National', 5, 3),
       (4, 'Bellevue Palace', 5, 4),
       (5, 'Les Trois Rois', 5, 5);

INSERT INTO guest (guest_id, first_name, last_name, email, address_id)
VALUES (1, 'Hans', 'Müller', 'hans.mueller@example.ch', 1),
       (2, 'Sophie', 'Meier', 'sophie.meier@example.ch', 2),
       (3, 'Luca', 'Rossi', 'luca.rossi@example.ch', 3),
       (4, 'Elena', 'Keller', 'elena.keller@example.ch', 4),
       (5, 'Marc', 'Weber', 'marc.weber@example.ch', 5);


INSERT INTO room_type (type_id, description, max_guests)
VALUES (1, 'Single', 1),
       (2, 'Double', 2),
       (3, 'Suite', 4),
       (4, 'Family Room', 5),
       (5, 'Penthouse', 6);


INSERT INTO Room (room_id, hotel_id, room_number, type_id, price_per_night)
VALUES (1, 1, '101', 1, 250.00),
       (2, 1, '102', 2, 400.00),
       (3, 2, '201', 3, 650.00),
       (4, 3, '301', 4, 900.00),
       (5, 4, '401', 5, 1500.00);

INSERT INTO booking (booking_id, guest_id, room_id, check_in_date, check_out_date, is_cancelled, total_amount)
VALUES (1, 1, 1, '2025-06-01', '2025-06-05', 0, 1000.00),
       (2, 2, 2, '2025-07-10', '2025-07-15', 0, 2000.00),
       (3, 3, 3, '2025-08-20', '2025-08-22', 0, 1300.00),
       (4, 4, 4, '2025-09-05', '2025-09-10', 1, 0.00), -- Cancelled booking
       (5, 5, 5, '2025-10-01', '2025-10-07', 0, 9000.00);

INSERT INTO invoice (invoice_id, booking_id, issue_date, total_amount)
VALUES (1, 1, '2025-06-05', 1000.00),
       (2, 2, '2025-07-15', 2000.00),
       (3, 3, '2025-08-22', 1300.00),
       (4, 5, '2025-10-07', 9000.00),
       (5, 4, '2025-09-10', 0.00); -- Cancelled booking, no charge

INSERT INTO facility (facility_id, facility_name)
VALUES (1, 'WiFi'),
       (2, 'TV'),
       (3, 'Air Conditioning'),
       (4, 'Mini Bar'),
       (5, 'Balcony');

INSERT INTO room_facility (room_id, facility_id)
VALUES (1, 1), -- Room 101 has WiFi
       (1, 2), -- Room 101 has TV
       (2, 1), -- Room 102 has WiFi
       (3, 3), -- Room 201 has Air Conditioning
       (4, 4); -- Room 301 has Mini Bar