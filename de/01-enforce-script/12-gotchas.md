# Kapitel 1.12: Was NICHT existiert (Fallstricke)

[Startseite](../../README.md) | [<< Zurueck: Fehlerbehandlung](11-error-handling.md) | **Fallstricke** | [Weiter: Funktionen & Methoden >>](13-functions-methods.md)

---

## Inhaltsverzeichnis

- [Vollstaendige Fallstrick-Referenz](#vollstaendige-fallstrick-referenz)
  1. [Kein ternaerer Operator](#1-kein-ternaerer-operator)
  2. [Keine do...while-Schleife](#2-keine-dowhile-schleife)
  3. [Kein try/catch/throw](#3-kein-trycatchthrow)
  4. [Keine Mehrfachvererbung](#4-keine-mehrfachvererbung)
  5. [Kein Operator-Overloading (ausser Index)](#5-kein-operator-overloading-ausser-index)
  6. [Keine Lambdas / anonymen Funktionen](#6-keine-lambdas--anonymen-funktionen)
  7. [Keine Delegates / Funktionszeiger (nativ)](#7-keine-delegates--funktionszeiger-nativ)
  8. [Kein String-Escape fuer Backslash/Anfuehrungszeichen](#8-kein-string-escape-fuer-backslashanfuehrungszeichen)
  9. [Keine Variablen-Neudeklaration in else-if-Bloecken](#9-keine-variablen-neudeklaration-in-else-if-bloecken)
  10. [Kein Ternaer in Variablendeklaration](#10-kein-ternaer-in-variablendeklaration)
  11. [Object.IsAlive() existiert NICHT auf Basis-Object](#11-objectisalive-existiert-nicht-auf-basis-object)
  12. [Kein nullptr — verwenden Sie NULL oder null](#12-kein-nullptr--verwenden-sie-null-oder-null)
  13. [switch/case hat KEIN Fall-Through](#13-switchcase-hat-kein-fall-through)
  14. [Keine Standard-Parameter-Ausdruecke](#14-keine-standard-parameter-ausdruecke)
  15. [JsonFileLoader.JsonLoadFile gibt void zurueck](#15-jsonfileloaderjsonloadfile-gibt-void-zurueck)
  16. [Kein #define-Wert-Substitution](#16-kein-define-wert-substitution)
  17. [Keine Interfaces / abstrakte Klassen (erzwungen)](#17-keine-interfaces--abstrakte-klassen-erzwungen)
  18. [Keine Generics-Einschraenkungen](#18-keine-generics-einschraenkungen)
  19. [Keine Enum-Validierung](#19-keine-enum-validierung)
  20. [Keine variadischen Parameter](#20-keine-variadischen-parameter)
  21. [Keine verschachtelten Klassendeklarationen](#21-keine-verschachtelten-klassendeklarationen)
  22. [Statische Arrays haben feste Groesse](#22-statische-arrays-haben-feste-groesse)
  23. [array.Remove ist unsortiert](#23-arrayremove-ist-unsortiert)
  24. [Kein #include — alles via config.cpp](#24-kein-include--alles-via-configcpp)
  25. [Keine Namespaces](#25-keine-namespaces)
  26. [String-Methoden modifizieren in-place](#26-string-methoden-modifizieren-in-place)
  27. [ref-Zyklen verursachen Speicherlecks](#27-ref-zyklen-verursachen-speicherlecks)
  28. [Keine Destruktor-Garantie beim Server-Shutdown](#28-keine-destruktor-garantie-beim-server-shutdown)
  29. [Kein Scope-basiertes Ressourcenmanagement (RAII)](#29-kein-scope-basiertes-ressourcenmanagement-raii)
  30. [GetGame().GetPlayer() gibt null auf dem Server zurueck](#30-getgamegetplayer-gibt-null-auf-dem-server-zurueck)
- [Kommend von C++](#kommend-von-c)
- [Kommend von C#](#kommend-von-c-1)
- [Kommend von Java](#kommend-von-java)
- [Kommend von Python](#kommend-von-python)
- [Schnellreferenz-Tabelle](#schnellreferenz-tabelle)
- [Navigation](#navigation)

---

## Vollstaendige Fallstrick-Referenz

### 1. Kein ternaerer Operator

**Was Sie schreiben wuerden:**
```c
int x = (condition) ? valueA : valueB;
```

**Was passiert:** Kompilierfehler. Der `? :`-Operator existiert nicht.

**Korrekte Loesung:**
```c
int x;
if (condition)
    x = valueA;
else
    x = valueB;
```

---

### 2. Keine do...while-Schleife

**Was Sie schreiben wuerden:**
```c
do {
    Process();
} while (HasMore());
```

**Was passiert:** Kompilierfehler. Das `do`-Schluesselwort existiert nicht.

**Korrekte Loesung — Flag-Muster:**
```c
bool first = true;
while (first || HasMore())
{
    first = false;
    Process();
}
```

**Korrekte Loesung — Break-Muster:**
```c
while (true)
{
    Process();
    if (!HasMore())
        break;
}
```

---

### 3. Kein try/catch/throw

**Was Sie schreiben wuerden:**
```c
try {
    RiskyOperation();
} catch (Exception e) {
    HandleError(e);
}
```

**Was passiert:** Kompilierfehler. Diese Schluesselwoerter existieren nicht.

**Korrekte Loesung:** Guard-Klauseln mit fruehzeitigem Return.
```c
void DoOperation()
{
    if (!CanDoOperation())
    {
        ErrorEx("Kann Operation nicht ausfuehren", ErrorExSeverity.WARNING);
        return;
    }

    // Sicher fortfahren
    RiskyOperation();
}
```

Siehe [Kapitel 1.11 — Fehlerbehandlung](11-error-handling.md) fuer vollstaendige Muster.

---

### 4. Keine Mehrfachvererbung

**Was Sie schreiben wuerden:**
```c
class MyClass extends BaseA, BaseB  // Zwei Basisklassen
```

**Was passiert:** Kompilierfehler. Nur Einfachvererbung wird unterstuetzt.

**Korrekte Loesung:** Von einer Klasse erben, die andere zusammensetzen:
```c
class MyClass extends BaseA
{
    ref BaseB m_Helper;

    void MyClass()
    {
        m_Helper = new BaseB();
    }
}
```

---

### 5. Kein Operator-Overloading (ausser Index)

**Was Sie schreiben wuerden:**
```c
Vector3 operator+(Vector3 a, Vector3 b) { ... }
bool operator==(MyClass other) { ... }
```

**Was passiert:** Kompilierfehler. Eigene Operatoren koennen nicht definiert werden.

**Korrekte Loesung:** Benannte Methoden verwenden:
```c
class MyVector
{
    float x, y, z;

    MyVector Add(MyVector other)
    {
        MyVector result = new MyVector();
        result.x = x + other.x;
        result.y = y + other.y;
        result.z = z + other.z;
        return result;
    }

    bool Equals(MyVector other)
    {
        return (x == other.x && y == other.y && z == other.z);
    }
}
```

**Ausnahme:** Der Index-Operator `[]` kann ueber `Get(index)`- und `Set(index, value)`-Methoden ueberladen werden:
```c
class MyContainer
{
    int data[10];

    int Get(int index) { return data[index]; }
    void Set(int index, int value) { data[index] = value; }
}

MyContainer c = new MyContainer();
c[3] = 42;        // Ruft Set(3, 42) auf
int v = c[3];     // Ruft Get(3) auf
```

---

### 6. Keine Lambdas / anonymen Funktionen

**Was Sie schreiben wuerden:**
```c
array.Sort((a, b) => a.name.CompareTo(b.name));
button.OnClick += () => { DoSomething(); };
```

**Was passiert:** Kompilierfehler. Lambda-Syntax existiert nicht.

**Korrekte Loesung:** Benannte Methoden definieren und als `ScriptCaller` uebergeben oder string-basierte Callbacks verwenden:
```c
// Benannte Methode
void OnButtonClick()
{
    DoSomething();
}

// String-basierter Callback (von CallLater, Timern etc. verwendet)
GetGame().GetCallQueue(CALL_CATEGORY_GAMEPLAY).CallLater(this.OnButtonClick, 1000, false);
```

---

### 7. Keine Delegates / Funktionszeiger (nativ)

**Was Sie schreiben wuerden:**
```c
delegate void MyCallback(int value);
MyCallback cb = SomeFunction;
cb(42);
```

**Was passiert:** Kompilierfehler. Das `delegate`-Schluesselwort existiert nicht.

**Korrekte Loesung:** `ScriptCaller`, `ScriptInvoker` oder string-basierte Methodennamen verwenden:
```c
// ScriptCaller (einzelner Callback)
ScriptCaller caller = ScriptCaller.Create(MyFunction);

// ScriptInvoker (Event mit mehreren Abonnenten)
ref ScriptInvoker m_OnEvent = new ScriptInvoker();
m_OnEvent.Insert(MyHandler);
m_OnEvent.Invoke();  // Ruft alle registrierten Handler auf
```

---

### 8. Kein String-Escape fuer Backslash/Anfuehrungszeichen

**Was Sie schreiben wuerden:**
```c
string path = "C:\\Users\\folder";
string quote = "He said \"hello\"";
```

**Was passiert:** CParser stuerzt ab oder erzeugt fehlerhaften Output. Die `\\`- und `\"`-Escape-Sequenzen brechen den String-Parser.

**Korrekte Loesung:** Backslash- und Anfuehrungszeichen in String-Literalen vollstaendig vermeiden:
```c
// Schraegstriche fuer Pfade verwenden
string path = "C:/Users/folder";

// Einfache Anfuehrungszeichen verwenden oder umformulieren, um eingebettete doppelte Anfuehrungszeichen zu vermeiden
string quote = "He said 'hello'";

// String-Verkettung verwenden, wenn Sie absolut Sonderzeichen brauchen
// (immer noch riskant — gruendlich testen)
```

> **Hinweis:** `\n`-, `\r`- und `\t`-Escape-Sequenzen funktionieren. Nur `\\` und `\"` sind fehlerhaft.

---

### 9. Keine Variablen-Neudeklaration in else-if-Bloecken

**Was Sie schreiben wuerden:**
```c
if (condA)
{
    string msg = "Fall A";
    Print(msg);
}
else if (condB)
{
    string msg = "Fall B";  // Gleicher Variablenname im Geschwisterblock
    Print(msg);
}
```

**Was passiert:** Kompilierfehler: "multiple declaration of variable 'msg'". Enforce Script behandelt Variablen in geschwisterlichen `if`/`else if`/`else`-Bloecken als im selben Scope befindlich.

**Korrekte Loesung — eindeutige Namen:**
```c
if (condA)
{
    string msgA = "Fall A";
    Print(msgA);
}
else if (condB)
{
    string msgB = "Fall B";
    Print(msgB);
}
```

**Korrekte Loesung — vor dem if deklarieren:**
```c
string msg;
if (condA)
{
    msg = "Fall A";
}
else if (condB)
{
    msg = "Fall B";
}
Print(msg);
```

---

### 10. Kein Ternaer in Variablendeklaration

Verwandt mit Fallstrick #1, aber spezifisch fuer Deklarationen:

**Was Sie schreiben wuerden:**
```c
string label = isAdmin ? "Admin" : "Player";
```

**Korrekte Loesung:**
```c
string label;
if (isAdmin)
    label = "Admin";
else
    label = "Player";
```

---

### 11. Object.IsAlive() existiert NICHT auf Basis-Object

**Was Sie schreiben wuerden:**
```c
Object obj = GetSomething();
if (obj.IsAlive())  // Pruefen ob lebendig
```

**Was passiert:** Kompilierfehler oder Laufzeitabsturz. `IsAlive()` ist auf `EntityAI` definiert, nicht auf `Object`.

**Korrekte Loesung:**
```c
Object obj = GetSomething();
EntityAI eai;
if (Class.CastTo(eai, obj) && eai.IsAlive())
{
    // Sicher lebendig
}
```

---

### 12. Kein nullptr — verwenden Sie NULL oder null

**Was Sie schreiben wuerden:**
```c
if (obj == nullptr)
```

**Was passiert:** Kompilierfehler. Das `nullptr`-Schluesselwort existiert nicht.

**Korrekte Loesung:**
```c
if (obj == null)    // Kleinbuchstaben funktioniert
if (obj == NULL)    // Grossbuchstaben funktioniert auch
if (!obj)           // Idiomatische Null-Pruefung (bevorzugt)
```

---

### 13. switch/case hat KEIN Fall-Through

**Was Sie schreiben wuerden (C/C++-Fall-Through erwartend):**
```c
switch (value)
{
    case 1:
    case 2:
    case 3:
        Print("1, 2 oder 3");  // In C++ fallen Cases 1 und 2 hierhin durch
        break;
}
```

**Was passiert:** Nur Case 3 fuehrt den Print aus. Cases 1 und 2 sind leer — sie tun nichts und fallen NICHT durch.

**Korrekte Loesung:**
```c
if (value >= 1 && value <= 3)
{
    Print("1, 2 oder 3");
}

// Oder jeden Fall explizit behandeln:
switch (value)
{
    case 1:
        Print("1, 2 oder 3");
        break;
    case 2:
        Print("1, 2 oder 3");
        break;
    case 3:
        Print("1, 2 oder 3");
        break;
}
```

> **Hinweis:** `break` ist technisch optional in Enforce Script, da es kein Fall-Through gibt, aber es ist konventionell, es einzufuegen.

---

### 14. Keine Standard-Parameter-Ausdruecke

**Was Sie schreiben wuerden:**
```c
void Spawn(vector pos = GetDefaultPos())    // Ausdruck als Standard
void Spawn(vector pos = Vector(0, 100, 0))  // Konstruktor als Standard
```

**Was passiert:** Kompilierfehler. Standardparameterwerte muessen **Literale** oder `NULL` sein.

**Korrekte Loesung:**
```c
void Spawn(vector pos = "0 100 0")    // String-Literal fuer Vektor — OK
void Spawn(int count = 5)             // Integer-Literal — OK
void Spawn(float radius = 10.0)      // Float-Literal — OK
void Spawn(string name = "default")   // String-Literal — OK
void Spawn(Object obj = NULL)         // NULL — OK

// Fuer komplexe Standards, Ueberladungen verwenden:
void Spawn()
{
    Spawn(GetDefaultPos());  // Die parametrische Version aufrufen
}

void Spawn(vector pos)
{
    // Eigentliche Implementierung
}
```

---

### 15. JsonFileLoader.JsonLoadFile gibt void zurueck

**Was Sie schreiben wuerden:**
```c
MyConfig cfg = JsonFileLoader<MyConfig>.JsonLoadFile(path);
// oder:
if (JsonFileLoader<MyConfig>.JsonLoadFile(path, cfg))
```

**Was passiert:** Kompilierfehler. `JsonLoadFile` gibt `void` zurueck, nicht das geladene Objekt oder einen bool.

**Korrekte Loesung:**
```c
MyConfig cfg = new MyConfig();  // Zuerst Instanz mit Standardwerten erstellen
JsonFileLoader<MyConfig>.JsonLoadFile(path, cfg);  // Befuellt cfg in-place
// cfg enthaelt jetzt geladene Werte (oder hat immer noch Standards, wenn die Datei ungueltig war)
```

> **Hinweis:** Die neuere `JsonFileLoader<T>.LoadFile()`-Methode gibt `bool` zurueck, aber `JsonLoadFile` (die haeufig gesehene Version) tut dies nicht.

---

### 16. Kein #define-Wert-Substitution

**Was Sie schreiben wuerden:**
```c
#define MAX_PLAYERS 60
#define VERSION_STRING "1.0.0"
int max = MAX_PLAYERS;
```

**Was passiert:** Kompilierfehler. Enforce Script `#define` erstellt nur Existenz-Flags fuer `#ifdef`-Pruefungen. Es unterstuetzt keine Wert-Substitution.

**Korrekte Loesung:**
```c
// const fuer Werte verwenden
const int MAX_PLAYERS = 60;
const string VERSION_STRING = "1.0.0";

// #define nur fuer bedingte Kompilierungs-Flags verwenden
#define MY_MOD_ENABLED
```

---

### 17. Keine Interfaces / abstrakte Klassen (erzwungen)

**Was Sie schreiben wuerden:**
```c
interface ISerializable
{
    void Serialize();
    void Deserialize();
}

abstract class BaseProcessor
{
    abstract void Process();
}
```

**Was passiert:** Die Schluesselwoerter `interface` und `abstract` existieren nicht.

**Korrekte Loesung:** Regulaere Klassen mit leeren Basismethoden verwenden:
```c
// "Interface" — Basisklasse mit leeren Methoden
class ISerializable
{
    void Serialize() {}     // In Unterklasse ueberschreiben
    void Deserialize() {}   // In Unterklasse ueberschreiben
}

// "Abstrakte" Klasse — gleiches Muster
class BaseProcessor
{
    void Process()
    {
        ErrorEx("BaseProcessor.Process() muss ueberschrieben werden!", ErrorExSeverity.ERROR);
    }
}

class ConcreteProcessor extends BaseProcessor
{
    override void Process()
    {
        // Tatsaechliche Implementierung
    }
}
```

Der Compiler erzwingt NICHT, dass Unterklassen die Basismethoden ueberschreiben. Das Vergessen des Ueberschreibens verwendet stillschweigend die leere Basisimplementierung.

---

### 18. Keine Generics-Einschraenkungen

**Was Sie schreiben wuerden:**
```c
class Container<T> where T : EntityAI  // T auf EntityAI einschraenken
```

**Was passiert:** Kompilierfehler. Die `where`-Klausel existiert nicht. Template-Parameter akzeptieren jeden Typ.

**Korrekte Loesung:** Zur Laufzeit validieren:
```c
class EntityContainer<Class T>
{
    void Add(T item)
    {
        // Laufzeit-Typpruefung statt Kompilierzeit-Einschraenkung
        EntityAI eai;
        if (!Class.CastTo(eai, item))
        {
            ErrorEx("EntityContainer akzeptiert nur EntityAI-Unterklassen");
            return;
        }
        // fortfahren
    }
}
```

---

### 19. Keine Enum-Validierung

**Was Sie schreiben wuerden:**
```c
EDamageState state = (EDamageState)999;  // Fehler oder Ausnahme erwarten
```

**Was passiert:** Kein Fehler. Jeder `int`-Wert kann einer Enum-Variable zugewiesen werden, auch Werte ausserhalb des definierten Bereichs.

**Korrekte Loesung:** Manuell validieren:
```c
bool IsValidDamageState(int value)
{
    return (value >= EDamageState.PRISTINE && value <= EDamageState.RUINED);
}

int rawValue = LoadFromConfig();
if (IsValidDamageState(rawValue))
{
    EDamageState state = rawValue;
}
else
{
    Print("Ungueltiger Schadenszustand: " + rawValue.ToString());
    EDamageState state = EDamageState.PRISTINE;  // Fallback
}
```

---

### 20. Keine variadischen Parameter

**Was Sie schreiben wuerden:**
```c
void Log(string format, params object[] args)
void Printf(string fmt, ...)
```

**Was passiert:** Kompilierfehler. Variadische Parameter existieren nicht.

**Korrekte Loesung:** `string.Format` mit fester Parameteranzahl verwenden, oder `Param`-Klassen nutzen:
```c
// string.Format unterstuetzt bis zu 9 Positionsargumente
string msg = string.Format("Spieler %1 bei %2 mit %3 HP", name, pos, hp);

// Fuer variable Datenmenge ein Array uebergeben
void LogMultiple(string tag, array<string> messages)
{
    foreach (string msg : messages)
    {
        Print("[" + tag + "] " + msg);
    }
}
```

---

### 21. Keine verschachtelten Klassendeklarationen

**Was Sie schreiben wuerden:**
```c
class Outer
{
    class Inner  // Verschachtelte Klasse
    {
        int value;
    }
}
```

**Was passiert:** Kompilierfehler. Klassen koennen nicht innerhalb anderer Klassen deklariert werden.

**Korrekte Loesung:** Alle Klassen auf oberster Ebene deklarieren, Namenskonventionen verwenden, um Beziehungen zu zeigen:
```c
class MySystem_Config
{
    int value;
}

class MySystem
{
    ref MySystem_Config m_Config;
}
```

---

### 22. Statische Arrays haben feste Groesse

**Was Sie schreiben wuerden:**
```c
int size = GetCount();
int arr[size];  // Dynamische Groesse zur Laufzeit
```

**Was passiert:** Kompilierfehler. Statische Array-Groessen muessen Kompilierzeit-Konstanten sein.

**Korrekte Loesung:**
```c
// Eine Konstante fuer statische Arrays verwenden
const int BUFFER_SIZE = 64;
int arr[BUFFER_SIZE];

// Oder dynamische Arrays fuer Laufzeit-Groessenanpassung verwenden
array<int> arr = new array<int>;
arr.Resize(GetCount());
```

---

### 23. array.Remove ist unsortiert

**Was Sie schreiben wuerden (Reihenfolge-Erhaltung erwartend):**
```c
array<string> items = {"A", "B", "C", "D"};
items.Remove(1);  // Erwartet: {"A", "C", "D"}
```

**Was passiert:** `Remove(index)` tauscht das Element mit dem **letzten** Element und entfernt dann das letzte. Ergebnis: `{"A", "D", "C"}`. Die Reihenfolge wird NICHT beibehalten.

**Korrekte Loesung:**
```c
// RemoveOrdered fuer Reihenfolge-Erhaltung verwenden (langsamer — verschiebt Elemente)
items.RemoveOrdered(1);  // {"A", "C", "D"} — korrekte Reihenfolge

// RemoveItem zum Finden und Entfernen nach Wert verwenden (ebenfalls geordnet)
items.RemoveItem("B");   // {"A", "C", "D"}
```

---

### 24. Kein #include — alles via config.cpp

**Was Sie schreiben wuerden:**
```c
#include "MyHelper.c"
#include "Utils/StringUtils.c"
```

**Was passiert:** Keine Wirkung oder Kompilierfehler. Es gibt keine `#include`-Direktive.

**Korrekte Loesung:** Alle Skriptdateien werden ueber `config.cpp` im `CfgMods`-Eintrag der Mod geladen. Die Dateiladereihenfolge wird durch die Skriptschicht (`3_Game`, `4_World`, `5_Mission`) und die alphabetische Reihenfolge innerhalb jeder Schicht bestimmt.

```cpp
// config.cpp
class CfgMods
{
    class MyMod
    {
        type = "mod";
        dependencies[] = { "Game", "World", "Mission" };

        class defs
        {
            class gameScriptModule
            {
                files[] = { "MyMod/Scripts/3_Game" };
            };
            class worldScriptModule
            {
                files[] = { "MyMod/Scripts/4_World" };
            };
            class missionScriptModule
            {
                files[] = { "MyMod/Scripts/5_Mission" };
            };
        };
    };
};
```

---

### 25. Keine Namespaces

**Was Sie schreiben wuerden:**
```c
namespace MyMod { class Config { } }
namespace MyMod.Utils { class StringHelper { } }
```

**Was passiert:** Kompilierfehler. Das `namespace`-Schluesselwort existiert nicht. Alle Klassen teilen einen einzigen globalen Scope.

**Korrekte Loesung:** Namenspraefixe verwenden, um Konflikte zu vermeiden:
```c
class MyConfig { }          // MyFramework
class MyAI_Config { }       // MyAI-Mod
class MyM_MissionData { }   // MyMissions-Mod
class VPP_AdminConfig { }     // VPP Admin
```

---

### 26. String-Methoden modifizieren in-place

**Was Sie schreiben wuerden (einen Rueckgabewert erwartend):**
```c
string upper = myString.ToUpper();  // Erwartet: gibt neuen String zurueck
```

**Was passiert:** `ToUpper()` und `ToLower()` modifizieren den String **in-place** und geben `void` zurueck.

**Korrekte Loesung:**
```c
// Zuerst eine Kopie machen, wenn Sie das Original beibehalten muessen
string original = "Hello World";
string upper = original;
upper.ToUpper();  // upper ist jetzt "HELLO WORLD", original unveraendert

// Gleich fuer TrimInPlace
string trimmed = "  hello  ";
trimmed.TrimInPlace();  // "hello"
```

---

### 27. ref-Zyklen verursachen Speicherlecks

**Was Sie schreiben wuerden:**
```c
class Parent
{
    ref Child m_Child;
}
class Child
{
    ref Parent m_Parent;  // Zirkulaere ref — beide referenzieren einander
}
```

**Was passiert:** Keines der Objekte wird jemals vom Garbage Collector erfasst. Die Referenzzaehler erreichen nie Null, weil jedes eine `ref` auf das andere haelt.

**Korrekte Loesung:** Eine Seite muss einen rohen (nicht-ref) Zeiger verwenden:
```c
class Parent
{
    ref Child m_Child;  // Parent BESITZT das Kind (ref)
}
class Child
{
    Parent m_Parent;    // Kind REFERENZIERT das Elternteil (roh — kein ref)
}
```

---

### 28. Keine Destruktor-Garantie beim Server-Shutdown

**Was Sie schreiben wuerden (Bereinigung erwartend):**
```c
void ~MyManager()
{
    SaveData();  // Erwartet, dass dies beim Shutdown laeuft
}
```

**Was passiert:** Server-Shutdown kann den Prozess beenden, bevor Destruktoren laufen. Ihr Speichern geschieht nie.

**Korrekte Loesung:** Proaktiv in regelmaessigen Abstaenden und bei bekannten Lebenszyklus-Events speichern:
```c
class MyManager
{
    void OnMissionFinish()  // Wird vor dem Shutdown aufgerufen
    {
        SaveData();  // Zuverlaessiger Speicherpunkt
    }

    void OnUpdate(float dt)
    {
        m_SaveTimer += dt;
        if (m_SaveTimer > 300.0)  // Alle 5 Minuten
        {
            SaveData();
            m_SaveTimer = 0;
        }
    }
}
```

---

### 29. Kein Scope-basiertes Ressourcenmanagement (RAII)

**Was Sie schreiben wuerden (in C++):**
```c
{
    FileHandle f = OpenFile("test.txt", FileMode.WRITE);
    // f wird automatisch geschlossen, wenn der Scope endet
}
```

**Was passiert:** Enforce Script schliesst Dateihandles nicht, wenn Variablen den Scope verlassen (auch nicht mit `autoptr`).

**Korrekte Loesung:** Ressourcen immer explizit schliessen:
```c
FileHandle fh = OpenFile("$profile:MyMod/data.txt", FileMode.WRITE);
if (fh != 0)
{
    FPrintln(fh, "data");
    CloseFile(fh);  // Muss manuell geschlossen werden!
}
```

---

### 30. GetGame().GetPlayer() gibt null auf dem Server zurueck

**Was Sie schreiben wuerden:**
```c
PlayerBase player = PlayerBase.Cast(GetGame().GetPlayer());
player.DoSomething();  // ABSTURZ auf dem Server!
```

**Was passiert:** `GetGame().GetPlayer()` gibt den **lokalen** Spieler zurueck. Auf einem dedizierten Server gibt es keinen lokalen Spieler — es gibt `null` zurueck.

**Korrekte Loesung:** Auf dem Server die Spielerliste durchiterieren:
```c
#ifdef SERVER
    array<Man> players = new array<Man>;
    GetGame().GetPlayers(players);
    foreach (Man man : players)
    {
        PlayerBase player;
        if (Class.CastTo(player, man))
        {
            player.DoSomething();
        }
    }
#else
    PlayerBase player = PlayerBase.Cast(GetGame().GetPlayer());
    if (player)
    {
        player.DoSomething();
    }
#endif
```

---

## Kommend von C++

Wenn Sie C++-Entwickler sind, hier die groessten Umstellungen:

| C++-Feature | Enforce-Script-Aequivalent |
|-------------|--------------------------|
| `std::vector` | `array<T>` |
| `std::map` | `map<K,V>` |
| `std::unique_ptr` | `ref` / `autoptr` |
| `dynamic_cast<T*>` | `Class.CastTo()` oder `T.Cast()` |
| `try/catch` | Guard-Klauseln |
| `operator+` | Benannte Methoden (`Add()`) |
| `namespace` | Namenspraefixe (`My`, `VPP_`) |
| `#include` | config.cpp `files[]` |
| RAII | Manuelle Bereinigung in Lebenszyklus-Methoden |
| Mehrfachvererbung | Einfachvererbung + Komposition |
| `nullptr` | `null` / `NULL` |
| Templates mit Einschraenkungen | Templates ohne Einschraenkungen + Laufzeitpruefungen |
| `do...while` | `while (true) { ... if (!cond) break; }` |

---

## Kommend von C#

| C#-Feature | Enforce-Script-Aequivalent |
|-------------|--------------------------|
| `interface` | Basisklasse mit leeren Methoden |
| `abstract` | Basisklasse + ErrorEx in Basismethoden |
| `delegate` / `event` | `ScriptInvoker` |
| Lambda `=>` | Benannte Methoden |
| `?.` Null-Bedingung | Manuelle Null-Pruefungen |
| `??` Null-Koaleszenz | `if (!x) x = default;` |
| `try/catch` | Guard-Klauseln |
| `using` (IDisposable) | Manuelle Bereinigung |
| Properties `{ get; set; }` | Oeffentliche Felder oder explizite Getter/Setter-Methoden |
| LINQ | Manuelle Schleifen |
| `nameof()` | Fest kodierte Strings |
| `async/await` | CallLater / Timer |

---

## Kommend von Java

| Java-Feature | Enforce-Script-Aequivalent |
|-------------|--------------------------|
| `interface` | Basisklasse mit leeren Methoden |
| `try/catch/finally` | Guard-Klauseln |
| Garbage Collection | `ref` + Referenzzaehlung (kein GC fuer Zyklen) |
| `@Override` | `override`-Schluesselwort |
| `instanceof` | `obj.IsInherited(typename)` |
| `package` | Namenspraefixe |
| `import` | config.cpp `files[]` |
| `enum` mit Methoden | `enum` (nur int) + Hilfsklasse |
| `final` | `const` (nur fuer Variablen) |
| Annotations | Nicht verfuegbar |

---

## Kommend von Python

| Python-Feature | Enforce-Script-Aequivalent |
|-------------|--------------------------|
| Dynamische Typisierung | Statische Typisierung (alle Variablen typisiert) |
| `try/except` | Guard-Klauseln |
| `lambda` | Benannte Methoden |
| List Comprehension | Manuelle Schleifen |
| `**kwargs` / `*args` | Feste Parameter |
| Duck Typing | `IsInherited()` / `Class.CastTo()` |
| `__init__` | Konstruktor (gleicher Name wie Klasse) |
| `__del__` | Destruktor (`~ClassName()`) |
| `import` | config.cpp `files[]` |
| Mehrfachvererbung | Einfachvererbung + Komposition |
| `None` | `null` / `NULL` |
| Einrueckungsbasierte Bloecke | `{ }`-Klammern |
| f-strings | `string.Format("text %1 %2", a, b)` |

---

## Schnellreferenz-Tabelle

| Feature | Existiert? | Workaround |
|---------|---------|------------|
| Ternaer `? :` | Nein | if/else |
| `do...while` | Nein | while + break |
| `try/catch` | Nein | Guard-Klauseln |
| Mehrfachvererbung | Nein | Komposition |
| Operator-Overloading | Nur Index | Benannte Methoden |
| Lambdas | Nein | Benannte Methoden |
| Delegates | Nein | `ScriptInvoker` |
| `\\` / `\"` in Strings | Fehlerhaft | Vermeiden |
| Variablen-Neudeklaration | Fehlerhaft in else-if | Eindeutige Namen oder vor if deklarieren |
| `Object.IsAlive()` | Nicht auf Basis-Object | Zuerst zu `EntityAI` casten |
| `nullptr` | Nein | `null` / `NULL` |
| switch Fall-Through | Nein | Jeder Case ist unabhaengig |
| Standard-Param-Ausdruecke | Nein | Nur Literale oder NULL |
| `#define`-Werte | Nein | `const` |
| Interfaces | Nein | Leere Basisklasse |
| Generic-Einschraenkungen | Nein | Laufzeit-Typpruefungen |
| Enum-Validierung | Nein | Manuelle Bereichspruefung |
| Variadische Params | Nein | `string.Format` oder Arrays |
| Verschachtelte Klassen | Nein | Oberste Ebene mit Namenspraefixen |
| Variable statische Arrays | Nein | `array<T>` |
| `#include` | Nein | config.cpp `files[]` |
| Namespaces | Nein | Namenspraefixe |
| RAII | Nein | Manuelle Bereinigung |
| `GetGame().GetPlayer()` Server | Gibt null zurueck | `GetPlayers()` iterieren |

---

## Navigation

| Zurueck | Hoch | Weiter |
|----------|----|------|
| [1.11 Fehlerbehandlung](11-error-handling.md) | [Teil 1: Enforce Script](../README.md) | [Teil 2: Mod-Struktur](../02-mod-structure/01-five-layers.md) |
