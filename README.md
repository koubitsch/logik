# Logik

Jedná se o zpracování známé hry logik,kde se hráči snaží uhodnout správnou kombinaci pěti barev.

## Spuštění

Před spuštěním je třeba mít nainstalovaný python a následně v adresáři tohoto projektu pomocí příkazového řádku spustit příkaz `pip install -r requirements.txt`.
Poté stačí hru spustit otevřením `logik.py`.

## Jak hrát

Hráč si může vybrat, zda chce hrát sám, nebo zda chce hrát proti počítači. V obou případech se hráč snaží uhodnout správnou kombinaci pěti barev. Po provedeném tipu se 
zobrazí určitý počet bílých a černých čar. Počet bílých čar udává počet správných barev, které jsou i na správném místě. Počet černých čar udává počet správných barev na špatném místě.
Barvy se v kombinacích mohou opakovat.
Při hře proti počítači se jedná o závod o to, kdo danou kombinaci uhodne jako první.

## Kód

Použil jsem modulů pygame. Samotný kód je strukturován do dvou souborů a to `logik.py` a `objekty.py`. `logik.py` obsahuje samotný cyklus hry a funkce, které mění globální proměnné a `objekty.py` 
obsahuje pomocné funkce a objekty, včetně mozku počítače.

## Počítač

Mozek počítače funguje tak, že má svůj seznam možných tipů, reprezentovaný boolovským seznamem o délce 8^5 (počet všech možných tipů). Seznam začíná plný True
Počítač ze seznamu náhodně vybere tip (ten co je True) a podle výsledku upraví svůj seznam možných tipů. Ty možné tipy, co by měli jiný výsledek s náhodně vybraným tipem, než je výsledek, změní na False.
To se opakuje než uhodne správnou kombinaci.