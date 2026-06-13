# 📊 Data Explorer

Aplikacja webowa oparta na Django do wgrywania, przechowywania i eksploracji plików CSV.  
Umożliwia podgląd danych i automatyczną analizę statystyczną każdego pliku CSV bez konieczności znajomości struktury kolumn.

---

## 🚀 Uruchomienie projektu (krok po kroku)

### Wymagania wstępne

- **Python 3.10+** (sprawdź: `python --version` lub `python3 --version`)
- **Git** (sprawdź: `git --version`)

---

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/karolkamuda89-ux/Projekt.git
cd Projekt
```

---

### 2. Tworzenie i aktywacja wirtualnego środowiska

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Po aktywacji na początku linii terminala pojawi się `(venv)`.

---

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

Instalowane pakiety: Django 6, pandas, numpy i inne.

---

### 4. Przygotowanie bazy danych

```bash
python manage.py migrate
```

Tworzy plik `db.sqlite3` z wymaganymi tabelami.

---

### 5. Uruchomienie serwera deweloperskiego

```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: **http://127.0.0.1:8000/**

Zatrzymanie serwera: `Ctrl + C`

---

## 🗺️ Nawigacja po aplikacji

### Strona główna — `http://127.0.0.1:8000/`

Widok powitalny. Dla zalogowanych użytkowników wyświetla:
- liczbę wgranych plików,
- nazwę i datę ostatnio wgranego pliku,
- przycisk szybkiego dodania kolejnego pliku.

---

### Rejestracja i logowanie

Aby korzystać z aplikacji, potrzebujesz konta.

1. Kliknij **„Zaloguj"** w prawym górnym rogu nawigacji.
2. Na stronie logowania kliknij zakładkę **„Zarejestruj się"** (lub przejdź do `/register/`).
3. Podaj **nazwę użytkownika**, **adres e-mail** i **hasło** (min. 10 znaków, nie może być zbyt pospolite).
4. Po rejestracji zaloguj się tymi samymi danymi.

---

### Wgrywanie pliku CSV — `/upload/`

1. Kliknij **„Wgraj CSV"** w nawigacji.
2. Wypełnij pola:
   - **Nazwa pliku** — dowolna nazwa opisowa (np. „Sprzedaż Q1 2025")
   - **Opis** — opcjonalny opis zestawu danych
   - **Plik CSV** — wybierz plik z dysku (tylko `.csv`)
3. Kliknij **„Wgraj"**.
4. Zostaniesz automatycznie przekierowany do widoku szczegółów.

> ⚠️ Aplikacja akceptuje **wyłącznie pliki `.csv`**. Inne formaty zostaną odrzucone z komunikatem błędu.

---

### Lista plików — `/list/`

Tabela z wszystkimi Twoimi wgranymi plikami. Możesz:
- **Wyszukiwać** pliki po nazwie (pole wyszukiwania na górze — działa w czasie rzeczywistym podczas pisania, a po naciśnięciu „Szukaj" filtruje po stronie serwera)
- **Sortować** kolumny klikając nagłówki: ID, Nazwa pliku, Data wgrania
- Przejść do **szczegółów** pliku przyciskiem „Szczegóły"
- **Usunąć** plik przyciskiem „Usuń" (wymaga potwierdzenia)

---

### Szczegóły pliku — `/detail/<id>/`

Główny widok analityczny. Wyświetla dla każdego wgranego pliku CSV:

#### 📁 Metadane pliku
- ID w bazie, data wgrania, rozmiar pliku, status analizy

#### 📊 Podstawowe statystyki
- Liczba wierszy (rekordów)
- Liczba kolumn
- Całkowita liczba pustych komórek
- Liczba przeanalizowanych kolumn

#### 🔍 Szczegóły kolumn
Karty dla każdej kolumny z automatycznym wykryciem typu:

| Typ kolumny | Wyświetlane informacje |
|---|---|
| **Liczbowa** | Min, Średnia, Max, liczba brakujących wartości |
| **Tekstowa / kategoryczna** | Liczba unikalnych wartości, najczęstsza wartość, liczba brakujących wartości |
| **Pusta** | Informacja o braku danych |

Możesz filtrować karty klikając: **Wszystkie / Liczbowe / Tekstowe / Puste**

#### 📉 Wykresy (Chart.js)
- **Wykres słupkowy** — braki danych per kolumna (pojawia się tylko gdy są braki)
- **Wykres doughnut** — rozkład typów kolumn (liczbowe / tekstowe / puste)

#### Pobieranie i usuwanie
- Przycisk **„⬇️ Pobierz CSV"** — pobiera oryginalny plik
- Przycisk **„Usuń plik"** — usuwa plik z bazy i dysku (z oknem potwierdzenia)

---

## 🏗️ Struktura projektu

```
Projekt/
├── manage.py                          # Punkt wejścia Django
├── requirements.txt                   # Zależności Python
├── db.sqlite3                         # Baza danych (tworzy się po migrate)
│
├── data_explorer_project/             # Konfiguracja projektu
│   ├── settings.py                    # Ustawienia Django
│   ├── urls.py                        # Główny routing URL
│   └── wsgi.py
│
├── datasets/                          # Główna aplikacja
│   ├── models.py                      # Model UploadedFile
│   ├── views.py                       # Logika widoków
│   ├── utils.py                       # Funkcja get_statistics (analiza CSV)
│   ├── urls.py                        # Routing aplikacji
│   ├── admin.py
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── templates/
│       └── datasets/
│           ├── index.html             # Strona główna (szablon bazowy)
│           ├── list.html              # Lista plików
│           ├── detail.html            # Szczegóły i analiza pliku
│           └── upload.html            # Formularz wgrywania
│
├── media/
│   └── datasets/                      # Wgrane pliki CSV (tworzone automatycznie)
│
└── static/
    └── css/
        └── main.css                   # Style aplikacji
```

---

## 🛠️ Technologie

| Technologia | Zastosowanie |
|---|---|
| **Django 6** | Framework webowy (MVT) |
| **pandas** | Analiza i statystyki plików CSV |
| **SQLite** | Baza danych (plik `db.sqlite3`) |
| **Bootstrap 5** | Responsywny interfejs użytkownika |
| **Chart.js** | Wykresy statystyk |
| **AOS** | Animacje przy przewijaniu |

---

## ❓ Najczęstsze problemy

**`ModuleNotFoundError: No module named 'django'`**  
Wirtualne środowisko nie jest aktywne. Aktywuj je (krok 2) i spróbuj ponownie.

**`django.db.utils.OperationalError: no such table`**  
Nie wykonano migracji. Uruchom `python manage.py migrate`.

**Strona nie ładuje się po `runserver`**  
Upewnij się, że serwer działa (nie ma błędów w terminalu) i że wchodzisz na `http://127.0.0.1:8000/`, a nie `https://`.

**Błąd przy wgrywaniu pliku**  
Upewnij się, że plik ma rozszerzenie `.csv`. Pliki `.xlsx`, `.txt` itp. są odrzucane.

---

## 👥 Autorzy

Projekt grupowy — przedmiot Programowanie Aplikacji Webowych.