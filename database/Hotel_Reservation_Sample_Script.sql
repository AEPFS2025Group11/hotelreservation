CREATE TABLE hotel
(
    -- Author: AEP
    id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    stars      INTEGER,
    address_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES address (id) ON DELETE SET NULL
);

CREATE TABLE address
(
    -- Author: AEP
    id       INTEGER PRIMARY KEY,
    street   TEXT NOT NULL,
    city     TEXT NOT NULL,
    zip_code TEXT
);

CREATE TABLE guest
(
    -- Author: AEP
    id             INTEGER PRIMARY KEY,
    first_name     TEXT    NOT NULL,
    last_name      TEXT    NOT NULL,
    email          TEXT UNIQUE,
    phone_number   TEXT    NOT NULL,
    loyalty_points INTEGER NOT NULL,
    address_id     INTEGER,
    FOREIGN KEY (address_id) REFERENCES address (id) ON DELETE SET NULL
);

CREATE TABLE room_type
(
    -- Author: AEP
    id INTEGER PRIMARY KEY,
    description TEXT    NOT NULL UNIQUE, -- E.g., Single, Double, Suite
    max_guests  INTEGER NOT NULL
);

CREATE TABLE room
(
    -- Author: AEP
    id INTEGER PRIMARY KEY,
    hotel_id        INTEGER NOT NULL,
    room_number     TEXT    NOT NULL,
    type_id         INTEGER NOT NULL,
    price_per_night REAL    NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel (id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES room_type (id) ON DELETE CASCADE
);

-- one-to-many mapping with guest, hotel, room
-- one booking can have only one room, but one room can be part of multiple bookings
-- if two rooms are booked for the same dates, two bookings should be created
-- check availability using business logic
CREATE TABLE booking
(
    -- Author: AEP
    id           INTEGER PRIMARY KEY,
    guest_id     INTEGER NOT NULL,
    room_id      INTEGER NOT NULL,
    check_in     DATE    NOT NULL,
    check_out    DATE    NOT NULL,
    is_cancelled BOOLEAN NOT NULL DEFAULT 0, -- 0 = confirmed, 1 = cancelled
    total_amount REAL,
    FOREIGN KEY (guest_id) REFERENCES guest (id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Room (id) ON DELETE CASCADE
);


CREATE TABLE invoice
(
    -- Author: AEP
    id INTEGER PRIMARY KEY,
    booking_id   INTEGER NOT NULL,
    issue_date   DATE    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL    NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES booking (id) ON DELETE CASCADE
);

CREATE TABLE facility
(
    -- Author: AEP
    id INTEGER PRIMARY KEY,
    facility_name TEXT NOT NULL UNIQUE
);

CREATE TABLE room_facility
(
    -- Author: AEP
    room_id     INTEGER NOT NULL,
    facility_id INTEGER NOT NULL,
    PRIMARY KEY (room_id, facility_id),
    FOREIGN KEY (room_id) REFERENCES Room (id) ON DELETE CASCADE,
    FOREIGN KEY (facility_id) REFERENCES facility (id) ON DELETE CASCADE
);

CREATE TABLE review
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL,
    guest_id INTEGER NOT NULL,
    rating   INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment  TEXT,

    FOREIGN KEY (hotel_id) REFERENCES hotel (id) ON DELETE CASCADE,
    FOREIGN KEY (guest_id) REFERENCES guest (id) ON DELETE CASCADE
);

CREATE TABLE payment
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    method     TEXT    NOT NULL,
    status     TEXT    NOT NULL DEFAULT 'pending',
    paid_at    DATE,
    FOREIGN KEY (booking_id) REFERENCES booking (id) ON DELETE CASCADE
);


INSERT INTO address (id, street, city, zip_code)
VALUES (1, 'Bahnhofstrasse 1', 'Zürich', '8001'),
       (2, 'Rue du Rhône 42', 'Genève', '1204'),
       (3, 'Pilatusstrasse 15', 'Luzern', '6003'),
       (4, 'Marktgasse 59', 'Bern', '3011'),
       (5, 'Freiestrasse 10', 'Basel', '4051'),
       (6, 'Seestrasse 18', 'Zürich', '8002'),
       (7, 'Avenue de la Gare 12', 'Lausanne', '1003'),
       (8, 'Kasernenstrasse 25', 'Zug', '6300'),
       (9, 'Dorfstrasse 7', 'St. Moritz', '7500'),
       (10, 'Via San Gottardo 15', 'Lugano', '6900'),
       (11, 'Bahnhofplatz 2', 'Winterthur', '8400'),
       (12, 'Poststrasse 3', 'Chur', '7000'),
       (13, 'Schulhausstrasse 9', 'St. Gallen', '9000'),
       (14, 'Rue de Lausanne 35', 'Neuchâtel', '2000'),
       (15, 'Hauptstrasse 66', 'Thun', '3600');

