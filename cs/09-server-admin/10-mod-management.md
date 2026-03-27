# Chapter 9.10: Sprava modu

[Domu](../README.md) | [<< Predchozi: Rizeni pristupu](09-access-control.md) | [Dalsi: Reseni problemu >>](11-troubleshooting.md)

---

> **Shrnuti:** Instalujte, konfigurujte a udrzujte mody tretich stran na dedickovanyem serveru DayZ. Pokryva spousteci parametry, stahovani z Workshopu, podpisove klice, poradi nacitani, mody pouze pro server vs. vyzadovane klientem, aktualizace a nejcastejsi chyby zpusobujici pady nebo vykopnuti hracu.

---

## Obsah

- [Jak se mody nacitaji](#jak-se-mody-nacitaji)
- [Format spousteciho parametru](#format-spousteciho-parametru)
- [Instalace modu z Workshopu](#instalace-modu-z-workshopu)
- [Klice modu (.bikey)](#klice-modu-bikey)
- [Poradi nacitani a zavislosti](#poradi-nacitani-a-zavislosti)
- [Mody pouze pro server vs. vyzadovane klientem](#mody-pouze-pro-server-vs-vyzadovane-klientem)
- [Aktualizace modu](#aktualizace-modu)
- [Reseni konfliktu modu](#reseni-konfliktu-modu)
- [Caste chyby](#caste-chyby)

---

## Jak se mody nacitaji

DayZ nacita mody pres spousteci parametr `-mod=`. Kazdy zaznam je cesta ke slozce obsahujici PBO soubory a `config.cpp`. Engine precte kazdy PBO v kazde slozce modu, registruje jeho tridy a skripty a potom pokracuje k dalsimu modu v seznamu.

Server a klient musi mit stejne mody v `-mod=`. Pokud server uvadi `@CF;@MyMod` a klient ma pouze `@CF`, pripojeni selze s nesouladem podpisu. Mody pouze pro server umistene v `-servermod=` jsou vyjimkou -- klienti je nikdy nepotrebuji.

---

## Format spousteciho parametru

Typicky spousteci prikaz modovaneho serveru:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Parametr | Ucel |
|-----------|---------|
| `-mod=` | Mody vyzadovane serverem i vsemi pripojujicimi se klienty |
| `-servermod=` | Mody pouze pro server (klienti je nepotrebuji) |

Pravidla:
- Cesty jsou **oddelene strednikem** bez mezer kolem stredniku
- Kazda cesta je relativni ke korenovemu adresari serveru (napr. `@CF` znamena `<koren_serveru>/@CF/`)
- Muzete pouzit absolutni cesty: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **Poradi je dulezite** -- zavislosti se musi objevit pred mody, ktere je potrebuji

---

## Instalace modu z Workshopu

### Krok 1: Stahnete mod

Pouzijte SteamCMD s **klientskym** App ID DayZ (221100) a Workshop ID modu:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login vase_uzivatelske_jmeno +workshop_download_item 221100 1559212036 +quit
```

Stazene soubory se ulozi do:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Krok 2: Vytvorte symlink nebo zkopirujte

Slozky Workshopu pouzivaji numericka ID, ktera jsou nepouzitelna v `-mod=`. Vytvorte pojmenovany symlink (doporuceno) nebo zkopirujte slozku:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Pouziti spojeni (junction) znamena, ze aktualizace pres SteamCMD se aplikuji automaticky -- zadne opetovne kopirovani neni potreba.

### Krok 3: Zkopirujte .bikey

Viz dalsi sekce.

---

## Klice modu (.bikey)

Kazdy podepsany mod obsahuje slozku `keys/` s jednim nebo vice soubory `.bikey`. Tyto soubory rikaji BattlEye, ktere podpisy PBO prijmout.

1. Otevrte slozku modu (napr. `@CF/keys/`)
2. Zkopirujte kazdy soubor `.bikey` do korenoveho adresare `keys/` serveru

```
DayZServer/
  keys/
    dayz.bikey              # Vanilka -- vzdy pritomen
    cf.bikey                # Zkopirovano z @CF/keys/
    vpp_admintools.bikey    # Zkopirovano z @VPPAdminTools/keys/
```

Bez spravneho klice kazdy hrac se spustenym modem dostane: **"Player kicked: Modified data"**.

---

## Poradi nacitani a zavislosti

Mody se nacitaji zleva doprava v parametru `-mod=`. Soubor `config.cpp` modu deklaruje sve zavislosti:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Pokud `MyMod` vyzaduje `CF`, pak `@CF` se musi objevit **pred** `@MyMod` ve spoustecim parametru:

```
-mod=@CF;@MyMod          ✓ spravne
-mod=@MyMod;@CF          ✗ pad nebo chybejici tridy
```

**Obecny vzor poradi nacitani:**

1. **Frameworkove mody** -- CF, Community-Online-Tools
2. **Knihovní mody** -- BuilderItems, jakykoliv sdileny balicek assetu
3. **Funkční mody** -- pridani map, zbrane, vozidla
4. **Zavisle mody** -- cokoliv, co uvadi vyse uvedene jako `requiredAddons`

Pokud si nejste jisti, zkontrolujte stranku Workshopu modu nebo dokumentaci. Vetsina autoru modu publikuje sve pozadovane poradi nacitani.

---

## Mody pouze pro server vs. vyzadovane klientem

| Parametr | Kdo to potrebuje | Typicke priklady |
|-----------|-------------|------------------|
| `-mod=` | Server + vsichni klienti | Zbrane, vozidla, mapy, mody UI, obleceni |
| `-servermod=` | Pouze server | Spravci ekonomiky, logovacinastroje, adminské backendy, planovaciskript |

Pravidlo je primocaré: pokud mod obsahuje **jakékoli** klientske skripty, layouty, textury nebo modely, musi jit do `-mod=`. Pokud pouze spousti serverovou logiku bez assetu, ktere klient nekdy pouziva, pouzijte `-servermod=`.

Umisteni modu pouze pro server do `-mod=` nutí kazdeho hrace jej stahnout. Umisteni modu vyzadovaneho klientem do `-servermod=` zpusobi chybejici textury, rozbité UI nebo chyby skriptu na klientu.

---

## Aktualizace modu

### Postup

1. **Zastavte server** -- aktualizace souboru behem behu serveru muze poskodit PBO
2. **Znovu stahnete** pres SteamCMD:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login vase_uzivatelske_jmeno +workshop_download_item 221100 <modID> +quit
   ```
3. **Zkopirujte aktualizovane soubory .bikey** -- autori modu obcas rotují sve podpisove klice. Vzdy zkopirujte cerstvý `.bikey` ze slozky `keys/` modu do adresare `keys/` serveru
4. **Restartujte server**

Pokud jste pouzili symlinky (spojeni), krok 2 aktualizuje soubory modu na miste. Pokud jste rucne kopirovali soubory, musite je zkopirovat znovu.

### Aktualizace na strane klienta

Hraci s odbérem modu na Steam Workshop dostávaji aktualizace automaticky. Pokud aktualizujete mod na serveru a hrac ma starou verzi, dostanou nesoulad podpisu a nemohou se pripojit, dokud se jejich klient neaktualizuje.

---

## Reseni konfliktu modu

### Zkontrolujte RPT log

Otevrte nejnovejsi soubor `.RPT` v `profiles/`. Hledejte:

- **"Cannot register"** -- kolize nazvu tridy mezi dvema mody
- **"Missing addons"** -- zavislost neni nactena (spatne poradi nacitani nebo chybejici mod)
- **"Signature verification failed"** -- nesoulad `.bikey` nebo chybejici klic

### Zkontrolujte log skriptu

Otevrte nejnovejsi `script_*.log` v `profiles/`. Hledejte:

- **"SCRIPT (E)"** radky -- chyby skriptu, casto zpusobene poradim nacitani nebo nesouladem verzi
- **"Definition of variable ... already exists"** -- dva mody definuji stejnou tridu

### Izolujte problem

Kdyz mate hodne modu a neco se rozbije, testujte inkrementalne:

1. Zacnete pouze s frameworkovymi mody (`@CF`)
2. Pridavejte jeden mod po druhem
3. Spustte a zkontrolujte logy po kazdem pridani
4. Mod, ktery zpusobuje chyby, je vinik

### Dva mody upravuji stejnou tridu

Pokud dva mody oba pouzivaji `modded class PlayerBase`, ten nacteny **posledni** (nejvice vpravo v `-mod=`) vyhraje. Jeho volani `super` retezi na verzi druheho modu. To obvykle funguje, ale pokud jeden mod prepise metodu bez volani `super`, zmeny druheho modu jsou ztraceny.

---

## Caste chyby

**Spatne poradi nacitani.** Server spadne nebo zapise "Missing addons", protoze zavislost jeste nebyla nactena. Reseni: presunte mod zavislosti drive v seznamu `-mod=`.

**Zapomenuti na `-servermod=` pro mody pouze pro server.** Hraci jsou nuceni stahnout mod, ktery nepotrebuji. Reseni: presunte mody pouze pro server z `-mod=` do `-servermod=`.

**Neaktualizace souboru `.bikey` po aktualizaci modu.** Hraci jsou vykopnuti s "Modified data", protoze klic serveru neodpovida novym podpisum PBO modu. Reseni: vzdy znovu zkopirujte soubory `.bikey` pri aktualizaci modu.

**Prebalovani PBO modu.** Prebaleni PBO souboru modu rozbije jeho digitalni podpis, zpusobi vykopnuti BattlEye pro kazdeho hrace a porusuje podminky vetsiny autoru modu. Nikdy neprezbalovejte mod, ktery jste nevytvorili.

**Michani cest Workshopu s mistnimi cestami.** Pouzivani surove numericke cesty Workshopu pro nekteré mody a pojmenovanych slozek pro jine zpusobuje zmatky pri aktualizaci. Vyberte si jeden pristup -- symlinky jsou nejcistejsi.

**Mezery v cestach modu.** Cesta jako `-mod=@My Mod` rozbije parsovani. Prejmennujte slozky modu, abyste se vyhnuli mezerám, nebo obalte cely parametr do uvozovek: `-mod="@My Mod;@CF"`.

**Zastaraly mod na serveru, aktualizovany na klientu (nebo naopak).** Nesoulad verze brani pripojeni. Udrzujte verze serveru a Workshopu synchronizovane. Aktualizujte vsechny mody a server ve stejnou dobu.

---

[Domu](../README.md) | [<< Predchozi: Rizeni pristupu](09-access-control.md) | [Dalsi: Reseni problemu >>](11-troubleshooting.md)
