
# 🏨 HotelReservation

Dieses Repository wird im Rahmen des Moduls **"FS25 Anwendungsentwicklung mit Python"** (Gruppe A & B) von der Gruppe **B-team11** verwendet.

---

## 🚀 Wichtige Befehle

### 🔧 Starten des Backends

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 5049
```

### 📄 Generieren der aktuellen API-Dokumentation (OpenAPI)

Um einen Überblick über alle verfügbaren Backend-Schnittstellen zu erhalten, kann folgender Befehl ausgeführt werden:

```bash
curl http://localhost:5049/openapi.json -o openapi.json
```

Alternativ steht auch eine browserbasierte Ansicht unter [http://localhost:5049/redoc](http://localhost:5049/redoc) zur Verfügung – vorausgesetzt, der Server läuft.

---

# 📚 Dokumentation

In diesem Kapitel werden die grundlegenden **Software- und Architekturentscheidungen** erklärt und dargestellt.

---

## 🧩 UML-Beziehungen

Die folgenden Abschnitte geben einen Überblick über typische **UML-Klassenbeziehungen**, wie sie auch in unserem **Visual Paradigm Klassendiagramm** verwendet wurden.

---

### 🔗 Association

Eine allgemeine Beziehung zwischen zwei Klassen. Beispiel: Eine Schule kann unabhängig von Lehrern existieren und umgekehrt.

```python
class School:
    def __init__(self, name):
        self.name = name


class Teacher:
    def __init__(self, name, school):
        self.name = name
        self.school = school  # Association: Teacher is linked to a School


school = School("Greenwood High")
teacher = Teacher("Mr. Smith", school)

print(teacher.name)         # Output: Mr. Smith
print(teacher.school.name)  # Output: Greenwood High
```

---

### 🧺 Aggregation

Stellt eine **schwache Parent-Child-Beziehung** dar. Beispiel: Ein Spieler existiert auch, wenn das Team gelöscht wird.

```python
class Player:
    def __init__(self, name):
        self.name = name


class Team:
    def __init__(self, players):
        self.players = players  # Aggregation


player1 = Player("Alice")
player2 = Player("Bob")

my_team = Team([player1, player2])
print(my_team.players[0].name)  # Output: Alice

del my_team
print(player1.name)             # Output: Alice
```

---

### ⚙️ Composition

Stellt eine **starke Parent-Child-Beziehung** dar. Beispiel: Ein Motor gehört zum Auto – wenn das Auto zerstört wird, verschwindet auch der Motor.

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower


class Car:
    def __init__(self, horsepower):
        self.engine = Engine(horsepower)  # Composition


my_car = Car(200)
print(my_car.engine.horsepower)  # Output: 200
```

---
# 🏗️ Backend Architektur

Dieses Dokument beschreibt die Architektur des Backend-Systems, basierend auf einer N-Tier Architektur mit FastAPI, SQLAlchemy und weiteren unterstützenden Libraries.

---

## 🔄 N-Tier Architektur

Die Anwendung ist in klar getrennte Schichten unterteilt, um Wartbarkeit, Testbarkeit und Skalierbarkeit zu gewährleisten.

### 📍 API (Application Programming Interface)

- Definiert die HTTP-Endpunkte (REST).
- Handhabt eingehende Anfragen und sendet Antworten.
- Nutzt Pydantic-Modelle zur Validierung und Serialisierung.

### ⚙️ Services

- Enthält die zentrale Geschäftslogik.
- Verarbeitet validierte Daten aus der API-Schicht.
- Ruft Methoden aus der Repository-Schicht auf.

#### 📦 DTOs (Data Transfer Objects)

- Repräsentieren strukturierte Daten, die zwischen Schichten ausgetauscht werden.
- Basieren auf Pydantic für automatische Validierung und Typsicherheit.

### 🗃️ Repositories

- Zuständig für den Datenzugriff (CRUD-Operationen).
- Verwenden SQLAlchemy für ORM-Funktionalität.
- Trennen Persistenzlogik von der Geschäftslogik.

### 🧬 Entities

- Datenbankmodelle, die mit Tabellenstrukturen korrespondieren.
- Definiert mithilfe von SQLAlchemy ORM.
- Enthalten Felder und optionale Relationen.

---

## 📚 Eingesetzte Libraries

| Library     | Beschreibung                                                                 |
|-------------|------------------------------------------------------------------------------|
| [FastAPI](https://fastapi.tiangolo.com/)     | Modernes Web-Framework für schnelle APIs mit automatischer Doku.      |
| [SQLAlchemy](https://www.sqlalchemy.org/)    | ORM für die objektorientierte Datenbankmodellierung.                 |
| [Pydantic](https://docs.pydantic.dev/latest/) | Validierung und Serialisierung von Daten mit Python-Typen.          |
| [Uvicorn](https://www.uvicorn.org/)          | Leichtgewichtiger ASGI-Server für asynchrone Webanwendungen.        |

---

## 📁 Projektstruktur

```text
backend/
│
├── app/
│   ├── api/              # API-Routen (Controller)
│   ├── auth/             # Auth-Logik
│   ├── database/         # Datenbank
│   ├── entities/         # SQLAlchemy-Modelle (Entities)
│   ├── repositories/     # Datenzugriff / Repositories
│   ├── services/         # Geschäftslogik
│   │   └── models/       # Pydantic-Modelle (DTOs)
│   ├── util/             # Hilfsklassen
│   └── main.py           # FastAPI Entry Point
│
├── requirements.txt      # Python Abhängigkeiten
└── README.md             # Projektbeschreibung
