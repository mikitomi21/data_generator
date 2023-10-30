USE AKCJE_STRAZY_POZARNEJ

CREATE TABLE Akcje(
	Numer_wezwania char(10) PRIMARY KEY,
	Data_i_godzina_wezwania dateTime,
	Ulica varchar(50),
	Numer varChar(10),
	Miejscowosc varchar(50)
);
CREATE TABLE Strazacy(
	Imie varchar(50),
	Nazwisko varchar(50),
	PESEL char(11) PRIMARY KEY,
	P³eæ char(1) check(P³eæ in ('K', 'M')),
	Data_urodzenia date,
	Data_rozpoczecia_pracy date,
	Data_zakonczenia_pracy date NULL
);
CREATE TABLE Kierowcy(
	PESEL char(11) REFERENCES Strazacy(PESEL),
	Data_wydania_prawa_jazdy date,
	Prawo_jazdy_kat_B bit,
	Prawo_jazdy_kat_BE bit,
	Prawo_jazdy_kat_C bit,
	Prawo_jazdy_kat_CE bit,
	Numer_prawa_jazdy char(13) PRIMARY KEY
);
CREATE TABLE Remizy(
	Numer int,
	Miejscowosc varchar(50),
	Ulica varchar(50),
	Numer_budynku varchar(10),
	Kod_pocztowy char(50),
	PRIMARY KEY(Numer, Miejscowosc)
);
CREATE TABLE Zespoly(
	ID_zespolu int PRIMARY KEY,
	Numer int,
	Miejscowosc varchar(50),
	FOREIGN KEY(Numer, Miejscowosc) REFERENCES Remizy(Numer, Miejscowosc)
);
CREATE TABLE Trasy(
	ID int PRIMARY KEY,
	Data_i_godzina_rozpoczecia dateTime,
	Data_i_godizna_zakonczania dateTime,
	nr_rejestracyjny_samochodu VARCHAR(20) NOT NULL 
		CHECK(SUBSTRING(nr_rejestracyjny_samochodu, 1 ,1) in ('B','C','D','E','F','G','K','L','N','O','P','R','S','T','W','Z')),
	Dlugosc int,
	Numer_wezwania char(10) REFERENCES Akcje(Numer_wezwania),
	Numer_prawa_jazdy char(13) REFERENCES Kierowcy(Numer_prawa_jazdy),
	ID_zespolu int REFERENCES Zespoly(ID_zespolu)
	/*TO DO*/
);
CREATE TABLE Drogi(
	Nazwa varchar(50),
	Miejscowosc varchar(50),
	PRIMARY KEY(Nazwa, Miejscowosc)
);
CREATE TABLE Przynaleznosc_do_trasy(
	ID int REFERENCES Trasy(ID),
	Nazwa varchar(50),
	Miejscowosc varchar(50),
	FOREIGN KEY(Nazwa, Miejscowosc) REFERENCES DROGI(Nazwa, Miejscowosc),
	PRIMARY KEY(ID, Nazwa, Miejscowosc)
);



CREATE TABLE Przynaleznosc_do_zespolu(
	ID_zespolu int REFERENCES Zespoly(ID_zespolu),
	PESEL char(11) REFERENCES Strazacy(PESEL),
	PRIMARY KEY(ID_zespolu, PESEL)
);

