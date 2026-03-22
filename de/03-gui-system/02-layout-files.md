# Kapitel 3.2: Layout-Dateiformat (.layout)

[Startseite](../../README.md) | [<< Zurueck: Widget-Typen](01-widget-types.md) | **Layout-Dateiformat** | [Weiter: Groesse & Positionierung >>](03-sizing-positioning.md)

---

## Grundstruktur

Eine `.layout`-Datei definiert einen Baum von Widgets. Jede Datei hat genau ein Wurzel-Widget, das verschachtelte Kinder enthaelt.

```
 WidgetTypeClass WidgetName {
 attribute value
 attribute "quoted value"
 {
  ChildWidgetTypeClass ChildName {
   attribute value
  }
 }
}
```

Wichtige Regeln:

1. Das Wurzelelement ist immer ein einzelnes Widget (typischerweise `FrameWidgetClass`).
2. Widget-Typnamen verwenden den **Layout-Klassennamen**, der immer mit `Class` endet (z.B. `FrameWidgetClass`, `TextWidgetClass`, `ButtonWidgetClass`).
3. Jedes Widget hat einen eindeutigen Namen nach seinem Typklassennamen.
4. Attribute sind `Schluessel Wert`-Paare, eines pro Zeile.
5. Attributnamen mit Leerzeichen muessen in Anfuehrungszeichen stehen: `"text halign" center`.
6. String-Werte stehen in Anfuehrungszeichen: `text "Hello World"`.
7. Numerische Werte stehen ohne Anfuehrungszeichen: `size 0.5 0.3`.
8. Kinder werden in `{ }`-Bloecken nach den Attributen des Elternteils verschachtelt.

---

## Attribut-Referenz

### Positionierung & Groesse

| Attribut | Werte | Beschreibung |
|---|---|---|
| `position` | `x y` | Widget-Position (proportional 0-1 oder Pixelwerte) |
| `size` | `w h` | Widget-Dimensionen (proportional 0-1 oder Pixelwerte) |
| `halign` | `left_ref`, `center_ref`, `right_ref` | Horizontaler Ausrichtungs-Referenzpunkt |
| `valign` | `top_ref`, `center_ref`, `bottom_ref` | Vertikaler Ausrichtungs-Referenzpunkt |
| `hexactpos` | `0` oder `1` | 0 = proportionale X-Position, 1 = Pixel-X-Position |
| `vexactpos` | `0` oder `1` | 0 = proportionale Y-Position, 1 = Pixel-Y-Position |
| `hexactsize` | `0` oder `1` | 0 = proportionale Breite, 1 = Pixel-Breite |
| `vexactsize` | `0` oder `1` | 0 = proportionale Hoehe, 1 = Pixel-Hoehe |
| `fixaspect` | `fixwidth`, `fixheight` | Seitenverhaeltnis beibehalten durch Einschraenkung einer Dimension |
| `scaled` | `0` oder `1` | Mit DayZ-UI-Skalierungseinstellung skalieren |
| `priority` | Ganzzahl | Z-Reihenfolge (hoehere Werte werden oben gerendert) |

Die `hexactpos`-, `vexactpos`-, `hexactsize`- und `vexactsize`-Flags sind die wichtigsten Attribute im gesamten Layout-System. Sie steuern, ob jede Dimension proportionale (0.0 - 1.0 relativ zum Elternteil) oder Pixel- (absolute Bildschirmpixel) Einheiten verwendet. Siehe [3.3 Groesse & Positionierung](03-sizing-positioning.md) fuer eine ausfuehrliche Erklaerung.

### Visuelle Attribute

| Attribut | Werte | Beschreibung |
|---|---|---|
| `visible` | `0` oder `1` | Anfangs-Sichtbarkeit (0 = versteckt) |
| `color` | `r g b a` | Farbe als vier Floats, jeweils 0.0 bis 1.0 |
| `style` | Style-Name | Vordefinierter visueller Style (z.B. `Default`, `Colorable`) |
| `draggable` | `0` oder `1` | Widget kann vom Benutzer gezogen werden |
| `clipchildren` | `0` oder `1` | Kind-Widgets an die Grenzen dieses Widgets beschneiden |
| `inheritalpha` | `0` oder `1` | Kinder erben den Alpha-Wert dieses Widgets |
| `keepsafezone` | `0` oder `1` | Widget innerhalb der Bildschirm-Sicherheitszone halten |

