from datetime import datetime, timedelta

from faker import Faker
import random
from unidecode import unidecode
import os
import csv

NUMBER_OF_EMPLOYEES = 15
NUMBER_OF_BUILDINGS = 3
NUMBER_OF_STREETS = 50
NUMBER_OF_STREETS2 = 10
NUMBER_OF_EVENTS = 30
NUMBER_OF_EVENTS2 = 10
MIN_NUMBER_OF_STREETS = 10
MAX_NUMBER_OF_STREETS = 20

START_DATE = datetime(2010, 1, 1)
MIDDLE_DATE = datetime(2015, 1, 1)
END_DATE = datetime(2015, 6, 1)

fake = Faker("pl_PL")

SEP = "|"

os.chdir("bulks")


class Pracownik:
    def __init__(self) -> None:
        self.imie = unidecode(fake.first_name())
        self.nazwisko = unidecode(fake.last_name())
        self.pesel = fake.random_int(min=10**10, max=(10**11) - 1)
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
        self.miejscowosc = random.choice(
            ["Gdansk", "Gdynia", "Sopot", "Rumia", "Reda", "Wejherowo", "Kartuzy"]
        )
        self.ulica = unidecode(fake.street_name())
        self.numer_budynku = fake.random_int(min=2, max=80)
        self.kod_pocztowy = (
            f"{fake.random_int(min=10, max=99)}-{fake.random_int(min=100, max=999)}"
        )

    def get_id(self) -> int:
        return self.numer

    def __str__(self) -> str:
        return f"{self.numer}{SEP}{self.miejscowosc}{SEP}{self.ulica}{SEP}{self.numer_budynku}{SEP}{self.kod_pocztowy}"


