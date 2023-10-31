USE AKCJE_STRAZY_POZARNEJ

BULK INSERT dbo.Akcje FROM 'C:\Studia\Hurtownie danych\data_generator\bulks\akcje2.bulk' WITH (FIELDTERMINATOR='|')

BULK INSERT dbo.Trasy FROM 'C:\Studia\Hurtownie danych\data_generator\bulks\trasy2.bulk' WITH (FIELDTERMINATOR='|')

BULK INSERT dbo.Przynaleznosc_do_trasy FROM 'C:\Studia\Hurtownie danych\data_generator\bulks\przy_do_tras2.bulk' WITH (FIELDTERMINATOR='|')

UPDATE Strazacy
SET Nazwisko = 'Grab'
WHere PESEL = 16535946067