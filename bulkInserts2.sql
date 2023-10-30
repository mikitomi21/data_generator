USE AKCJE_STRAZY_POZARNEJ

BULK INSERT dbo.Akcje FROM 'D:\Studia\5\Hurtownie danych\data_generator\bulks\akcje2.bulk' WITH (FIELDTERMINATOR='|')

BULK INSERT dbo.Trasy FROM 'D:\Studia\5\Hurtownie danych\data_generator\bulks\trasy2.bulk' WITH (FIELDTERMINATOR='|')

BULK INSERT dbo.Przynaleznosc_do_trasy FROM 'D:\Studia\5\Hurtownie danych\data_generator\bulks\przy_do_tras2.bulk' WITH (FIELDTERMINATOR='|')