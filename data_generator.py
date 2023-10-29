from datetime import datetime, timedelta

from faker import Faker
import random
from unidecode import unidecode

NUMBER_OF_EMPLOYEES = 100
NUMBER_OF_BUILDINGS = 5
NUMBER_OF_STREETS = 200
NUMBER_OF_EVENTS = 100
MIN_NUMBER_OF_STREETS = 20
MAX_NUMBER_OF_STREETS = 40

fake = Faker('pl_PL')

SEP = '|'


class Pracownik:
    def __init__(self) -> None:
        self.imie = unidecode(fake.first_name())
        self.nazwisko = unidecode(fake.last_name())
        self.pesel = fake.random_int(min=10 ** 10, max=(10 ** 11) - 1)
        self.plec = random.choice(["K", "M"])
        self.data_urodzenia = fake.date_of_birth(minimum_age=25, maximum_age=65)
        self.data_roz_prac = fake.date_of_birth(minimum_age=2, maximum_age=10)
        self.data_zak_prac = self.get_data_zak_prac

    @property
    def get_data_zak_prac(self):
        rand = random.randint(1, 10)
        if rand == 10:
            while True:
                rand_data = fake.date_of_birth(minimum_age=0, maximum_age=3)
                if rand_data > self.data_roz_prac:
                    return rand_data
        else:
            return ""

    def get_pesel(self) -> str:
        return self.pesel

    def __str__(self) -> str:
        return f"{self.imie}{SEP}{self.nazwisko}{SEP}{self.pesel}{SEP}{self.plec}{SEP}{self.data_urodzenia}{SEP}{self.data_roz_prac}{SEP}{self.data_zak_prac}"


class Kierowca:
    def __init__(self, pesel) -> None:
        self.pesel = pesel
        self.data_prawa_jazdy = fake.date_of_birth(minimum_age=25, maximum_age=65)
        self.kat = self.get_kat
        self.numer_prawa_jazdy = self.get_numer

    @property
    def get_numer(self) -> str:
        return f"{fake.random_int(min=10000, max=99999)}/{fake.random_int(min=10, max=99)}/{fake.random_int(min=1000, max=9999)}"

    @property
    def get_kat(self) -> list[bool]:
        while True:
            kats = [random.choice([1, 0]) for _ in range(4)]
            if any(kat == 1 for kat in kats):
                return kats

    def __str__(self) -> str:
        return f"{self.pesel}{SEP}{self.data_prawa_jazdy}{SEP}{self.get_kat[0]}{SEP}{self.get_kat[1]}{SEP}{self.get_kat[2]}{SEP}{self.get_kat[3]}{SEP}{self.numer_prawa_jazdy}"


class Remiza:
    def __init__(self, id_remizy) -> None:
        self.numer = id_remizy
        self.miejscowosc = random.choice(["Gdansk", "Gdynia", "Sopot", "Rumia", "Reda", "Wejherowo", "Kartuzy"])
        self.ulica = unidecode(fake.street_name())
        self.numer_budynku = fake.random_int(min=2, max=80)
        self.kod_pocztowy = f"{fake.random_int(min=10, max=99)}-{fake.random_int(min=100, max=999)}"

    def get_id(self) -> int:
        return self.numer

    def __str__(self) -> str:
        return f"{self.numer}{SEP}{self.miejscowosc}{SEP}{self.ulica}{SEP}{self.numer_budynku}{SEP}{self.kod_pocztowy}"


class Zespol:
    def __init__(self, id_zespolu) -> None:
        self.id = id_zespolu

    def __str__(self) -> str:
        return str(self.id)


class PrzyDoZespolu:
    def __init__(self, id_zespolu, id_remizy, pesel_pracownika) -> None:
        self.id_zespolu = id_zespolu
        self.id_remizy = id_remizy
        self.pesel_pracownika = pesel_pracownika

    def __str__(self) -> str:
        return f"{self.id_zespolu}{SEP}{self.id_remizy}{SEP}{self.pesel_pracownika}"


class Droga:
    def __init__(self) -> None:
        self.nazwa = unidecode(fake.street_name())
        self.miejscowosc = random.choice(["Gdansk", "Gdynia", "Sopot", "Rumia", "Reda", "Wejherowo", "Kartuzy"])

    def __str__(self) -> str:
        return f"{self.nazwa}{SEP}{self.miejscowosc}"


class Trasa:
    def __init__(self, id_trasy, data_roz, akcja) -> None:
        self.id = id_trasy
        self.dlugosc = fake.random_int(min=3, max=80)
        self.data_roz = self.get_data_roz(data_roz)
        self.data_zak = self.get_data_zak()
        self.numer_rej_pojazdu = self.get_numer_rej_pojazdu()
        self.akcja = akcja

    def get_numer_rej_pojazdu(self):
        #TODO z csv to wziac
        return unidecode(fake.street_name())[:2].upper() + fake.bothify("?????").upper()

    def get_data_roz(self, data_roz):
        deley_time = random.randint(100, 500)
        return data_roz + timedelta(seconds=deley_time)

    def get_data_zak(self):
        time_of_event = self.dlugosc * random.randint(40, 80)
        return self.data_roz + timedelta(seconds=time_of_event)

    def __str__(self) -> str:
        return f"{self.id}{SEP}{self.data_roz}{SEP}{self.data_zak}{SEP}{self.numer_rej_pojazdu}{SEP}{self.dlugosc}"