### Verhaltens-Attribute

| Attribut | Werte | Beschreibung |
|---|---|---|
| `ignorepointer` | `0` oder `1` | Widget ignoriert Mauseingabe (Klicks gehen hindurch) |
| `disabled` | `0` oder `1` | Widget ist deaktiviert |
| `"no focus"` | `0` oder `1` | Widget kann keinen Tastaturfokus erhalten |

### Text-Attribute

Diese gelten fuer `TextWidgetClass`, `RichTextWidgetClass`, `MultilineTextWidgetClass`, `ButtonWidgetClass` und andere texttragende Widgets.

| Attribut | Werte | Beschreibung |
|---|---|---|
| `text` | `"string"` | Standard-Textinhalt |
| `font` | `"pfad/zur/schrift"` | Schriftdateipfad |
| `"text halign"` | `left`, `center`, `right` | Horizontale Textausrichtung innerhalb des Widgets |
| `"text valign"` | `top`, `center`, `bottom` | Vertikale Textausrichtung innerhalb des Widgets |
| `"bold text"` | `0` oder `1` | Fette Darstellung |
| `"italic text"` | `0` oder `1` | Kursive Darstellung |
| `"exact text"` | `0` oder `1` | Exakte Pixel-Schriftgroesse statt proportional verwenden |
| `"exact text size"` | Ganzzahl | Schriftgroesse in Pixeln (erfordert `"exact text" 1`) |
| `"size to text h"` | `0` oder `1` | Widget-Breite an Text anpassen |
| `"size to text v"` | `0` oder `1` | Widget-Hoehe an Text anpassen |
| `"text sharpness"` | Float | Text-Rendering-Schaerfe |
| `wrap` | `0` oder `1` | Wortumbruch aktivieren |

### Bild-Attribute

Diese gelten fuer `ImageWidgetClass`.

| Attribut | Werte | Beschreibung |
|---|---|---|
| `image0` | `"set:name image:name"` | Primaerbild aus einem ImageSet |
| `mode` | `blend`, `additive`, `stretch` | Bild-Mischmodus |
| `"src alpha"` | `0` oder `1` | Quell-Alpha-Kanal verwenden |
| `stretch` | `0` oder `1` | Bild auf Widget-Groesse dehnen |
| `filter` | `0` oder `1` | Texturfilterung aktivieren |
| `"flip u"` | `0` oder `1` | Bild horizontal spiegeln |
| `"flip v"` | `0` oder `1` | Bild vertikal spiegeln |
| `"clamp mode"` | `clamp`, `wrap` | Textur-Kantenverhalten |
| `"stretch mode"` | `stretch_w_h`, etc. | Dehnungsmodus |

### Spacer-Attribute

Diese gelten fuer `WrapSpacerWidgetClass` und `GridSpacerWidgetClass`.

| Attribut | Werte | Beschreibung |
|---|---|---|
| `Padding` | Ganzzahl | Innerer Abstand in Pixeln |
| `Margin` | Ganzzahl | Abstand zwischen Kind-Elementen in Pixeln |
| `"Size To Content H"` | `0` oder `1` | Breite an Kinder anpassen |
| `"Size To Content V"` | `0` oder `1` | Hoehe an Kinder anpassen |
| `content_halign` | `left`, `center`, `right` | Horizontale Ausrichtung des Kind-Inhalts |
| `content_valign` | `top`, `center`, `bottom` | Vertikale Ausrichtung des Kind-Inhalts |
| `Columns` | Ganzzahl | Rasterspalten (nur GridSpacer) |
| `Rows` | Ganzzahl | Rasterzeilen (nur GridSpacer) |

### Button-Attribute

| Attribut | Werte | Beschreibung |
|---|---|---|
| `switch` | `toggle` | Macht den Button zu einem Toggle (bleibt gedrueckt) |
| `style` | Style-Name | Visueller Style fuer den Button |

