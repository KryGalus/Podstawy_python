
import json
import urllib.request
from datetime import datetime

def pobierz_kurs_waluty_na_dzien(waluta, data):
    url = f'http://api.nbp.pl/api/exchangerates/rates/a/{waluta}/{data}/'

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            kurs_waluty = round(data['rates'][0]['mid'], 2)  # Zaokrąglamy do dwóch miejsc po przecinku
            return kurs_waluty
    except Exception as e:
        print(f'Błąd: {e}')
        return None

def oblicz_roznice_kursow(waluta, data1, data2):
    kurs1 = pobierz_kurs_waluty_na_dzien(waluta, data1)
    kurs2 = pobierz_kurs_waluty_na_dzien(waluta, data2)

    if kurs1 is not None and kurs2 is not None:
        roznica = round(kurs2 - kurs1, 2)  # Zaokrąglamy do dwóch miejsc po przecinku
        return roznica
    else:
        return None

def oblicz_kwote_po_kursie(kwota, kurs):
    return round(kwota * kurs, 2)

def zapisz_do_pliku(wyniki):
    with open('wynik.txt', 'w') as file:
        file.write(wyniki)

# Wprowadzanie daty wystawienia faktury przez użytkownika
try:
    data_wystawienia_faktury = input('Podaj datę wystawienia faktury w formacie RRRR-MM-DD: ')
    data_wystawienia_faktury = datetime.strptime(data_wystawienia_faktury, '%Y-%m-%d')
except ValueError:
    print('Proszę o wprowadzenie poprawnej daty.')
    exit()

# Wprowadzenie daty opłacenia faktury przez użytkownika
try:
    data_oplacenia_faktury = input('Podaj datę opłacenia faktury w formacie RRRR-MM-DD: ')
    data_oplacenia_faktury = datetime.strptime(data_oplacenia_faktury, '%Y-%m-%d')
except ValueError:
    print('Proszę o wprowadzenie poprawnej daty.')
    exit()

# Sprawdzenie, czy data opłacenia nie jest wcześniejsza niż data wystawienia faktury
if data_oplacenia_faktury < data_wystawienia_faktury:
    print('Data opłacenia nie może być wcześniejsza niż data wystawienia faktury.')
    exit()

# Wybór waluty
waluta = input('Podaj kod waluty (EUR, GBP, USD): ').upper()

# Sprawdzenie poprawności kodu waluty
if waluta not in ['EUR', 'GBP', 'USD']:
    print('Proszę o wprowadzenie poprawnego kodu waluty.')
    exit()

# Wprowadzenie kwoty z faktury
try:
    kwota_z_faktury = float(input('Podaj kwotę z faktury: '))
except ValueError:
    print('Proszę o wprowadzenie poprawnej kwoty.')
    exit()

# Przykład użycia funkcji
kurs_wystawienia_faktury = pobierz_kurs_waluty_na_dzien(waluta, data_wystawienia_faktury.strftime('%Y-%m-%d'))
kurs_oplacenia_faktury = pobierz_kurs_waluty_na_dzien(waluta, data_oplacenia_faktury.strftime('%Y-%m-%d'))

if kurs_wystawienia_faktury is not None:
    print(f'Aktualny kurs {waluta} na dzień {data_wystawienia_faktury}: {kurs_wystawienia_faktury}')
else:
    print(f'Nie udało się pobrać kursu {waluta} dla podanej daty wystawienia faktury.')

if kurs_oplacenia_faktury is not None:
    print(f'Aktualny kurs {waluta} na dzień {data_oplacenia_faktury}: {kurs_oplacenia_faktury}')
else:
    print(f'Nie udało się pobrać kursu {waluta} dla daty opłacenia faktury.')

# Obliczanie różnicy kursów
roznica_kursow = oblicz_roznice_kursow(waluta, data_wystawienia_faktury.strftime('%Y-%m-%d'), data_oplacenia_faktury.strftime('%Y-%m-%d'))

if roznica_kursow is not None:
    print(f'Różnica kursowa między {data_wystawienia_faktury} a {data_oplacenia_faktury}: {roznica_kursow}')
else:
    print('Nie udało się obliczyć różnicy kursów.')

# Obliczanie kwoty po kursie z daty wystawienia faktury
kwota_po_kursie_wystawienia = oblicz_kwote_po_kursie(kwota_z_faktury, kurs_wystawienia_faktury)

# Obliczanie kwoty po kursie z daty opłacenia faktury
kwota_po_kursie_oplacenia = oblicz_kwote_po_kursie(kwota_z_faktury, kurs_oplacenia_faktury)

# Obliczanie różnicy kwoty
roznica_kwoty = round(kwota_po_kursie_oplacenia - kwota_po_kursie_wystawienia, 2)

print(f'Kwota po kursie z daty wystawienia faktury: {kwota_po_kursie_wystawienia}')
print(f'Kwota po kursie z daty opłacenia faktury: {kwota_po_kursie_oplacenia}')
print(f'Różnica kwotowa: {roznica_kwoty}')

# Zapisz wyniki do pliku
wyniki = f'''Data wystawienia faktury: {data_wystawienia_faktury}
Data opłacenia faktury: {data_oplacenia_faktury}
Kod waluty: {waluta}
Kurs na dzień wystawienia faktury: {kurs_wystawienia_faktury}
Kurs na dzień opłacenia faktury: {kurs_oplacenia_faktury}
Różnica kursowa między {data_wystawienia_faktury} a {data_oplacenia_faktury}: {roznica_kursow}
Kwota po kursie z daty wystawienia faktury: {kwota_po_kursie_wystawienia}
Kwota po kursie z daty opłacenia faktury: {kwota_po_kursie_oplacenia}
Różnica kwotowa: {roznica_kwoty}
'''

# Zapisz wyniki do pliku
zapisz_do_pliku(wyniki)
