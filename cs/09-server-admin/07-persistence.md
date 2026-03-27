# Chapter 9.7: Stav sveta a persistence

[Domu](../README.md) | [<< Predchozi: Spawnovani hracu](06-player-spawning.md) | [Dalsi: Ladeni vykonu >>](08-performance.md)

Persistence DayZ udrzuje svet nazivz mezi restarty. Pochopeni, jak funguje, vam umozni spravovat baze, planovat wipy a vyhnout se poskozeni dat.

## Obsah

- [Jak funguje persistence](#jak-funguje-persistence)
- [Adresar storage_1/](#adresar-storage_1)
- [Parametry persistence v globals.xml](#parametry-persistence-v-globalsxml)
- [System uzemni vlajky](#system-uzemni-vlajky)
- [Predmety hoarderu](#predmety-hoarderu)
- [Nastaveni persistence v cfggameplay.json](#nastaveni-persistence-v-cfggameplayjson)
- [Postupy wipu serveru](#postupy-wipu-serveru)
- [Strategie zalohovani](#strategie-zalohovani)
- [Caste chyby](#caste-chyby)

---

## Jak funguje persistence

DayZ uklada stav sveta do adresare `storage_1/` uvnitr slozky profilu vaseho serveru. Cyklus je primocarý:

1. Server periodicky uklada stav sveta (vychozi priblizne kazdych ~30 minut) a pri radnem vypnuti.
2. Pri restartu server nacte `storage_1/` a obnovi vsechny perzistentni objekty -- vozidla, baze, stany, sudy, inventare hracu.
3. Predmety bez persistence (vetsina lootu na zemi) jsou regenerovany Centralni ekonomikou pri kazdem restartu.

Pokud `storage_1/` neexistuje pri spusteni, server vytvori cisty svet bez dat hracu a bez postavenych struktur.

---

## Adresar storage_1/

Profil vaseho serveru obsahuje `storage_1/` s temito podadresari a soubory:

| Cesta | Obsah |
|------|----------|
| `data/` | Binarni soubory obsahujici svetove objekty -- casti bazi, umistene predmety, pozice vozidel |
| `players/` | Soubory **.save** pro kazdeho hrace indexovane podle SteamID64. Kazdy soubor uklada pozici, inventar, zdravi, stavove efekty |
| `snapshot/` | Snapshoty stavu sveta pouzivane behem operaci ukladani |
| `events.bin` / `events.xy` | Stav dynamickych udalosti -- sleduje lokace helikopterovych zricenin, pozice konvoju a dalsi spawnovane udalosti |

Slozka `data/` je hlavni cast persistence. Obsahuje serializovana data objektu, ktera server nacita pri startu k rekonstrukci sveta.

---

## Parametry persistence v globals.xml

Soubor **globals.xml** (ve slozce vasi mise) ridi casovace cisteni a chovani vlajek. Toto jsou hodnoty relevantni pro persistenci:

```xml
<!-- Obnoveni uzemni vlajky -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 dni (sekundy) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 dni (sekundy) -->

<!-- Casovace cisteni -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Vychozi cisteni (sekundy) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Mrtvé telo hrace: 1 hodina -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Mrtvé zvire: 20 minut -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Mrtvé zombie: 5,5 minuty -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Zniceny predmet: 5,5 minuty -->

<!-- Chovani cisteni -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Max predmetu vycistenych za cyklus -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Preskocit cisteni do 100 m od hrace -->
```

Hodnota `CleanupAvoidance` zabranuje serveru v despawnovani objektu blizko aktivnich hracu. Pokud je mrtvé telo do 100 metru od jakehokoliv hrace, zustane, dokud se hrac nepresune nebo se casovac neresetuje.

---

## System uzemni vlajky

Uzemni vlajky jsou jadrem persistence bazi v DayZ. Zde je, jak dve klicove hodnoty spolupracuji:

- **FlagRefreshFrequency** (`432000` sekund = 5 dni) -- Jak casto musite interagovat s vlajkou, abyste ji udrzeli aktivni. Prijdete k vlajce a pouzijte akci "Refresh".
- **FlagRefreshMaxDuration** (`3456000` sekund = 40 dni) -- Maximalni akumulovany cas ochrany. Kazda obnova prida az FlagRefreshFrequency casu, ale celkovy cas nemuze prekrocit tento strop.

Kdyz casovac vlajky vyprsi:

1. Sama vlajka se stane zpusobilou pro cisteni.
2. Vsechny casti stavby baze pripojene k teto vlajce ztrateji svou ochranu persistence.
3. V dalsim cyklu cisteni zacnou nechranene casti mizet.

Pokud snizite FlagRefreshFrequency, hraci musi navstevovat sve baze casteji. Pokud zvysite FlagRefreshMaxDuration, baze preziji dele mezi navstevami. Upravujte obe hodnoty spolecne tak, aby odpovidaly stylu hrani na vasem serveru.

---

## Predmety hoarderu

V **cfgspawnabletypes.xml** jsou urcite kontejnery oznaceny tagem `<hoarder/>`. To je oznacuje jako predmety schopne skladovani, ktere se pocitaji do limitu ulozneho prostoru na hrace v Centralni ekonomice.

Vanilkove predmety hoarderu jsou:

| Predmet | Typ |
|------|------|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Ulozne sudy |
| CarTent, LargeTent, MediumTent, PartyTent | Stany |
| SeaChest | Podvodni ulozny prostor |
| SmallProtectorCase | Maly zamykatelny kufrik |
| UndergroundStash | Zakopaná skrys |
| WoodenCrate | Craftova bedna |

Priklad z **cfgspawnabletypes.xml**:

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

Server sleduje, kolik predmetu hoarderu kazdy hrac umistil. Po dosazeni limitu nova umisteni bud selzou, nebo se nejstarsi predmet despawnuje (v zavislosti na konfiguraci serveru).

---

## Nastaveni persistence v cfggameplay.json

Soubor **cfggameplay.json** ve slozce vasi mise obsahuje nastaveni ovlivnujici odolnost bazi a kontejneru:

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Nastaveni | Vychozi | Efekt |
|---------|---------|--------|
| `disableBaseDamage` | `false` | Kdyz je `true`, casti stavby baze (zdi, brany, strazni veze) nemohou byt poskozeny. Tim se efektivne zakazuje rajdovani. |
| `disableContainerDamage` | `false` | Kdyz je `true`, ulozne kontejnery (stany, sudy, bedny) nemohou byt poskozeny. Predmety uvnitr zustanou v bezpeci. |

Nastaveni obou na `true` vytvari server prately k PvE, kde jsou baze a ulozny prostor neznicitelne. Vetsina PvP serveru nechava obe na `false`.

---

## Postupy wipu serveru

Mate ctyri typy wipu, kazdy cili na jinou cast `storage_1/`. **Vzdy zastavte server pred provedenim jakehokoliv wipu.**

### Uplny wipe

Smazte celou slozku `storage_1/`. Server vytvori cisty svet pri dalsim spusteni. Vsechny baze, vozidla, stany, data hracu a stav udalosti jsou pryc.

### Wipe ekonomiky (zachovat hrace)

Smazte `storage_1/data/`, ale ponechte `storage_1/players/` nedotknuty. Hraci si zachovaji sve postavy a inventare, ale vsechny umistene objekty (baze, stany, sudy, vozidla) jsou odstraneny.

### Wipe hracu (zachovat svet)

Smazte `storage_1/players/`. Vsechny postavy hracu se resetuji na cerstve spawny. Baze a umistene objekty zustanou ve svete.

### Reset pocasi / udalosti

Smazte `events.bin` nebo `events.xy` ze `storage_1/`. Tim se resetuji pozice dynamickych udalosti (helikopterove zriceniny, konvoje). Server vygeneruje nove lokace udalosti pri dalsim spusteni.

---

## Strategie zalohovani

Data persistence jsou po ztrate nenahraditelna. Dodrzujte tyto postupy:

- **Zalohujte pri zastavenem serveru.** Zkopirujte celou slozku `storage_1/` behem doby, kdy server neni spusten. Kopirovani za behu riskuje zachyceni castecneho nebo poskozeneho stavu.
- **Planujte zalohy pred restarty.** Pokud provozujete automaticke restarty (kazdych 4-6 hodin), pridejte krok zalohy do vaseho restartovacího skriptu, ktery zkopiruje `storage_1/` pred spustenim procesu serveru.
- **Uchovavejte vice generaci.** Rotujte zalohy, abyste meli alespon 3 nedavne kopie. Pokud je vase posledni zaloha poskozena, muzete se vratit k drive.
- **Ukladejte mimo stroj.** Kopirovani zaloh na oddelený disk nebo do cloudoveho uloziste. Selhani disku na stroji serveru odnese vase zalohy, pokud jsou na stejnem disku.

Minimalní zálohovací skript (spousten pred startem serveru):

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Caste chyby

Tyto se opakované objevuji v komunitach serverovych adminu:

| Chyba | Co se stane | Prevence |
|---------|-------------|------------|
| Smazani `storage_1/` behem behu serveru | Poskozeni dat. Server zapisuje do souboru, ktere jiz neexistuji, coz zpusobi pady nebo castecny stav pri dalsim spusteni. | Vzdy nejprve zastavte server. |
| Nezalohovani pred wipem | Pokud omylem smazete spatnou slozku nebo wipe selze, neni mozna obnova. | Zalohujte `storage_1/` pred kazdym wipem. |
| Zamena resetu pocasi s uplnym wipem | Smazani `events.xy` pouze resetuje pozice dynamickych udalosti. Neresetuje loot, baze ani hrace. | Vete, ktere soubory co ridi (viz tabulka adresare vyse). |
| Vlajka neobnovena vcas | Po 40 dnech (FlagRefreshMaxDuration) vlajka vyprsi a vsechny pripojene casti baze se stanou zpusobilymi pro cisteni. Hraci prijdou o celou bazi. | Pripomínejte hracum interval obnovy. Snizujte FlagRefreshMaxDuration na malo populovanych serverech. |
| Uprava globals.xml behem behu serveru | Zmeny se nepromitnou do restartu. Hure, server muze prepsat vase upravy pri vypnuti. | Upravujte konfiguracni soubory pouze pri zastavenem serveru. |

---

[Domu](../README.md) | [<< Predchozi: Spawnovani hracu](06-player-spawning.md) | [Dalsi: Ladeni vykonu >>](08-performance.md)