class PrzyDoTrasy:
    def __init__(self, id_trasy, nazwa, miejscowosc) -> None:
        self.id_trasy = id_trasy
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc

    def __str__(self) -> str:
        return f"{self.id_trasy}{SEP}{self.nazwa}{SEP}{self.miejscowosc}"
class Akcja:
    def __init__(self, nr_wezwania, numer, miejscowosc) -> None:
        self.nr_wezwania = nr_wezwania
        self.data_wez = fake.date_time_this_decade()
        self.ulica = numer
        self.numer = fake.random_int(min=3, max=80)
        self.miejscowosc = miejscowosc

    def __str__(self) -> str:
        return f"{self.nr_wezwania}{SEP}{self.data_wez}{SEP}{self.ulica}{SEP}{self.numer}{SEP}{self.miejscowosc}"


pracownicy = []
with open('pracownicy.bulk', 'w') as f:
    pass

with open('pracownicy.bulk', 'a') as f:
    for _ in range(NUMBER_OF_EMPLOYEES):
        pracownik = Pracownik()
        pracownicy.append(pracownik)
        f.write(pracownik.__str__() + '\n')

remizy = []
with open('remizy.bulk', 'w') as f:
    pass

with open('remizy.bulk', 'a') as f:
    for i in range(NUMBER_OF_BUILDINGS):
        remiza = Remiza(i + 1)
        remizy.append(remiza)
        f.write(remiza.__str__() + '\n')

przy_do_zespolu = []
with open('przy_do_zespolu.bulk', 'w') as f:
    pass

with open('przy_do_zespolu.bulk', 'a') as f:
    sizes_of_team = [4, 5, 6]
    size_of_team = None
    number_emp_in_team = 0
    id_remizy = 0
    for pracownik in pracownicy:
        if size_of_team is None or number_emp_in_team == size_of_team:
            number_emp_in_team = 0
            size_of_team = random.choice(sizes_of_team)
            id_remizy += 1
        zespol = PrzyDoZespolu(id_remizy, random.choice(remizy).get_id(), pracownik.get_pesel())
        przy_do_zespolu.append(zespol)
        number_emp_in_team += 1
        f.write(zespol.__str__() + '\n')

zespoly = []
with open('zespoly.bulk', 'w') as f:
    pass

with open('zespoly.bulk', 'a') as f:
    for i in range(przy_do_zespolu[-1].id_zespolu):
        zespol = Zespol(i + 1)
        zespoly.append(zespol)
        f.write(zespol.__str__() + '\n')

kierowcy = []
with open('kierowcy.bulk', 'w') as f:
    pass

old_team = 1
last_driver = ""
with open('kierowcy.bulk', 'a') as f:
    is_driver = False
    for zespol in przy_do_zespolu:
        if zespol.pesel_pracownika in kierowcy:
            is_driver = True
        if old_team != zespol.id_zespolu:
            old_team = zespol.id_zespolu
            if not is_driver:
                kierowca = Kierowca(last_driver)
                kierowcy.append(last_driver)
                f.write(kierowca.__str__() + '\n')
            is_driver = False

        last_driver = zespol.pesel_pracownika

drogi = []
with open('drogi.bulk', 'w') as f:
    pass

with open('drogi.bulk', 'a') as f:
    for _ in range(NUMBER_OF_STREETS):
        droga = Droga()
        drogi.append(droga)
        f.write(droga.__str__() + '\n')


akcje = []
with open('akcje.bulk', 'w') as f:
    pass

with open('akcje.bulk', 'a') as f:
    for i in range(NUMBER_OF_EVENTS):
        droga = random.choice(drogi)
        akcja = Akcja(i + 1, droga.nazwa, droga.miejscowosc)
        akcje.append(akcja)
        f.write(akcja.__str__() + '\n')



trasy = []
with open('trasy.bulk', 'w') as f:
    pass

with open('trasy.bulk', 'a') as f:
    for i in range(NUMBER_OF_STREETS):
        akcja = random.choice(akcje)
        trasa = Trasa(i+1, akcja.data_wez, akcja.nr_wezwania)
        trasy.append(trasa)
        f.write(trasa.__str__() + '\n')

przy_do_tras = []
with open('przy_do_tras.bulk', 'w') as f:
    pass

with open('przy_do_tras.bulk', 'a') as f:
    i = 1
    for _ in range(NUMBER_OF_STREETS):
        number_of_cars = [1,2,3]
        for trasa in trasy:
            cars = random.choice(number_of_cars)
            for _ in range(cars):
                number_of_streets = random.randint(MIN_NUMBER_OF_STREETS,MAX_NUMBER_OF_STREETS)
                tab_of_streets = []
                while len(tab_of_streets) < number_of_streets:
                    droga = random.choice(drogi)
                    if droga not in tab_of_streets:
                        tab_of_streets.append(droga)
                        przy_do_trasy = PrzyDoTrasy(i, droga.nazwa, droga.miejscowosc)
                        f.write(przy_do_trasy.__str__() + '\n')
                        i += 1