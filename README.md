## Informacje
Celem aplikacji jest umożliwienie szkołom prowadzenia kształcenia zdalnego. Aplikacja będzie składać się z widoku strony głównej, strony z kursami, profilu użytkownika, szczegółów danego kursu, chatu oraz niezbędnych formularzy interaktywnych. Użytkownicy będą mieli możliwość założenia konta, po czym administrator przydziela ich do odpowiednich grup - nauczyciel lub student. Nauczyciel będzie miał możliwość tworzenia swoich kursów do których będą zapisywać się studenci. następnie w kursie będzie mógł dodawać/edytować tematy, jego opis co należy zrobić, pliki pomocnicze oraz same zadania do wykonania. Jeśli student prześle rozwiązanie zadania, bedzie rowniez mozliwosc jego ocenienia przez nauczyciela. Student zapisuje się tylko raz do danego kursu (pozniej bedzie mogl wchodzic bez podawania hasła), a następnie bedzie mogl wykonywac zadania zamieszczone przez nauczyciela. Wszyscy uzykownicy beda mieli mozliwosc wysylania wiadomosci do siebie za pośrednictwem chatu.

## Setup
```
$ pip install virtualenv
$ python -m venv [nazwa]
$ .\\[nazwa]\Scripts\activate.bat
$ pip install -r requirements.txt
```

## ENV
```
DB_NAME=[nazwa bazy danych]
DB_USER=[nazwa uzytkownika bazy danych]
DB_PASSWORD=[haslo do bazy danych]
DB_HOST=[host bazy]
DB_PORT=[port]
C_PRI_K=[prywatny klucz captcha]
C_PUB_K=[publiczny klucz captcha]
EMAIL_U=[email]
EMAIL_P=[haslo do email'a]
```

## Autorzy
* Gabriel Charkiewicz
* Kamil Mieczkowski
* Jakub Laskowski

## Wygląd
![image](https://github.com/kejden/szkieletowe-projekt/assets/108090061/21265910-215e-47e4-a9ec-dfc4ff575f39)
![image](https://github.com/kejden/szkieletowe-projekt/assets/108090061/12863363-9298-4aa3-8eb0-1f79a20a3026)
![image](https://github.com/kejden/szkieletowe-projekt/assets/108090061/a1b9971c-27ac-4466-9186-b32d9feae1e3)
![image](https://github.com/kejden/szkieletowe-projekt/assets/108090061/304a9a02-fad3-4295-9393-27608025461c)
![image](https://github.com/kejden/szkieletowe-projekt/assets/108090061/ed576a94-759d-467a-9b8d-5b3c5dd0b961)