INSERT INTO hotel (id, name, stars, address_id)
VALUES (1, 'Hotel Baur au Lac', 5, 1),
       (2, 'Four Seasons Hôtel des Bergues', 5, 2),
       (3, 'Grand Hotel National', 5, 3),
       (4, 'Bellevue Palace', 5, 4),
       (5, 'Les Trois Rois', 5, 5),
       (6, 'Park Hyatt Zurich', 5, 6),
       (7, 'Lausanne Palace', 5, 7),
       (8, 'Parkhotel Zug', 4, 8),
       (9, 'Badrutt’s Palace Hotel', 5, 9),
       (10, 'Hotel Splendide Royal', 5, 10),
       (11, 'Sorell Hotel Krone', 4, 11),
       (12, 'ABC Swiss Quality Hotel', 4, 12),
       (13, 'Einstein St. Gallen', 5, 13),
       (14, 'Beau-Rivage Neuchâtel', 5, 14),
       (15, 'Hotel Seepark', 4, 15);

INSERT INTO guest (id, first_name, last_name, email, phone_number, loyalty_points, address_id)
VALUES (1, 'Hans', 'Müller', 'hans.mueller@example.ch', '+41 79 123 45 67', 0, 1),
       (2, 'Sophie', 'Meier', 'sophie.meier@example.ch', '+41 76 234 56 78', 0, 2),
       (3, 'Luca', 'Rossi', 'luca.rossi@example.ch', '+41 78 345 67 89', 0, 3),
       (4, 'Elena', 'Keller', 'elena.keller@example.ch', '+41 77 456 78 90', 0, 4),
       (5, 'Marc', 'Weber', 'marc.weber@example.ch', '+41 79 567 89 01', 0, 5),
       (6, 'Nina', 'Baumann', 'nina.baumann@example.ch', '+41 76 678 90 12', 0, 6),
       (7, 'Thomas', 'Schmid', 'thomas.schmid@example.ch', '+41 78 789 01 23', 0, 7),
       (8, 'Laura', 'Brunner', 'laura.brunner@example.ch', '+41 77 890 12 34', 0, 8),
       (9, 'Fabio', 'Ricci', 'fabio.ricci@example.ch', '+41 79 901 23 45', 0, 9),
       (10, 'Anna', 'Zimmermann', 'anna.zimmermann@example.ch', '+41 76 012 34 56', 0, 10),
       (11, 'Martin', 'Gerber', 'martin.gerber@example.ch', '+41 78 123 45 67', 0, 11),
       (12, 'Julia', 'Graf', 'julia.graf@example.ch', '+41 77 234 56 78', 0, 12),
       (13, 'Pascal', 'Hug', 'pascal.hug@example.ch', '+41 79 345 67 89', 0, 13),
       (14, 'Simone', 'Roth', 'simone.roth@example.ch', '+41 76 456 78 90', 0, 14),
       (15, 'Lena', 'Hofer', 'lena.hofer@example.ch', '+41 78 567 89 01', 0, 15);



INSERT INTO room_type (id, description, max_guests)
VALUES (1, 'Single', 1),
       (2, 'Double', 2),
       (3, 'Suite', 4),
       (4, 'Family Room', 5),
       (5, 'Penthouse', 6);


INSERT INTO room (id, hotel_id, room_number, type_id, price_per_night)
VALUES (1, 1, '101', 1, 250.00),
       (2, 1, '102', 2, 400.00),
       (3, 2, '201', 3, 650.00),
       (4, 3, '301', 4, 900.00),
       (5, 4, '401', 5, 1500.00),
       (6, 6, '202', 2, 420.00),
       (7, 6, '203', 3, 650.00),
       (8, 7, '301', 4, 900.00),
       (9, 8, '101', 2, 280.00),
       (10, 9, '501', 5, 2000.00),
       (11, 10, '601', 3, 700.00),
       (12, 11, '102', 1, 200.00),
       (13, 12, '202', 2, 340.00),
       (14, 13, '303', 3, 800.00),
       (15, 14, '404', 4, 1200.00),
       (16, 15, '505', 1, 220.00),
       (17, 15, '506', 2, 350.00),
       (18, 15, '507', 3, 620.00),
       (19, 13, '304', 4, 1000.00),
       (20, 14, '405', 5, 1800.00);

