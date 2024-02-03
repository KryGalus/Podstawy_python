Program służy do obliczania różnicy kurs walut. Program napisany jest w języku Python i w celu ustalenia kursów walut korzysta z api NBP.
Program wysyła zapytania do api i pobiera kursy walut z dni podanych przez użytkownika.
Program pobiera od użytkownika date wystawienia faktury (rrrr-mm-dd), date opłacenia faktury (rrrr-mm-dd), walute (EUR,GBP,USD) oraz kwote znajdującą się na fakturze.
Sposób użycia:
Program na początku zapyta o podanie daty wystawienia faktury,
następnie o date jej opłacenia,
potem o walute,
na koniec zapyta o kwotę z faktury.
Wynik:
Program pokaże podane przez użytkownika dane, kursy walut obowiązujące w dniach podanych przez użytkownika oraz różnice kursową i kwotę pozostałą do zapłaty, ew. nadpłate.
W przypadku podania błędnej daty bądź waluty program poinformuje użytkownika.