class Zespol:
    def __init__(self, id_zespolu, id_remizy, miejscowosc) -> None:
        self.id = id_zespolu
        self.id_remizy = id_remizy
        self.miejscowosc = miejscowosc

    def __str__(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return f"{self.id}{SEP}{self.id_remizy}{SEP}{self.miejscowosc}"


class PrzyDoZespolu:
    def __init__(self, id_zespolu, id_remizy, pesel_pracownika) -> None:
        self.id_zespolu = id_zespolu
        # self.id_remizy = id_remizy
        self.pesel_pracownika = pesel_pracownika

    def __str__(self) -> str:
        return f"{self.id_zespolu}{SEP}{self.pesel_pracownika}"


class Droga:
    def __init__(self) -> None:
        self.nazwa = unidecode(fake.street_name())
        self.miejscowosc = random.choice(
            ["Gdansk", "Gdynia", "Sopot", "Rumia", "Reda", "Wejherowo", "Kartuzy"]
        )

    def __str__(self) -> str:
        return f"{self.nazwa}{SEP}{self.miejscowosc}"


class Trasa:
    def __init__(self, id_trasy, data_roz, akcja, id_zespolu, kierowca) -> None:
        self.id = id_trasy
        self.dlugosc = fake.random_int(min=3, max=80)
        self.data_roz = self.get_data_roz(data_roz)
        self.data_zak = self.get_data_zak()
        self.numer_rej_pojazdu = self.get_numer_rej_pojazdu()
        self.akcja = akcja
        self.id_zespolu = id_zespolu
        self.kierowca = kierowca

    def get_numer_rej_pojazdu(self):
        # TODO z csv to wziac
        return unidecode(fake.street_name())[:2].upper() + fake.bothify("?????").upper()

    def get_data_roz(self, data_roz):
        deley_time = random.randint(100, 500)
        return data_roz + timedelta(seconds=deley_time)

    def get_data_zak(self):
        time_of_event = self.dlugosc * random.randint(40, 80)
        return self.data_roz + timedelta(seconds=time_of_event)

    def __str__(self) -> str:
        return f"{self.id}{SEP}{self.data_roz}{SEP}{self.data_zak}{SEP}{self.numer_rej_pojazdu}{SEP}{self.dlugosc}{SEP}{self.akcja}{SEP}{self.kierowca}{SEP}{self.id_zespolu}"


class PrzyDoTrasy:
    def __init__(self, id_trasy, nazwa, miejscowosc) -> None:
        self.id_trasy = id_trasy
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc

    def __str__(self) -> str:
        return f"{self.id_trasy}{SEP}{self.nazwa}{SEP}{self.miejscowosc}"


class Akcja:
    def __init__(self, nr_wezwania, numer, miejscowosc, start_date, end_date) -> None:
        self.nr_wezwania = nr_wezwania
        self.data_wez = fake.date_time_between_dates(start_date, end_date)
        self.ulica = numer
        self.numer = fake.random_int(min=3, max=80)
        self.miejscowosc = miejscowosc

    def get_data_wez(self, etap):
        if etap == START_DATE:
            return

    def __str__(self) -> str:
        return f"{self.nr_wezwania}{SEP}{self.data_wez}{SEP}{self.ulica}{SEP}{self.numer}{SEP}{self.miejscowosc}"


class Pojazd:
    def __init__(self, nr_wezwania) -> None:
        self.nr_wezwania = nr_wezwania
        self.marka = fake.random_element(
            elements=("Ford", "Toyota", "Volkswagen", "BMW", "Audi")
        )
        self.pojemnosc = fake.random_element(
            elements=("1.0", "1.2", "1.5", "2.0", "2.5")
        )
        self.moc = fake.random_int(min=50, max=400)
        self.rok = fake.random_int(min=1990, max=2023)
        self.masa = fake.random_int(min=50, max=500)
        self.dop_masa = fake.random_int(min=1000, max=3000)
        self.roz_osi = fake.random_int(min=2500, max=3500)
        self.wysokosc = fake.random_int(min=1400, max=2000)
        self.poj_wodny = fake.random_element(
            elements=("Diesel", "Benzyna", "LPG", "Elektryczny")
        )
        self.ilosc_drzwi = fake.random_element(elements=(2, 4, 5))

    def to_tab(self):
        return [
            self.nr_wezwania,
            self.marka,
            self.pojemnosc,
            self.moc,
            self.rok,
            self.masa,
            self.dop_masa,
            self.roz_osi,
            self.wysokosc,
            self.poj_wodny,
            self.ilosc_drzwi,
        ]


pracownicy = []
with open("Strazacy.bulk", "w") as f:
    pass

with open("Strazacy.bulk", "a") as f:
    for _ in range(NUMBER_OF_EMPLOYEES):
        pracownik = Pracownik()
        pracownicy.append(pracownik)
        f.write(pracownik.__str__() + "\n")

remizy = []
with open("Remizy.bulk", "w") as f:
    pass

with open("Remizy.bulk", "a") as f:
    for i in range(NUMBER_OF_BUILDINGS):
        remiza = Remiza(i + 1)
        remizy.append(remiza)
        f.write(remiza.__str__() + "\n")

przy_do_zespolu = []
with open("Przynaleznosc_do_zespolu.bulk", "w") as f:
    pass

with open("Przynaleznosc_do_zespolu.bulk", "a") as f:
    sizes_of_team = [4, 5, 6]
    size_of_team = None
    number_emp_in_team = 0
    id_remizy = 0
    for pracownik in pracownicy:
        if size_of_team is None or number_emp_in_team == size_of_team:
            number_emp_in_team = 0
            size_of_team = random.choice(sizes_of_team)
            id_remizy += 1
        zespol = PrzyDoZespolu(
            id_remizy, random.choice(remizy).get_id(), pracownik.get_pesel()
        )
        przy_do_zespolu.append(zespol)
        number_emp_in_team += 1
        f.write(zespol.__str__() + "\n")

zespoly = []
with open("Zespoly.bulk", "w") as f:
    pass

with open("Zespoly.bulk", "a") as f:
    for i in range(przy_do_zespolu[-1].id_zespolu):
        zespol = Zespol(
            i + 1,
            random.choice(remizy).numer,
            random.choice(
                ["Gdansk", "Gdynia", "Sopot", "Rumia", "Reda", "Wejherowo", "Kartuzy"]
            ),
        )
        zespoly.append(zespol)
        f.write(zespol.__str__() + "\n")

kierowcy = []
with open("Kierowcy.bulk", "w") as f:
    pass

old_team = 1
last_driver = ""
with open("Kierowcy.bulk", "a") as f:
    is_driver = False
    for zespol in przy_do_zespolu:
        if zespol.pesel_pracownika in kierowcy:
            is_driver = True
        if old_team != zespol.id_zespolu:
            old_team = zespol.id_zespolu
            if not is_driver:
                kierowca = Kierowca(last_driver)
                kierowcy.append(kierowca)
                f.write(kierowca.__str__() + "\n")
            is_driver = False

        last_driver = zespol.pesel_pracownika

drogi = []
with open("Drogi.bulk", "w") as f:
    pass

with open("Drogi.bulk", "a") as f:
    for _ in range(NUMBER_OF_STREETS):
        droga = Droga()
        if not any(
            droga.nazwa == i.nazwa and droga.miejscowosc == i.miejscowosc for i in drogi
        ):
            drogi.append(droga)
            f.write(droga.__str__() + "\n")


akcje = []
with open("Akcje.bulk", "w") as f:
    pass

with open("Akcje.bulk", "a") as f:
    for i in range(NUMBER_OF_EVENTS):
        droga = random.choice(drogi)
        akcja = Akcja(i + 1, droga.nazwa, droga.miejscowosc, START_DATE, MIDDLE_DATE)
        akcje.append(akcja)
        f.write(akcja.__str__() + "\n")

akcje2 = []
with open("akcje2.bulk", "w") as f:
    pass

with open("akcje2.bulk", "a") as f:
    for i in range(NUMBER_OF_EVENTS, NUMBER_OF_EVENTS2 + NUMBER_OF_EVENTS):
        droga = random.choice(drogi)
        akcja = Akcja(i + 1, droga.nazwa, droga.miejscowosc, MIDDLE_DATE, END_DATE)
        akcje2.append(akcja)
        f.write(akcja.__str__() + "\n")


trasy = []
with open("Trasy.bulk", "w") as f:
    pass

with open("Trasy.bulk", "a") as f:
    number_of_cars = [1,2,3]
    j = 1
    for i in range(NUMBER_OF_STREETS):
        akcja = random.choice(akcje)
        zespol = random.choice(zespoly)
        pesele_kierowcow = [kierowca.pesel for kierowca in kierowcy]
        trasa = None
        cars = random.choice(number_of_cars)
        send_team = []
        for car in range(cars):
            for polaczenia in przy_do_zespolu:
                if (
                    polaczenia.id_zespolu == zespol.id
                    and polaczenia.pesel_pracownika in pesele_kierowcow
                    and (polaczenia.id_zespolu not in [i[0] for i in send_team]
                    or polaczenia.pesel_pracownika not in [i[1] for i in send_team])
                ):
                    numer_prawo_jazdy = next(
                        (
                            kierowca.numer_prawa_jazdy
                            for kierowca in kierowcy
                            if kierowca.pesel == polaczenia.pesel_pracownika
                        ),
                        "",
                    )
                    trasa = Trasa(
                        j,
                        akcja.data_wez,
                        akcja.nr_wezwania,
                        zespol.id,
                        numer_prawo_jazdy,
                    )
                    j+=1
                    trasy.append(trasa)
                    send_team.append((zespol.id, numer_prawo_jazdy))
                    f.write(trasa.__str__() + "\n")


trasy2 = []
with open("Trasy2.bulk", "w") as f:
    pass

with open("Trasy2.bulk", "a") as f:
    number_of_cars = [1, 2, 3]
    j = max(trasa.id for trasa in trasy)+1
    for i in range(NUMBER_OF_STREETS, NUMBER_OF_STREETS2+NUMBER_OF_STREETS):
        akcja = random.choice(akcje)
        zespol = random.choice(zespoly)
        pesele_kierowcow = [kierowca.pesel for kierowca in kierowcy]
        trasa = None
        cars = random.choice(number_of_cars)
        send_team = []
        for car in range(cars):
            for polaczenia in przy_do_zespolu:
                if (
                        polaczenia.id_zespolu == zespol.id
                        and polaczenia.pesel_pracownika in pesele_kierowcow
                        and (polaczenia.id_zespolu not in [i[0] for i in send_team]
                             or polaczenia.pesel_pracownika not in [i[1] for i in send_team])
                ):
                    numer_prawo_jazdy = next(
                        (
                            kierowca.numer_prawa_jazdy
                            for kierowca in kierowcy
                            if kierowca.pesel == polaczenia.pesel_pracownika
                        ),
                        "",
                    )
                    trasa = Trasa(
                        j,
                        akcja.data_wez,
                        akcja.nr_wezwania,
                        zespol.id,
                        numer_prawo_jazdy,
                    )
                    j += 1
                    trasy2.append(trasa)
                    send_team.append((zespol.id, numer_prawo_jazdy))
                    f.write(trasa.__str__() + "\n")


with open("Przynaleznosc_do_trasy.bulk", "w") as f:
    pass

with open("Przynaleznosc_do_trasy.bulk", "a") as f:
    for trasa in trasy:
        number_of_streets = random.randint(
            MIN_NUMBER_OF_STREETS, MAX_NUMBER_OF_STREETS
        )
        tab_of_streets = []
        while len(tab_of_streets) < number_of_streets:
            droga = random.choice(drogi)
            if (droga.nazwa, droga.miejscowosc) not in tab_of_streets:
                tab_of_streets.append((droga.nazwa, droga.miejscowosc))
                przy_do_trasy = PrzyDoTrasy(
                    trasa.id, droga.nazwa, droga.miejscowosc
                )
                f.write(przy_do_trasy.__str__() + "\n")

with open("Przy_do_tras2.bulk", "w") as f:
    pass

with open("Przy_do_tras2.bulk", "a") as f:
    for trasa in trasy2:
        number_of_streets = random.randint(
            MIN_NUMBER_OF_STREETS, MAX_NUMBER_OF_STREETS
        )
        tab_of_streets = []
        while len(tab_of_streets) < number_of_streets:
            droga = random.choice(drogi)
            if (droga.nazwa, droga.miejscowosc) not in tab_of_streets:
                tab_of_streets.append((droga.nazwa, droga.miejscowosc))
                przy_do_trasy = PrzyDoTrasy(
                    trasa.id, droga.nazwa, droga.miejscowosc
                )
                f.write(przy_do_trasy.__str__() + "\n")

with open("Pojazdy.csv", "w") as f:
    pass

with open("Pojazdy.csv", "a") as f:
    writer = csv.writer(f)
    headers = [
        "Numer rejestracyjny pojazdu",
        "Marka pojazdu",
        "Pojemnosc skokowa silnika",
        "Moc silnika",
        "Rok produkcji",
        "Masa wlasna",
        "Dopuszczalna masa calkowita",
        "Rozstaw osi",
        "Wysokosc",
        "Pojemnosc zbiornika wody",
        "Ilosc drzwi",
    ]
    writer.writerow(headers)

    pojazdy = list(
        set(
            [trasa.numer_rej_pojazdu for trasa in trasy]
            + [trasa.numer_rej_pojazdu for trasa in trasy2]
        )
    )
    for pojazdId in pojazdy:
        pojazd = Pojazd(pojazdId)
        writer.writerow(pojazd.to_tab())