### Slider-Attribute

| Attribut | Werte | Beschreibung |
|---|---|---|
| `"fill in"` | `0` oder `1` | Gefuellte Spur hinter dem Slider-Griff anzeigen |
| `"listen to input"` | `0` oder `1` | Auf Mauseingabe reagieren |

### Scroll-Attribute

| Attribut | Werte | Beschreibung |
|---|---|---|
| `"Scrollbar V"` | `0` oder `1` | Vertikale Scrollleiste anzeigen |
| `"Scrollbar H"` | `0` oder `1` | Horizontale Scrollleiste anzeigen |

---

## Skript-Integration

### Das `scriptclass`-Attribut

Das `scriptclass`-Attribut bindet ein Widget an eine Enforce-Script-Klasse. Wenn das Layout geladen wird, erstellt die Engine eine Instanz dieser Klasse und ruft deren `OnWidgetScriptInit(Widget w)`-Methode auf.

```
FrameWidgetClass MyPanel {
 size 1 1
 scriptclass "MyPanelHandler"
}
```

Die Skript-Klasse muss von `Managed` erben und `OnWidgetScriptInit` implementieren:

```c
class MyPanelHandler : Managed
{
    Widget m_Root;

    void OnWidgetScriptInit(Widget w)
    {
        m_Root = w;
    }
}
```

### Der ScriptParamsClass-Block

Parameter koennen vom Layout an die `scriptclass` ueber einen `ScriptParamsClass`-Block uebergeben werden. Dieser Block erscheint als zweiter `{ }`-Kindblock nach den Kindern des Widgets.

```
ImageWidgetClass Logo {
 image0 "set:dayz_gui image:DayZLogo"
 scriptclass "Bouncer"
 {
  ScriptParamsClass {
   amount 0.1
   speed 1
  }
 }
}
```

Die Skript-Klasse liest diese Parameter in `OnWidgetScriptInit` ueber das Skriptparameter-System des Widgets.

### DabsFramework ViewBinding

In Mods, die DabsFramework MVC verwenden, verbindet das `scriptclass "ViewBinding"`-Muster Widgets mit den Dateneigenschaften eines ViewControllers:

```
TextWidgetClass StatusLabel {
 scriptclass "ViewBinding"
 "text halign" center
 {
  ScriptParamsClass {
   Binding_Name "StatusText"
   Two_Way_Binding 0
  }
 }
}
```

| Parameter | Beschreibung |
|---|---|
| `Binding_Name` | Name der ViewController-Eigenschaft, an die gebunden wird |
| `Two_Way_Binding` | `1` = UI-Aenderungen werden an den Controller zurueckgepusht |
| `Relay_Command` | Funktionsname am Controller, der bei Klick/Aenderung des Widgets aufgerufen wird |
| `Selected_Item` | Eigenschaft, an die das ausgewaehlte Element gebunden wird (fuer Listen) |
| `Debug_Logging` | `1` = ausfuehrliches Logging fuer diese Bindung aktivieren |

---

## Kinder-Verschachtelung

Kinder werden in einem `{ }`-Block nach den Attributen des Elternteils platziert. Mehrere Kinder koennen im selben Block existieren.

```
FrameWidgetClass Parent {
 size 1 1
 {
  TextWidgetClass Child1 {
   position 0 0
   size 1 0.1
   text "Erstes"
  }
  TextWidgetClass Child2 {
   position 0 0.1
   size 1 0.1
   text "Zweites"
  }
 }
}
```

Kinder werden immer relativ zu ihrem Elternteil positioniert. Ein Kind mit `position 0 0` und `size 1 1` (proportional) fuellt sein Elternteil vollstaendig.

---

## Vollstaendig kommentiertes Beispiel

Hier ist eine vollstaendig kommentierte Layout-Datei fuer ein Benachrichtigungs-Panel -- die Art von UI, die Sie fuer eine Mod erstellen koennten:

```
// Wurzelcontainer -- unsichtbarer Frame der 30% der Bildschirmbreite abdeckt
// Horizontal zentriert, am oberen Bildschirmrand positioniert
FrameWidgetClass NotificationPanel {

 // Zu Beginn versteckt (Skript zeigt es an)
 visible 0

 // Keine Mausklicks auf Dinge hinter diesem Panel blockieren
 ignorepointer 1

 // Blauer Farbton (R=0.2, G=0.6, B=1.0, A=0.9)
 color 0.2 0.6 1.0 0.9

 // Position: 0 Pixel von links, 0 Pixel von oben
 position 0 0
 hexactpos 1
 vexactpos 1

 // Groesse: 30% der Elternbreite, 30 Pixel hoch
 size 0.3 30
 hexactsize 0
 vexactsize 1

 // Horizontal innerhalb des Elternteils zentrieren
 halign center_ref

 // Kinder-Block
 {
  // Textlabel fuellt das gesamte Benachrichtigungs-Panel
  TextWidgetClass NotificationText {

   // Ebenfalls Mauseingabe ignorieren
   ignorepointer 1

   // Position am Ursprung relativ zum Elternteil
   position 0 0
   hexactpos 1
   vexactpos 1

   // Elternteil vollstaendig fuellen (proportional)
   size 1 1
   hexactsize 0
   vexactsize 0

   // Text in beide Richtungen zentrieren
   "text halign" center
   "text valign" center

   // Fette Schrift verwenden
   font "gui/fonts/Metron-Bold"

   // Standardtext (wird vom Skript ueberschrieben)
   text "Benachrichtigung"
  }
 }
}
```

Und hier ein komplexeres Beispiel -- ein Dialog mit Titelleiste, scrollbarem Inhalt und einem Schliessen-Button:

```
WrapSpacerWidgetClass MyDialog {
 clipchildren 1
 color 0.7059 0.7059 0.7059 0.7843
 size 0.35 0
 halign center_ref
 valign center_ref
 priority 998
 style Outline_1px_BlackBackground
 Padding 5
 "Size To Content H" 1
 "Size To Content V" 1
 content_halign center
 {
  // Titelleisten-Zeile
  FrameWidgetClass TitleBarRow {
   size 1 26
   hexactsize 0
   vexactsize 1
   draggable 1
   {
    PanelWidgetClass TitleBar {
     color 0.4196 0.6471 1 0.9412
     size 1 25
     style rover_sim_colorable
     {
      TextWidgetClass TitleText {
       size 0.85 0.9
       text "Mein Dialog"
       font "gui/fonts/Metron"
       "text halign" center
       "text valign" center
      }
      ButtonWidgetClass CloseBtn {
       size 0.15 0.9
       halign right_ref
       text "X"
      }
     }
    }
   }
  }

  // Scrollbarer Inhaltsbereich
  ScrollWidgetClass ContentScroll {
   size 0.97 235
   hexactsize 0
   vexactsize 1
   "Scrollbar V" 1
   {
    WrapSpacerWidgetClass ContentItems {
     size 1 0
     hexactsize 0
     "Size To Content V" 1
    }
   }
  }
 }
}
```

---

## Haeufige Fehler

1. **Das `Class`-Suffix vergessen** -- In Layouts schreiben Sie `TextWidgetClass`, nicht `TextWidget`.
2. **Proportionale und Pixelwerte mischen** -- Wenn `hexactsize 0`, sind die Groessenwerte 0.0-1.0 proportional. Wenn `hexactsize 1`, sind es Pixelwerte. `300` im proportionalen Modus zu verwenden bedeutet das 300-fache der Elternbreite.
3. **Mehrwort-Attribute nicht in Anfuehrungszeichen setzen** -- Schreiben Sie `"text halign" center`, nicht `text halign center`.
4. **ScriptParamsClass im falschen Block platzieren** -- Es muss in einem separaten `{ }`-Block nach dem Kinder-Block stehen, nicht darin.

---

## Naechste Schritte

- [3.3 Groesse & Positionierung](03-sizing-positioning.md) -- Das proportionale vs. Pixel-Koordinatensystem beherrschen
- [3.4 Container-Widgets](04-containers.md) -- Vertiefung in Spacer- und Scroll-Widgets