INSERT INTO booking (id, guest_id, room_id, check_in, check_out, is_cancelled, total_amount)
VALUES (1, 1, 1, '2025-06-01', '2025-06-05', 0, 1000.00),
       (2, 2, 2, '2025-07-10', '2025-07-15', 0, 2000.00),
       (3, 3, 3, '2025-08-20', '2025-08-22', 0, 1300.00),
       (4, 4, 4, '2025-09-05', '2025-09-10', 1, 0.00), -- Cancelled booking
       (5, 5, 5, '2025-10-01', '2025-10-07', 0, 9000.00),
       (6, 6, 6, '2025-05-10', '2025-05-15', 0, 2100.00),
       (7, 7, 7, '2025-06-12', '2025-06-14', 0, 1300.00),
       (8, 8, 8, '2025-07-01', '2025-07-06', 0, 4500.00),
       (9, 9, 9, '2025-08-10', '2025-08-15', 1, 0.00),
       (10, 10, 10, '2025-09-20', '2025-09-25', 0, 10000.00),
       (11, 11, 11, '2025-10-02', '2025-10-06', 0, 2800.00),
       (12, 12, 12, '2025-10-08', '2025-10-12', 0, 800.00),
       (13, 13, 13, '2025-11-01', '2025-11-05', 0, 1360.00),
       (14, 14, 14, '2025-11-10', '2025-11-15', 0, 4000.00),
       (15, 15, 15, '2025-12-01', '2025-12-05', 0, 4800.00);

INSERT INTO invoice (id, booking_id, issue_date, total_amount)
VALUES (1, 1, '2025-06-05', 1000.00),
       (2, 2, '2025-07-15', 2000.00),
       (3, 3, '2025-08-22', 1300.00),
       (4, 5, '2025-10-07', 9000.00),
       (5, 4, '2025-09-10', 0.00),
       (6, 6, '2025-05-15', 2100.00),
       (7, 7, '2025-06-14', 1300.00),
       (8, 8, '2025-07-06', 4500.00),
       (9, 9, '2025-08-15', 0.00),
       (10, 10, '2025-09-25', 10000.00),
       (11, 11, '2025-10-06', 2800.00),
       (12, 12, '2025-10-12', 800.00),
       (13, 13, '2025-11-05', 1360.00),
       (14, 14, '2025-11-15', 4000.00),
       (15, 15, '2025-12-05', 4800.00);

INSERT INTO facility (id, facility_name)
VALUES (1, 'WiFi'),
       (2, 'TV'),
       (3, 'Air Conditioning'),
       (4, 'Mini Bar'),
       (5, 'Balcony');

INSERT INTO room_facility (room_id, facility_id)
VALUES (1, 1),
       (1, 2),
       (2, 1),
       (3, 3),
       (4, 4),
       (6, 1),
       (6, 3),
       (6, 4),
       (7, 2),
       (7, 3),
       (7, 5),
       (8, 1),
       (8, 2),
       (8, 5),
       (10, 4),
       (10, 5),
       (11, 1),
       (11, 2),
       (12, 3),
       (12, 4),
       (13, 1),
       (13, 2),
       (13, 3),
       (14, 5),
       (15, 1),
       (15, 2),
       (15, 4),
       (16, 1),
       (16, 3),
       (17, 2),
       (17, 4),
       (18, 3),
       (18, 5),
       (19, 4),
       (19, 5),
       (20, 1),
       (20, 2),
       (20, 3),
       (20, 4),
       (20, 5);

INSERT INTO review (hotel_id, guest_id, rating, comment)
VALUES (1, 1, 5, 'Fantastischer Aufenthalt, alles war perfekt!'),
       (2, 3, 4, 'Sehr schönes Hotel, aber Frühstück war mittelmäßig.'),
       (3, 5, 3, 'Zimmer war okay, aber Lage nicht optimal.'),
       (1, 2, 5, 'Super freundliches Personal und saubere Zimmer.'),
       (4, 4, 2, 'Leider sehr laut in der Nacht.'),
       (2, 6, 4, 'Tolle Lage, würden wieder kommen.'),
       (5, 7, 1, 'Nie wieder, schlechte Erfahrung.');

INSERT INTO payment (booking_id, method, status, paid_at)
VALUES (1, 'credit_card', 'paid', '2025-06-01'),
       (2, 'paypal', 'paid', '2025-07-10'),
       (3, 'bank_transfer', 'paid', '2025-08-20'),
       (5, 'credit_card', 'paid', '2025-10-01'),
       (6, 'paypal', 'paid', '2025-05-10'),
       (7, 'credit_card', 'paid', '2025-06-12'),
       (8, 'bank_transfer', 'paid', '2025-07-01'),
       (10, 'credit_card', 'paid', '2025-09-20'),
       (11, 'paypal', 'paid', '2025-10-02'),
       (12, 'credit_card', 'paid', '2025-10-08'),
       (13, 'credit_card', 'paid', '2025-11-01'),
       (14, 'bank_transfer', 'paid', '2025-11-10'),
       (15, 'paypal', 'paid', '2025-12-01');
