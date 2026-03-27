# Chapter 9.9: Rizeni pristupu

[Domu](../README.md) | [<< Predchozi: Ladeni vykonu](08-performance.md) | [Dalsi: Sprava modu >>](10-mod-management.md)

---

> **Shrnuti:** Nakonfigurujte, kdo se muze pripojit k vasemu serveru DayZ, jak funguji bany, jak povolit vzdalenousspravu a jak overovani podpisu modu zabranuje neoprávnenemu obsahu. Tato kapitola pokryva kazdy mechanismus rizeni pristupu dostupný operatorovi serveru.

---

## Obsah

- [Adminsky pristup pres serverDZ.cfg](#adminsky-pristup-pres-serverdzcfg)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [BattlEye anti-cheat](#battleye-anti-cheat)
- [RCON (vzdálena konzole)](#rcon-vzdalena-konzole)
- [Overovani podpisu](#overovani-podpisu)
- [Adresar keys/](#adresar-keys)
- [Adminske nastroje ve hre](#adminske-nastroje-ve-hre)
- [Caste chyby](#caste-chyby)

---

## Adminsky pristup pres serverDZ.cfg

Parametr `passwordAdmin` v **serverDZ.cfg** nastavuje adminské heslo pro vas server:

```cpp
passwordAdmin = "YourSecretPassword";
```

Toto heslo pouzivate dvema zpusoby:

1. **Ve hre** -- otevrte chat a napiste `#login YourSecretPassword` pro ziskani adminskych opravneni pro tuto session.
2. **RCON** -- pripojte se pomoci BattlEye RCON klienta s timto heslem (viz sekce RCON nize).

Udrzujte adminské heslo dlouhé a jedinecne. Kdokoliv s nim ma plnou kontrolu nad bezicim serverem.

---

## ban.txt

Soubor **ban.txt** se nachazi v adresari profilu vaseho serveru (cesta, kterou nastavite s `-profiles=`). Obsahuje jedno SteamID64 na radek:

```
76561198012345678
76561198087654321
```

- Kazdy radek je ciste 17mistne SteamID64 -- zadna jmena, zadne komentare, zadna hesla.
- Hracum, jejichz SteamID se v tomto souboru objevi, je odmitnuto pripojeni.
- Soubor muzete upravovat behem behu serveru; zmeny se projevi pri dalsim pokusu o pripojeni.

---

## whitelist.txt

Soubor **whitelist.txt** se nachazi ve stejnem adresari profilu. Kdyz povolite whitelist, pripojit se mohou pouze SteamID uvedena v tomto souboru:

```
76561198012345678
76561198087654321
```

Format je identicky s **ban.txt** -- jedno SteamID64 na radek, nic dalsiho.

Whitelist je uzitecny pro privatni komunity, testovaci servery nebo udalosti, kde potrebujete kontrolovany seznam hracu.

---

## BattlEye anti-cheat

BattlEye je system proti podvodům integrovany do DayZ. Jeho soubory se nachazi ve slozce `BattlEye/` uvnitr adresare vaseho serveru:

| Soubor | Ucel |
|------|---------|
| **BEServer_x64.dll** | Binarni soubor enginu BattlEye anti-cheat |
| **beserver_x64.cfg** | Konfiguracni soubor (RCON port, RCON heslo) |
| **bans.txt** | BattlEye-specificke bany (zalozene na GUID, ne SteamID) |

BattlEye je ve vychozim stavu povoleny. Server spustite s `DayZServer_x64.exe` a BattlEye se nacte automaticky. Pro explicitni zakazani (nedoporuceno pro produkci) pouzijte spousteci parametr `-noBE`.

Soubor **bans.txt** ve slozce `BattlEye/` pouziva BattlEye GUID, ktere se lisi od SteamID64. Bany vydane pres RCON nebo prikazy BattlEye se do tohoto souboru zapisuji automaticky.

---

## RCON (vzdálena konzole)

BattlEye RCON vam umoznuje spravovat server na dalku bez nutnosti byt ve hre. Nakonfigurujte jej v `BattlEye/beserver_x64.cfg`:

```
RConPassword yourpassword
RConPort 2306
```

Vychozi port RCON je vas herní port plus 4. Pokud server bezi na portu `2302`, RCON ma vychozi hodnotu `2306`.

### Dostupne prikazy RCON

| Prikaz | Efekt |
|---------|--------|
| `kick <hrac> [duvod]` | Vykopne hrace ze serveru |
| `ban <hrac> [minuty] [duvod]` | Zablokuje hrace (zapise do BattlEye bans.txt) |
| `say -1 <zprava>` | Vysila zpravu vsem hracum |
| `#shutdown` | Radné vypnuti serveru |
| `#lock` | Zamkne server (zadna nova pripojeni) |
| `#unlock` | Odemkne server |
| `players` | Vypise pripojene hrace |

K RCON se pripojujete pomoci BattlEye RCON klienta (existuje nekolik bezplatnych nastroju). Pripojeni vyzaduje IP, RCON port a heslo z **beserver_x64.cfg**.

---

## Overovani podpisu

Parametr `verifySignatures` v **serverDZ.cfg** ridi, zda server kontroluje podpisy modu:

```cpp
verifySignatures = 2;
```

| Hodnota | Chovani |
|-------|----------|
| `0` | Zakazano -- kdokoliv se muze pripojit s jakymkoliv mody, zadne kontroly podpisu |
| `2` | Uplne overeni -- klienti musi mit platne podpisy pro vsechny nactene mody (vychozi) |

Na produkcnich serverech vzdy pouzijte `verifySignatures = 2`. Nastaveni na `0` umoznuje hracum pripojit se s upravenymi nebo nepodepsanymi mody, coz je vazne bezpecnostni riziko.

---

## Adresar keys/

Adresar `keys/` v koreni vaseho serveru obsahuje soubory **.bikey**. Kazdy `.bikey` odpovida modu a rika serveru "podpisy tohoto modu jsou duveryhhodne."

Kdyz je `verifySignatures = 2`:

1. Server kontroluje kazdy mod, ktery pripojujici se klient ma nacteny.
2. Pro kazdy mod server hleda odpovidajici `.bikey` v `keys/`.
3. Pokud odpovidajici klic chybi, hrac je vykopnut.

Kazdy mod, ktery nainstalujete na server, obsahuje soubor `.bikey` (obvykle ve slozce `Keys/` nebo `Key/` modu). Tento soubor zkopirujete do adresare `keys/` vaseho serveru.

```
DayZServer/
├── keys/
│   ├── dayz.bikey              ← vanilka (vzdy pritomen)
│   ├── MyMod.bikey             ← zkopirovano z @MyMod/Keys/
│   └── AnotherMod.bikey        ← zkopirovano z @AnotherMod/Keys/
```

Pokud pridáte novy mod a zapomenete zkopirovat jeho `.bikey`, kazdy hrac se spustenym modem bude pri pripojeni vykopnut.

---

## Adminske nastroje ve hre

Po prihlaseni pomoci `#login <heslo>` v chatu ziskate pristup k adminskym nastrojum:

- **Seznam hracu** -- zobrazeni vsech pripojenych hracu s jejich SteamID.
- **Kick/ban** -- odstraneni nebo zablokovani hracu primo ze seznamu hracu.
- **Teleport** -- pouziti adminske mapy k teleportaci na jakoukoli pozici.
- **Adminsky log** -- log akcí hracu na strane serveru (zabití, pripojeni, odpojeni) zapisovany do souboru `*.ADM` v adresari profilu.
- **Volna kamera** -- odpojeni od vasi postavy a volny let po mape.

Tyto nastroje jsou vestaveny do vanilkove hry. Mody tretich stran (jako Community Online Tools) vyrazne rozsirují moznosti admina.

---

## Caste chyby

Toto jsou problemy, na ktere operatori serveru narazi nejcasteji:

| Chyba | Priznak | Reseni |
|---------|---------|-----|
| Chybejici `.bikey` v `keys/` | Hraci jsou pri pripojeni vykopnuti s chybou podpisu | Zkopirujte soubor `.bikey` modu do adresare `keys/` vaseho serveru |
| Umisteni jmen nebo hesel do **ban.txt** | Bany nefunguji; nahodne chyby | Pouzivejte pouze cisté hodnoty SteamID64, jednu na radek |
| Konflikt portu RCON | RCON klient se nemuze pripojit | Ujistete se, ze RCON port neni pouzivan jinou sluzbou; zkontrolujte pravidla firewallu |
| `verifySignatures = 0` v produkci | Kdokoliv se muze pripojit se zmenenymi mody | Nastavte na `2` na jakemkoliv verejnem serveru |
| Zapomenuti otevrit RCON port ve firewallu | RCON klient vyprsi casem | Otevrte UDP port RCON (vychozi 2306) ve vasem firewallu |
| Uprava **bans.txt** v `BattlEye/` se SteamID | Bany nefunguji | BattlEye **bans.txt** pouziva GUID, ne SteamID; pouzijte **ban.txt** v adresari profilu pro bany SteamID |

---

[Domu](../README.md) | [<< Predchozi: Ladeni vykonu](08-performance.md) | [Dalsi: Sprava modu >>](10-mod-management.md)
