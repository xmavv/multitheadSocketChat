# MULTITHREAD CHAT WITH SOCKETS

- [Opis problemu](#opis-problemu)
- [Instrukcje uruchomienia projektu](#instrukcje-uruchomienia-projektu)
    - [uruchomienie projektu](#uruchomienie-projektu)
- [Czym są wątki i co reprezentują](#czym-są-wątki-i-co-reprezentują)
- [Sekcje krytyczne i ich rozwiązanie](#sekcje-krytyczne-i-ich-rozwiązanie)

## Opis problemu
problemik polega na zaimplementowaniu najprostszego chatu, wykorzystujac watki oraz gniazda(sockety :D)
- serwer ustawia socket na ktorym lacza sie clienci
- serwer przechowuje sockety clientow i za kazdym razem tworzy nowy watek clieta
- kazdy client moze wlaczyc sie do chatu za pomoca swojego socketa i porozumiewac sie z innymi clientami
- clienci widza swoje wiadomosci na ogolnodostepnym chacie

obsluga socketow serwera i clienta zostala zaimplementowana przy pomocy artykulu https://realpython.com/python-sockets/

## Instrukcje uruchomienia projektu

#### uruchomienie projektu
w sciezce projektu 

```python server.py```
```python client.py```
add as many clients as u wish...

gdzie argument to ilosc filozofow


## Czym są wątki i co reprezentują
### w przypadku serwera: 

- watki to nasi klienci, poniewaz dzialaja w tym samym czasie i chca sie porozumiewac na chacie
- serwer przechowuje liste wszystkich socketow clientow, tak aby moc wyslac wszystkim wiadomosc, gdy od ktoregokolwiek z clientow przyjdzie wiadomosc do serwera
- serwer w nieskonczonej petli czeka na nowe polaczenie, po czym startuje nowy watek
- kazdy watek (socket) czeka na wiadomosc do serwera i gdy takowa dostanie, wysyla ja do wszystkich clientow

### w przypadku clienta:

- kazdy client ma dwa watki: do wysylania wiadomosc, oraz do odbierania wiadomosci, to musi byc zrobione w taki sposob, poniewaz wczesniej w kodzie widnialo cos takiego:

```python
message = input()
s.sendall(message.encode())
data = s.recv(1024)
print(data)
```

wowczas client nie dostawal wiadomosci od serwera przed tym jak jej nie wyslal (synchroniczne dzialanie), co nie jest naszym chcianym rozwiazaniem, my chcemy aby client mogl otrzymac wiadomosc (w mniemaniu od innego clienta) nie patrzac na to czy wczesniej wyslal jakis komunikat

## Sekcje krytyczne i ich rozwiązanie
### w przypadku serwera: 

- sekcja krytyczna moze wystapic w przypadku jednoczesnego wpisywania nowego socketu do listy `clients` oraz wysylania wiadomosci do wszystkich socketow z listy `clients`

w tym celu stworzono mutex `clients_mutex`, ktory blokuje dostep do tej zmiennej przy dodawaniu nowego socketa oraz przy wysylaniu wiadomosci

### w przypadku clienta:
- wychodzi na to ze socket ma dwa osobne buffery dla wysylania i odbierania, wiec nie ma tutaj mowy o sekcji krytycznej