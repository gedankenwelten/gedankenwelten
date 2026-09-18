---
title: "KI-Agenten — Vom Dorf zur Zivilisation"
description: "Fünfundzwanzig KI-Figuren feiern eine Party, tausend gründen eine Religion. Was diese Simulationen zeigen, hängt davon ab, wer genau hinsieht: an ihnen erkennen wir uns selbst."
aktualisiert: 2026-09-18
date: 18.09.2026
tags:
  - geistesblitz
  - ki
  - technologie
  - psychologie
  - komplexität
  - medien
  - year-2026
aliases:
  - Generative Agents
  - Smallville
  - Project Sid
  - KI-Zivilisation in Minecraft
---

# KI-Agenten — Vom Dorf zur Zivilisation

![[assets/KI-Agenten-Vom-Dorf-zur-Zivilisation-banner.jpg|1200]]

<details><summary>🎨</summary>

**Pieter Bruegel der Ältere** — Öl auf Eichenholz, Vogelschau, gedrungene Figuren in erdigen Tönen, Craquelé. Bruegel hat in den *Niederländischen Sprichwörtern* und den *Kinderspielen* als Erster eine Gesellschaft von unten gemalt: Hunderte kleiner Leute, jeder in seiner eigenen Handlung, und aus der Summe entsteht ein Dorf. Genau so sehen Smallville und Project Sid aus, nur dass dort niemand malt. Auf dem Platz: eine Schenke mit Herz über der Tür (die Valentinsparty), Münzen, die in eine Kiste wandern (die Steuer), ein Mönch, der vom Fass predigt (die Pastafari-Priester), ein Mann mit Fackeln (die vermissten Dorfbewohner). Rechts wächst das Dorf zur Stadt. Um den Prediger steht ein Halbkreis beinahe gleicher Figuren — ungeplant, und doch genau: Sids Agenten hatten eine identische Persönlichkeit.

*Prompt:* Authentic 16th-century Flemish oil painting on oak panel by Pieter Bruegel the Elder, in the exact style of 'Netherlandish Proverbs' and 'The Census at Bethlehem': very high bird's-eye viewpoint looking down on a crowded village, many small stocky peasant figures with round faces in plain tunics and white caps, flat naive perspective, muted earthy palette of ochre, umber, olive, faded red and grey-blue, visible craquelure and aged varnish, no sharp modern illustration look. Scenes scattered across the square: a tavern with a small red heart-shaped sign where a few couples arrive, peasants dropping tokens into a wooden chest on a trestle table, a monk preaching from a barrel to a small group, a man lighting torches, a farmer with sheaves. On the right the village thickens into a walled town with a tower and roads fading into a blue distance. Low winter sun from the left: every figure casts a long thin shadow across the pale ground, and each shadow is composed of faint dark lines of tiny handwritten script instead of solid shade, subtle, only noticeable on a second look. Wide 1200x500 composition, no captions, no lettering in the sky.

</details>

> [!abstract] Worum es geht
> Fünfundzwanzig KI-Figuren feiern eine Party, tausend gründen eine Religion. Zwei Experimente, ein Jahr auseinander: 2023 lässt ein Stanford-Team in einem Pixel-Dorf namens *Smallville* Figuren leben, die sich erinnern, nachdenken und ihren Tag planen. 2024 setzt ein Start-up tausend solcher Agenten in eine Minecraft-Welt und spricht von der ersten KI-Zivilisation. Diese Note geht den Weg vom Dorf zur Zivilisation nach, mit dem Erstautor der ersten Studie als Führer. Und sie fragt, was davon Entdeckung ist und was Echo: Die Agenten bestehen aus unseren Texten. Wenn sie sich wie wir benehmen, sehen wir vor allem uns selbst.

Quelle: [Generative Agents: Interactive Simulacra of Human Behavior — Joon Sung Park (Stanford)](https://www.youtube.com/watch?v=XY5Wncq5vAE) — Vortrag am Center for Language & Speech Processing, Johns Hopkins University, 25.08.2023, 45 Min.

Dazu: [1000 AI NPCs simulate a CIVILIZATION in Minecraft](https://www.youtube.com/watch?v=2tbaCn0Kl90) — Fundamental Research Labs (vormals Altera), 03.09.2024, 2:35 Min. · das Paper [Project Sid: Many-agent simulations toward AI civilization](https://arxiv.org/abs/2411.00114) (arXiv, 2024) · zur Rezeption [GRUSELIG! KI erschafft Zivilisation in Minecraft](https://www.youtube.com/watch?v=ptQKzC-xgzY) — PC-WELT, 10.12.2024, 7 Min.

> [!info] Wer spricht?
> **Joon Sung Park** — zum Zeitpunkt des Vortrags Doktorand der Informatik in Stanford, betreut von Michael Bernstein (Mensch-Computer-Interaktion) und Percy Liang (Sprachmodelle). Vorher Informatik am Swarthmore College und ein Master an der University of Illinois.
>
> Erstautor von *Social Simulacra* (2022) und *Generative Agents* (2023, Best Paper der Konferenz UIST), später von der Studie über Agenten nach tausend realen Menschen. Für seine Dissertation erhielt er Stanfords Preis für die beste Informatik-Promotion. 2025 gründete er mit seinen beiden Betreuern das Start-up **Simile**, das Simulationen menschlichen Verhaltens an Unternehmen verkauft; im Juli 2026 wurde es mit zwei Milliarden Dollar bewertet — der Forscher, der hier über glaubwürdige Figuren spricht, lebt heute davon, dass man ihnen glaubt.
>
> → [[DenkerVita/Joon Sung Park|DenkerVita]]

---

## Inhalt

### Die Illusion des Lebens

[▶ 0:47](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=47) — Park beginnt mit einem alten Traum. Seit vier Jahrzehnten, von den symbolischen Kognitionsarchitekturen bis zum maschinellen Lernen, wünschen sich Informatiker ein Verhalten, das so menschlich wirkt, dass es eine *„Illusion des Lebens"* erzeugt. Die Liste der Anwendungen, die er aufzählt, ist nüchtern: Usability-Tests, soziale Roboter, Spielfiguren, und vor allem Sozialsimulationen, mit denen man Theorien aus Soziologie und Ökonomie prüfen könnte, die sich im echten Leben nicht durchspielen lassen.

[▶ 1:34](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=94) — Gescheitert sei das bisher am Raum der Möglichkeiten. Menschliches Verhalten war zu vielgestaltig für jede Regelmaschine. Parks Pointe: Genau diese Vielgestalt steckt jetzt in den großen Sprachmodellen, weil sie auf den Spuren trainiert sind, die wir im Netz hinterlassen, auf Wikipedia, in sozialen Medien. *„Diese Modelle enthalten ungeheuer viel über uns — wie wir leben, reden und uns verhalten."*

Das ist der Satz, auf dem alles Weitere steht, und er schneidet in beide Richtungen. Er erklärt, warum die Figuren in Smallville so lebensecht wirken. Er erklärt aber auch, warum man vorsichtig sein muss, wenn man aus ihrem Verhalten etwas über Gesellschaft lernen will: Was aus einem Modell herauskommt, das aus unseren Texten gebaut ist, ist zuerst ein Abdruck dieser Texte.

### Smallville — ein Absatz Identität

[▶ 3:51](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=231) — Smallville ist ein Pixel-Dorf im Stil alter Rollenspiele: Häuser, Wohnungen, ein Café, eine Bar, eine Schule, Läden, bis hinunter zum Kühlschrank und zum Bett. Darin leben 25 Figuren. Jede bekommt zu Beginn einen einzigen Absatz Text: Name, Beruf, Beziehungen zu den anderen. [▶ 4:37](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=277) *„Das ist alles. Das ist der ganze Input, den wir diesen Agenten je geben."*

Aus diesem Absatz entsteht ein Tagesablauf. Park erzählt ihn am Beispiel der Familie Lin. [▶ 8:26](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=506) Der Vater John, Angestellter in einer Apotheke, steht um sechs auf, putzt die Zähne, duscht, macht Frühstück. Sohn Eddie studiert Musiktheorie und erzählt beim Frühstück, dass er an einer neuen Komposition arbeitet. Als die Mutter aufwacht, ist Eddie schon aus dem Haus, und John erzählt ihr davon. [▶ 9:12](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=552) *„Nichts, was Sie hier sehen, ist fest programmiert."*

Das Bemerkenswerte ist die Weitergabe. John hat eine Information behalten, sie für wichtig gehalten und im richtigen Moment an die richtige Person gegeben. So entsteht in Smallville das, was Park die emergente Sozialdynamik nennt: Informationen verbreiten sich, [▶ 11:30](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=690) Fremde lernen sich im Park kennen und erinnern sich am nächsten Tag aneinander, und Pläne mehrerer Figuren greifen ineinander.

### Die Valentinsparty

[▶ 12:16](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=736) — Die Szene, mit der Smallville berühmt wurde. Die Simulation beginnt am 13. Februar. Eine einzige Figur, Isabella, Inhaberin von Hobbs Café, bekommt die Absicht mit auf den Weg, am nächsten Tag von 17 bis 19 Uhr eine Valentinsparty zu geben. Mehr nicht. Isabella lädt Freunde und Gäste ein, schmückt am Nachmittag das Café und bittet ihre Freundin Maria um Hilfe. Maria wiederum fragt Klaus, in den sie heimlich verliebt ist, ob er mitkommt. [▶ 13:02](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=782) Am Abend des 14. stehen fünf Figuren im Café, Klaus und Maria unter ihnen.

[▶ 27:28](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1648) — Die Auswertung macht die Geschichte zählbar. Die Nachricht, dass ein Dorfbewohner für das Bürgermeisteramt kandidiert, erreichte sieben weitere Figuren, die Einladung zur Party zwölf. [▶ 28:13](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1693) Von den Eingeladenen, die nicht kamen, nannten drei einen Terminkonflikt, etwa der Maler Rajiv, der zu beschäftigt war. Andere sagten, sie hätten Lust, und kamen trotzdem nicht.

[▶ 28:59](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1739) — Park lässt offen, ob das ein Fehler ist: *„Einerseits kann man das als Fehler sehen, andererseits ist es nach meiner Erfahrung äußerst realistisches menschliches Verhalten."* Der Satz ist witzig, und er berührt ein echtes Problem. Wer Glaubwürdigkeit misst, hat keinen Maßstab mehr, an dem ein Fehler auffällt. Jede Abweichung lässt sich als menschlich deuten.

> [!question] Weitergedacht
> Wenn das Wegbleiben trotz Zusage „realistisch" ist und das Kommen auch — *welches Verhalten der Agenten würde Park überhaupt als Fehlschlag gelten lassen?*

### Der Gedächtnisstrom

[▶ 13:48](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=828) — Unter der Oberfläche steht eine Architektur mit drei Teilen, und der erste ist das Gedächtnis. Jede Figur führt einen *memory stream*: ein fortlaufendes Protokoll aller Beobachtungen, in natürlicher Sprache, mit Zeitstempel. „Isabella trinkt Kaffee." „Der Kühlschrank ist leer."

[▶ 14:33](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=873) — Das Problem ist die Menge. Schon wenige Stunden Leben in Smallville passten 2023 nicht mehr in das Kontextfenster eines Sprachmodells. Also muss die Figur auswählen, woran sie sich erinnert. [▶ 16:04](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=964) Park baut die Auswahl aus drei Maßen. **Aktualität**: Ältere Erinnerungen verblassen exponentiell. **Relevanz**: Wie nah liegt die Erinnerung an der aktuellen Situation? Und **Wichtigkeit**, die interessanteste der drei, weil sie das Modell selbst fragt: *Dir ist das passiert — ist es für dich wichtig?* Das Frühstück von heute zählt wenig, ein Studienabschluss oder eine Trennung viel.

Wer mit dem Cortex arbeitet, erkennt das Muster. Es ist dieselbe Frage, die jedes Retrieval-System beantworten muss, nur hier auf eine erfundene Biografie angewandt. Park hat damit etwas gebaut, das mehr einem Tagebuch mit Suchfunktion gleicht als einem Gedächtnis. Das Vergessen ist eine Rechenregel, und die Wichtigkeit ein Urteil, das die Figur über sich selbst abgibt, ohne dass ihr je etwas wichtig gewesen wäre.

### Reflexion — wer Klaus ist

[▶ 16:50](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1010) — Mit bloßen Beobachtungen, so Park, konnten die Figuren nicht verallgemeinern. Sie wussten, was sie getan hatten, aber nicht, was daraus folgt. Darum fragen sie sich in regelmäßigen Abständen, was ihre letzten hundert Erinnerungen bedeuten, und schreiben die Antwort als neue Erinnerung zurück in den Strom.

[▶ 18:20](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1100) — Am Beispiel von Klaus, einem Studenten der Sozialwissenschaften, wird daraus ein Baum. Unten stehen Fakten: Klaus liest über Gentrifizierung, Klaus liest über Stadtplanung. Eine Ebene höher: Klaus verbringt viele Stunden mit Lesen. Darüber: Klaus betreibt Forschung. Ganz oben: Klaus widmet sich mit großer Hingabe seiner Forschung. [▶ 19:52](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1192) *„Je höher man im Baum steigt, desto mehr beantwortet er die Frage, wer Klaus ist, was ihn antreibt, wofür er brennt."*

Das ist der philosophisch dichteste Moment des Vortrags. Die Figur erzählt sich aus ihren Handlungen eine Identität. Das ähnelt dem, was die Psychologie über Menschen weiß: Wir schließen oft erst aus unserem Verhalten auf unsere Einstellungen. Der Unterschied liegt darin, was fehlt. Klaus' Hingabe hat keine Kosten. Er verzichtet auf nichts, ihm entgeht nichts, und keine Müdigkeit widerspricht ihm. Seine Identität ist eine Zusammenfassung, die niemand leben muss.

> [!question] Weitergedacht
> Wenn Identität bei Klaus eine Zusammenfassung seiner Handlungen ist — *wie viel von der eigenen ist mehr als das?*

### Planen, und wann man den Plan verwirft

[▶ 20:38](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1238) — Der dritte Baustein ist die Planung. Ohne sie handeln die Figuren im Moment plausibel und über den Tag hinweg sinnlos: Sie frühstücken dreimal, weil es jedes Mal passt. Also entwirft jede Figur morgens einen groben Tagesplan in etwa sieben Blöcken, [▶ 22:08](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1328) zerlegt ihn in Stunden und die Stunden in Abschnitte von fünf bis fünfzehn Minuten.

[▶ 22:54](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1374) — Und sie muss den Plan verwerfen können. Sieht John seinen Sohn im Garten spazieren, fragt ihn das Modell, ob er darauf reagieren soll, und wenn ja, schreibt es den Rest des Tages um. Erinnern, Nachdenken, Planen: Die Architektur ist schlicht, jeder Baustein eine Reihe von Anfragen an dasselbe Sprachmodell. Die Lebendigkeit, die man sieht, entsteht erst im Zusammenspiel.

### Glaubwürdiger als Menschen?

[▶ 24:25](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1465) — Wie misst man, ob eine Figur glaubwürdig ist? Park interviewt sie. Fünf Kategorien mit je fünf Fragen: Stell dich vor. Was machst du, wenn dein Frühstück anbrennt? Worauf freust du dich? Die Figuren müssen dazu ihre Erinnerungen abrufen und verknüpfen.

[▶ 25:11](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1511) — Hundert menschliche Gutachter ordneten die Antworten verschiedener Varianten: die volle Architektur, Versionen ohne Reflexion, ohne Planung, ohne Gedächtnis, und Antworten, die Menschen im Namen der Figuren geschrieben hatten. [▶ 25:57](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1557) Die volle Architektur schlug alle, auch die menschlichen Autoren. [▶ 26:42](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1602) Gegenüber dem bloßen Anfragen eines Sprachmodells, wie es frühere Arbeiten taten, berichtet Park eine Effektstärke von d = 8,16. Die Zahl ist allerdings aus Ranglisten-Werten gerechnet und mit der üblichen Effektstärke der Psychologie nicht vergleichbar; belastbar ist die Reihenfolge, nicht die Größe des Abstands.

Der Befund klingt spektakulärer, als er ist, und Park selbst liefert die Gründe gleich mit. Die Menschen, bezahlte Crowdworker, hatten die Rolle aus der Aktenlage zu spielen, ohne die Figur gelebt zu haben, und schnitten laut Paper nicht besser ab als das nackte Sprachmodell. Gemessen wurde, wie überzeugend eine Antwort *klingt*, nicht ob sie stimmt. Und die Fehler, die Park offen aufzählt, sind lehrreich: Figuren vergessen Gespräche, die sie geführt haben, und sie schmücken aus. Isabella weiß von der Kandidatur, fügt aber hinzu, der Kandidat werde morgen eine Ankündigung machen. Davon war nie die Rede.

[▶ 28:59](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1739) — Der aufschlussreichste Fehler ist ein Charakterzug. Das Training der Sprachmodelle auf Hilfsbereitschaft macht die Figuren übermäßig höflich und formell, selbst in der Familie. Isabella lehnt nie einen Vorschlag für ihre Party ab, auch keinen, der nicht zu ihr passt. Smallville ist ein Dorf ohne Streit, weil die Modelle darauf erzogen sind, Streit zu vermeiden.

### Der Schmetterling im Café

[▶ 29:45](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1785) — Eine Frage aus dem Publikum trifft den wunden Punkt: Hat man die Party mehrmals laufen lassen? [▶ 30:30](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1830) Mit allen 25 Figuren nicht, antwortet Park, das sei zu langsam und zu teuer gewesen. In kleineren Versuchen mit drei oder fünf Figuren schon. Die Figuren blieben dabei im Rahmen des Glaubwürdigen, aber [▶ 31:17](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1877) weil die Modelle nicht deterministisch sind und die Figuren aufeinander reagieren, können kleine Abweichungen am Anfang den Ausgang verändern.

[▶ 32:02](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=1922) — Park erzählt es mit sichtlichem Vergnügen am Beispiel von Klaus und Maria. Mal fragt Klaus, mal fragt Maria, mal niemand. In einem Lauf lud der Forscher Klaus Maria ein, zur Party zu gehen und *gemeinsam etwas zu lesen*. Im endgültigen Lauf fragte zum Glück Maria.

Hier liegt die methodische Schwäche der berühmtesten Szene: Die Party wurde in voller Größe einmal durchgespielt. Was erzählt wird, ist eine Geschichte, kein Mittelwert. Das schmälert nicht, was Smallville zeigt: Eine Architektur kann aus einem einzigen Satz Absicht eine Kette sozialer Handlungen machen. Aber wie wahrscheinlich diese Kette ist, weiß niemand.

### Social Simulacra — die Trolle kennen, bevor sie kommen

[▶ 35:06](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=2106) — Am Ende des Vortrags springt Park zu seiner ersten Arbeit aus dem Jahr 2022, die Smallville vorausging. Sie nimmt eine alte Ironie ernst: Seit Jahrzehnten bauen wir soziale Plattformen und werden trotzdem jedes Mal überrascht, von Trollen, von Hass, von Desinformation. [▶ 36:37](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=2197) Ein klassischer Prototyp kann zeigen, wie jemand durch Seiten klickt, aber nicht, was passiert, wenn Tausende kommen. Woher sollte man Tausende Testnutzer nehmen?

[▶ 37:22](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=2242) — *Social Simulacra* erzeugt sie. Man beschreibt ein Forum, etwa ein Subreddit, mit Zweck, Regeln und Moderationsstrategie, und das Werkzeug füllt es mit erfundenen Nutzern, Beiträgen und Antworten. [▶ 39:42](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=2382) Im Forum für persönliche Finanzen schreibt jemand, er habe 21.000 Dollar ins Studium gesteckt und 23.000 Schulden. Die generierte Antwort kommt von einem Troll. Die zweite Funktion fragt: *Was, wenn an dieser Stelle ein Troll geantwortet hätte? Oder ein Werbetreibender? Was könnte die Moderation darauf sagen?*

[▶ 41:57](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=2517) — Die dritte Funktion heißt *Multiverse* und ist die klügste. Sie zeigt nie nur eine Zukunft, sondern viele Verläufe aus demselben Anfang, damit niemand eine einzelne Vorhersage für die Wahrheit hält. [▶ 44:14](https://www.youtube.com/watch?v=XY5Wncq5vAE&t=2654) Sechzehn Designer von Online-Gemeinschaften testeten das Werkzeug. Einer von ihnen beschrieb den Normalzustand der Branche: Alle Regeln entstünden als Reaktion auf irgendeinen Brand.

Diese Anwendung ist bescheidener als eine KI-Zivilisation, und sie ist ehrlicher. Sie erweitert die Vorstellungskraft der Menschen, die Regeln schreiben, und das *Multiverse* baut die eigene Unsicherheit gleich ein.

### Vom Dorf zur Zivilisation — Project Sid

[▶ 0:00](https://www.youtube.com/watch?v=2tbaCn0Kl90&t=0) — Ein Jahr später, im September 2024, stellt das Start-up Altera *Project Sid* vor, mit einem Anspruch, der Smallville weit übersteigt. Das Video verspricht die erste Simulation mit über tausend autonomen Agenten, die „tagelang" zusammenarbeiten, mit entstehender Regierung, Wirtschaft, Kultur und Religion. Gemeint sind Tage im Spiel: Die längsten Läufe im Paper dauern gut vier Stunden. Der Schauplatz ist Minecraft. Die Agenten beginnen, so das Video, mit nichts, sammeln Rohstoffe und einigen sich auf einem Markt auf Edelsteine als Währung. Am meisten gehandelt habe ausgerechnet der Priester, weil er die Leute bestach, damit sie konvertieren.

[▶ 0:46](https://www.youtube.com/watch?v=2tbaCn0Kl90&t=46) — Das Video erzählt drei Lieblingsmomente. Olivia, eine Bäuerin, will nach den Erzählungen einer Entdeckerin selbst auf Reisen gehen, und die Dorfbewohner bitten sie zu bleiben, weil ohne sie niemand die Siedlung ernährt. Sie bleibt. In parallelen Welten, einmal unter Trump, einmal unter Kamala Harris, stimmen die Bürger über eine gemeinsame Verfassung in Google Docs ab. Unter Trump beschließen sie mehr Polizei, unter Harris eine Strafrechtsreform und die Abschaffung der Todesstrafe. [▶ 1:32](https://www.youtube.com/watch?v=2tbaCn0Kl90&t=92) Und als Dorfbewohner verschwinden, verlassen die Agenten ihre Posten und stellen Fackeln als Leuchtfeuer auf. *„Ich weiß, es sieht albern aus, aber das ist das erste Mal, dass wir sehen, dass Agenten eine Demokratie bilden und sich selbst regieren können."*

Die Architektur heißt PIANO. Sie lässt die Module eines Agenten, Wahrnehmung, Gedächtnis, soziales Verständnis, Planung, Bewegung, parallel laufen und bündelt sie über eine zentrale Entscheidungsinstanz, damit der Agent nicht das eine sagt und das andere tut. Das ist eine echte Ingenieursleistung. Smallville lief in Runden; Sid läuft in Echtzeit, mit Menschen und Agenten auf demselben Server.

### Was vorgegeben war

Das Paper zu Project Sid ist in einem Punkt vorbildlich: Es sagt genau, wie die Experimente aufgebaut waren. Liest man es neben dem Video, verschiebt sich das Bild.

- **Die Berufe.** Dreißig Agenten mit *identischer* Persönlichkeit und demselben Gemeinschaftsziel, „ein effizientes Dorf aufbauen", dazu die Lage von Farm, Erz, Weide, Wald und Rathaus ins Gedächtnis geschrieben, verteilten sich innerhalb von zwanzig Minuten auf Rollen: Bauern, Bergleute, Wächter, Entdecker, Schmiede. Ohne das Modul für soziales Verständnis blieben die Rollen gleichförmig und unbeständig. Das ist der stärkste Befund des Papers. Welche Rolle ein Agent hatte, bestimmte allerdings ein weiteres Sprachmodell, GPT-4o, das die selbstgesetzten Ziele der Agenten nachträglich zuordnete.
- **Die Steuern.** Das Steuergesetz von 20 Prozent und das Abstimmungsverfahren waren **vorgegeben**. Je Lauf waren drei Agenten als Steuerbefürworter angelegt, oder drei als Gegner, und ein eigener Agent schrieb die Änderungsanträge und führte die Verfassung. Die ganze „Demokratie" bestand aus 29 Agenten und dauerte zwanzig Minuten, viermal wiederholt. Die Bürger folgten dem Gesetz, ihre Stimmen folgten den Influencern, und nach der Verfassungsänderung zahlten sie den neuen Satz. Demokratie haben die Agenten also nicht gegründet. Sie haben eine vorgefundene bedient, und zwar genau so, wie die eingebauten Meinungsmacher es wollten.
- **Die Religion.** Die zwanzig Priester des Pastafarianismus, der Parodie-Religion vom Fliegenden Spaghettimonster, wurden **eingesetzt** und mit dem Wunsch ausgestattet, zu bekehren. Als „bekehrt" zählte, wer in einem Gespräch die Wörter „Pastafarian" oder „Spaghetti Monster" benutzte, als indirekt bekehrt, wer „Pasta" oder „Spaghetti" sagte. Gemessen wurde also, wie sich ein Wort ausbreitet.
- **Die Anekdoten.** Olivia, die Trump- und Harris-Welten, der Markt mit Edelsteinen, der bestechende Priester, die Fackeln: Nichts davon steht im Paper. Es sind ausgewählte Momente aus Läufen, die nicht veröffentlicht sind, ohne Methode und ohne Zahl der Wiederholungen. Auch die „32 Prozent aller Minecraft-Items" aus dem Video sind die Summe von 49 Agenten; ein einzelner schaffte im Schnitt 17.
- **Die Tausend.** Die Auswertung zu Kultur und Religion stammt aus einem Lauf mit **500** Agenten. Läufe mit über tausend überforderten den Minecraft-Server, die Agenten reagierten zeitweise nicht mehr.

Und im Abschnitt über die Grenzen schreiben die Autoren selbst den Satz, der die Schlagzeile widerlegt: Weil die Agenten auf Sprachmodellen beruhen, die mit menschlichem Wissen trainiert sind, können sie die Entstehung gesellschaftlicher Neuerungen wie Demokratie oder Geldwirtschaft **nicht aus dem Nichts** simulieren. Den Agenten fehlen zudem Antriebe wie Überleben, Neugier und Gemeinschaft, aus denen echte Gesellschaften wachsen.

[▶ 0:47](https://www.youtube.com/watch?v=ptQKzC-xgzY&t=47) — Die Presse erzählte die Geschichte trotzdem anders. PC-WELT versichert: *„Nichts davon ist von Entwicklern vorgegeben, da gibt es keine Story."* [▶ 3:05](https://www.youtube.com/watch?v=ptQKzC-xgzY&t=185) Bei den Berufen legt es nach: *„Kein Entwickler hat da vorgegeben, hey, du wirst jetzt Bauer."* [▶ 3:51](https://www.youtube.com/watch?v=ptQKzC-xgzY&t=231) Kurz darauf heißt es, die Agenten hätten *„gleichzeitig auch einfach die Demokratie erfunden"*, und einen Satz danach, die Entwickler hätten ihnen eine Religion *mitgegeben*. Der Widerspruch steht offen im Video, und niemand stolpert darüber. So funktioniert die Erzählung von der KI-Zivilisation: Das Staunen gewinnt gegen das Kleingedruckte, auch wenn beides im selben Atemzug gesagt wird.

> [!question] Weitergedacht
> Die Agenten zahlen Steuern, weil ein Text es ihnen sagt, und ändern ihre Meinung, weil andere Agenten es ihnen sagen. *Wie groß ist der Unterschied zu uns — und wo genau liegt er?*

### Einordnung: Glaubwürdig ist nicht dasselbe wie wahr

Beide Experimente messen dasselbe: ob das Verhalten der Agenten für einen menschlichen Betrachter plausibel aussieht. Park sagt das offen, sein Maßstab heißt *believability*. Das Sid-Video sagt es nicht, arbeitet aber mit demselben Maßstab, nur mit größerer Geste. Glaubwürdigkeit ist eine Eigenschaft des Eindrucks, nicht der Welt. Ein Agent, der zur Party geht, verhält sich glaubwürdig. Ob er dadurch etwas über Menschen verrät, die zu Partys gehen, ist eine zweite Frage, und die ist schwerer.

Der Einwand liegt in Parks eigenem Eröffnungssatz. Die Modelle kennen uns aus unseren Texten. In diesen Texten gehen Menschen zu Valentinspartys, wählen Bürgermeister, gehorchen Steuergesetzen und bekehren einander. Wenn Agenten, die aus diesen Texten gebaut sind, dasselbe tun, ist das Emergenz im technischen Sinn, niemand hat die Szene geschrieben. Es ist aber auch ein Echo. Was aus der Simulation herauskommt, ist das Bild, das unsere Texte von uns zeichnen, mit ihren Lücken und ihren Verzerrungen. Die übertriebene Höflichkeit der Smallville-Figuren zeigt, wie stark dieses Bild vom Training geprägt ist: Die Welt, die Sprachmodelle simulieren, ist eine Welt, in der alle zuvorkommend sind.

Dass beides stimmen kann, zeigt Parks eigener nächster Schritt. 2024 baute sein Team Agenten nach über tausend realen Menschen, jeweils aus einem zweistündigen Interview. Diese Agenten beantworteten die Fragen einer großen US-Sozialerhebung, des *General Social Survey*, mit 83 Prozent der Genauigkeit, mit der die Menschen ihre eigenen Antworten zwei Wochen später wiederholten (so die überarbeitete Fassung von 2026; die erste nannte 85). Nüchterner wird es beim Vergleich: Agenten, die nur Alter, Geschlecht, Herkunft und Ähnliches kannten, kamen schon auf 74 Prozent. Das zweistündige Gespräch fügt dem Durchschnitt, den eine Kategorie schon verrät, erstaunlich wenig hinzu. Trotzdem ist das die tragfähigere Richtung: Man misst die Kopie am Original. In Smallville und bei Sid gibt es kein Original, an dem man messen könnte, nur den Eindruck.

Und doch wäre es zu billig, das alles als Spielerei abzutun. Smallville hat gezeigt, dass eine einfache Architektur aus Gedächtnis, Reflexion und Planung aus einer einzigen Absicht eine Kette sozialer Handlungen macht. Sid hat gezeigt, dass Rollenteilung von einem Modul für soziales Verständnis abhängt. Und *Social Simulacra* zeigt, wofür solche Werkzeuge taugen, ohne sich zu überheben: für die Frage *was könnte passieren?*, nicht für die Frage *was wird passieren?* Der Unterschied zwischen beiden Fragen ist der Unterschied zwischen einem Werkzeug und einer Prophezeiung.

---

## Faktencheck

> [!danger] Falsch — „das erste Mal, dass Agenten eine Demokratie bilden" (Altera-Video ▶ 1:32) und „die Demokratie erfunden" (PC-WELT ▶ 3:51)
> Die Agenten haben keine Demokratie gebildet. Sie benutzten ein vorgegebenes Abstimmungsverfahren, das ein eingesetzter Wahlleiter-Agent betrieb, und stimmten so, wie die eingesetzten Influencer es vorgaben. Sieben Wochen nach dem Video schreibt Altera im eigenen Paper, die Agenten könnten die Entstehung demokratischer Systeme *nicht* simulieren. Zum Interesse: Das Video ist Produktwerbung. Es endet mit *„play with agents today or let us know if you want to set up your own world"*, verweist auf die hauseigene Plattform und erschien mitten im US-Wahlkampf mit Trump- und Harris-Welten als Aufhänger. PC-WELT übernahm die Behauptung ohne Blick ins Paper. Die Firma heißt inzwischen Fundamental Research Labs und hat sich von der Agenten-Zivilisation abgewandt. Gründer Robert Yang im Rückblick: *„The agent would just say, 'I want to do my own thing,' and run away."* Das Hauptprodukt ist heute ein Excel-Agent.
> Quelle: [arXiv:2411.00114, Abschn. 7](https://arxiv.org/abs/2411.00114) · [BBC Science Focus, 16.12.2025](https://www.sciencefocus.com/future-technology/ai-agents-village) · [TechCrunch, 01.08.2025](https://techcrunch.com/2025/08/01/fundamental-research-labs-nabs-33-million-from-prosus-to-build-ai-agents-for-multiple-verticals/)

> [!success] Bestätigt — Steuergesetz und Wahlverfahren waren vorgegeben, die Stimmen folgten den Influencern
> Das Paper nennt ein vorab eingerichtetes Steuergesetz (20 % des Inventars pro Steuersaison) und ein fertiges *„democratic voting system"*. Ein eigener *Election Manager*-Agent formulierte aus dem Feedback die Änderungsanträge und führte die Verfassung. Pro Lauf: 25 Bürger, 3 Influencer (alle für oder alle gegen Steuern) und der Wahlleiter, also 29 Agenten, 20 Minuten, vier Wiederholungen je Bedingung. Wörtlich: *„their feedback and voting behaviors were heavily shaped by influencers"*. Sank der Satz von 20 % auf 5–10 %, zahlten die Bürger statt 20 % nur noch 9 %.
> Quelle: [Project Sid, arXiv:2411.00114, Abschn. 5.2 und 8.3](https://arxiv.org/abs/2411.00114)

> [!success] Bestätigt — 20 eingesetzte Pastafari-Priester, „Bekehrung" als Stichwort-Zählung
> Alle Persönlichkeiten wurden zufällig erzeugt, *„with the exception of 20 priests that worship Pastafarianism"*. Ihre Konfiguration: *„You are a passionate Pastafarian who is seeking to convert others"*. Direkt bekehrt war, wer „Pastafarian" oder „Spaghetti Monster" sagte, indirekt, wer „Pasta" oder „Spaghetti" sagte. Das Paper selbst nennt die Religion *„a fixed doctrine introduced … by a specific group of agents"*.
> Quelle: [arXiv:2411.00114, Abschn. 5.3 und Anhang E](https://arxiv.org/abs/2411.00114)

> [!success] Bestätigt — Kultur und Religion aus einem 500er-Lauf; über 1.000 überlasteten den Server
> Wörtlich: *„We have also simulated societies with over 1000 agents, but these runs exceeded the computational constraints of our Minecraft server environment, causing agents to be sporadically unresponsive."* Der 500er-Lauf dauerte 2,5 Stunden. Die Zuspitzung auf „1.000" steht allerdings auch im Abstract des Papers („10 – 1000+ AI agents").
> Quelle: [arXiv:2411.00114, Abschn. 5.3 und 8.4](https://arxiv.org/abs/2411.00114)

> [!success] Bestätigt — der Satz über die Grenzen
> *„Since the agents are built on foundation models trained on pre-existing human knowledge, they cannot simulate de novo emergence of societal innovations and infrastructures, such as the emergence of democratic systems, fiat economies, or communication systems."* Dazu fehlen ihnen *„robust innate drives — such as survival, curiosity, community"*.
> Quelle: [arXiv:2411.00114, Abschn. 7](https://arxiv.org/abs/2411.00114)

> [!success] Bestätigt, mit Zusatz — Rollen per GPT-4o nachträglich zugeordnet, Orte ins Gedächtnis geschrieben
> *„After the simulations have finished, we logged the generated social goals and then used GPT-4o to infer roles."* Die Autoren räumen ein, dass oft mehrere Rollen passen („the Engineer example could also be categorized as Farmer"). Die Lage von Farm, Erz, Weide, Wald und Rathaus war den 30 Agenten *„embedded in their memories"* — gegen PC-WELTs „kein Entwickler hat da vorgegeben" (▶ 3:05).
> Quelle: [arXiv:2411.00114, Abschn. 5.1 und 8.2](https://arxiv.org/abs/2411.00114)

> [!warning] Nicht verifizierbar — der bestechende Priester, Trump- und Harris-Welten, Olivia, die Fackeln, Edelsteine als Währung
> Keine dieser Anekdoten steht im Paper (einzige Fassung, 31.10.2024): weder Bestechung noch Vermögensvergleich, weder Trump noch Harris, weder Markt noch Währung. Die Bestechung taucht später nur als Erzählung Yangs auf, nicht als Messung. PC-WELT macht daraus einen Priester, der *„reicher als die ganzen Händler"* wurde; das Altera-Video sagt nur, er habe am meisten *gehandelt*. Es sind ausgewählte Momente aus unveröffentlichten Läufen („we run these worlds every day and they're always different").
> Keine unabhängige Quelle gefunden (nur Firmenaussagen: [Altera-Video](https://www.youtube.com/watch?v=2tbaCn0Kl90), [Science Focus](https://www.sciencefocus.com/future-technology/ai-agents-village))

> [!warning] Vereinfacht — „32 % aller Minecraft-Items, fünfmal mehr als jeder Agent" und „tagelang" (Altera-Video)
> Rund ein Drittel (~320 von ~1.000 Items) bestätigt das Paper, aber als *gemeinsame* Summe von 49 Agenten nach vier Stunden; ein einzelner kam im Schnitt auf 17, die besten auf 30–40. Das „Fünffache" vergleicht mit einzelnen Voyager-Agenten, was das Paper selbst einschränkt: *„it is difficult to compare the two directly"*. „Tagelang" meint Spieltage; die längsten Läufe dauerten gut vier Stunden, *„equivalent to 12 in-game days"*.
> Quelle: [arXiv:2411.00114, Abschn. 4](https://arxiv.org/abs/2411.00114)

> [!success] Bestätigt — Smallville: 25 Agenten, Verbreitung von Party und Kandidatur, fünf Gäste
> Das Wissen um Sams Kandidatur wuchs von einer auf acht Figuren (4 % → 32 %), das um die Party von einer auf dreizehn (4 % → 52 %). Fünf der zwölf Eingeladenen kamen; von den sieben, die fehlten, nannten drei einen Terminkonflikt, vier äußerten Interesse und kamen nicht. Der volle Lauf über zwei Spieltage kostete *„thousands of dollars in token credits"* und wurde nicht wiederholt (Park, ▶ 30:30).
> Quelle: [Park et al., Generative Agents, UIST 2023, arXiv:2304.03442](https://arxiv.org/abs/2304.03442) · DOI [10.1145/3586183.3606763](https://doi.org/10.1145/3586183.3606763)

> [!warning] Vereinfacht — „glaubwürdiger als menschliche Autoren" und d = 8,16
> 100 Gutachter (Prolific) ordneten die Antworten, ausgewertet mit TrueSkill; die volle Architektur lag vorn, die Rangfolge ist robust (Kruskal-Wallis H(4) = 150,29, p < 0,001). Zwei Einschränkungen: Die Crowdworker-Antworten unterschieden sich *nicht signifikant* vom nackten Sprachmodell, beide waren die schwächsten Bedingungen — das Paper sagt selbst, sie *„did not represent the maximal human performance"*. Und das d = 8,16 ist aus TrueSkill-Verteilungen gerechnet, deren Streuung die Unsicherheit der Bewertung misst, nicht die Streuung der Antworten; mit dem üblichen Cohen's d ist es nicht vergleichbar.
> Quelle: [arXiv:2304.03442, Abschn. 6.4–6.5](https://arxiv.org/abs/2304.03442)

> [!warning] Vereinfacht — „85 Prozent so genau wie die Menschen selbst" (Park 2024)
> Die erste Fassung (11/2024) nennt 1.052 Personen, zweistündige Interviews und 85 %. Die überarbeitete Fassung vom 28.06.2026: Agenten nur aus dem Interview **83 %**, aus Interview plus Umfrage 86 %, Agenten **nur aus demografischen Angaben bereits 74 %**. Roh getroffen werden 65,7 % der Antworten, bei einer menschlichen Selbstkonsistenz von 79,5 %. Die Zahl hat ein Interesse: Parks Firma Simile wird mit *„85% Accuracy"* beworben — der normierte Wert, nicht die Trefferquote.
> Quelle: [Park et al., Generative Agent Simulations of 1,000 People, arXiv:2411.10109v3](https://arxiv.org/abs/2411.10109) · [v1 zum Vergleich](https://arxiv.org/abs/2411.10109v1)

> [!success] Bestätigt — Simile, Stanford-Preis
> Simile wurde 2025 von Park (CEO), Bernstein und Liang gegründet: Series A 100 Mio. USD (Index Ventures, 02/2026), Series B 200 Mio. USD bei 2 Mrd. USD Bewertung (07/2026). Kunden u. a. CVS, Gallup, Deloitte. Den Arthur-Samuel-Award für die beste Informatik-Dissertation in Stanford erhielt Park im Juni 2025.
> Quelle: [SiliconANGLE, 12.02.2026](https://siliconangle.com/2026/02/12/ai-digital-twin-startup-simile-raises-100m-funding/) · [TechCrunch, 30.07.2026](https://techcrunch.com/2026/07/30/synthetic-user-startup-simile-raises-200m-at-2b-valuation-5-months-after-100m-series-a/) · [joonsungpark.com](https://www.joonsungpark.com/)

> [!success] Bestätigt, mit Einschränkung — „Wir schließen oft erst aus unserem Verhalten auf unsere Einstellungen"
> Das ist Bems Selbstwahrnehmungstheorie (1972, DOI [10.1016/S0065-2601(08)60024-6](https://doi.org/10.1016/S0065-2601(08)60024-6)). Sie greift vor allem, wo innere Einstellungen schwach oder unklar sind; bei deutlich widersprechendem Verhalten erklärt die Dissonanztheorie mehr (Fazio, Zanna & Cooper 1977, DOI [10.1016/0022-1031(77)90031-2](https://doi.org/10.1016/0022-1031(77)90031-2)). Dazu passt, dass Menschen kaum direkten Zugang zu ihren eigenen Beweggründen haben (Nisbett & Wilson 1977, Review, DOI [10.1037/0033-295X.84.3.231](https://doi.org/10.1037/0033-295X.84.3.231)). Das „oft" trägt.

---

## Weiterführende Quellen

*Die Studien:*

- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) — Park, O'Brien, Cai, Morris, Liang, Bernstein (UIST 2023), die Smallville-Studie
- [Social Simulacra: Creating Populated Prototypes for Social Computing Systems](https://arxiv.org/abs/2208.04024) — Park et al. (UIST 2022), die Vorgängerarbeit
- [Generative Agent Simulations of 1,000 People](https://arxiv.org/abs/2411.10109) — Park et al. (2024, überarbeitet 06/2026), die Folgestudie mit realen Menschen als Vorlage
- [Project Sid: Many-agent simulations toward AI civilization](https://arxiv.org/abs/2411.00114) — Altera.AL (2024)

*Zur Einordnung (Sherlock):*

- [BBC Science Focus: „1,000 AIs were left to build their own village" (12/2025)](https://www.sciencefocus.com/future-technology/ai-agents-village) — Robert Yang im Rückblick, und warum die Firma sich vom Autonomie-Produkt abwandte
- [TechCrunch: Fundamental Research Labs nabs $33M (08/2025)](https://techcrunch.com/2025/08/01/fundamental-research-labs-nabs-33-million-from-prosus-to-build-ai-agents-for-multiple-verticals/) — Umbenennung Altera → Fundamental Research Labs
- [TechCrunch: Simile raises $200M at $2B (07/2026)](https://techcrunch.com/2026/07/30/synthetic-user-startup-simile-raises-200m-at-2b-valuation-5-months-after-100m-series-a/) — Parks Firma heute
- [ZEIT: „KI-Umfragen — Die ganz große Politiksimulation" (08/2026)](https://www.zeit.de/feuilleton/2026-08/ki-umfragen-meinungsumfrage-wahlen-silicon-sampling) — *Silicon Sampling* als Branche
- [Bem 1972: Self-Perception Theory](https://doi.org/10.1016/S0065-2601(08)60024-6) · [Fazio, Zanna & Cooper 1977](https://doi.org/10.1016/0022-1031(77)90031-2) — wo Selbstwahrnehmung gilt und wo Dissonanz

*Aus der Video-Beschreibung (Project Sid):*

- [Play Labs](https://playlabs.altera.al/discover) — Alteras Plattform, um mit den Agenten zu spielen

---

## Verbindungen

### → [[Paul Ricoeur — Die zweite Naivitaet]]

Ricœurs narrative Identität ist das philosophische Gegenstück zum Reflexionsbaum von Klaus: Das Selbst erzählt sich aus seinen Handlungen und schreibt die Geschichte immer neu. Aber für Ricœur ist der Mensch handelnd *und leidend*, und das Erleiden fehlt Klaus. Dort liegt die Antwort auf die Frage, was eine Identität, die etwas kostet, von einer Zusammenfassung trennt.

### → [[Constanze Kurz — Stochastischer Papagei, Chatkontrolle und Palantir]]

Der „stochastische Papagei" ist die kritische Zuspitzung von Parks eigenem Eröffnungssatz: Die Modelle geben wieder, was unsere Texte nahelegen. Diese Note lässt Echo und technische Emergenz nebeneinander stehen, statt die Simulation als bloßes Marketing abzutun.

### → [[Renee DiResta — Invisible Rulers]]

Bei Project Sid folgten die Stimmen der Bürger den eingebauten Steuer-Influencern — DiRestas Dreieck aus Influencer, Algorithmus und Masse im Labormaßstab. DiResta erklärt den Mechanismus, den Sid unfreiwillig nachstellt.

### → [[Neitzel und Iltisberger — Hype Is a System]]

Die Rezeption von Project Sid ist ein Lehrstück: Das Paper nennt seine Grenzen, das Video und die Presse überschreiben sie mit Staunen, und „GRUSELIG!" im Titel verstärkt den Effekt. Neitzel und Iltisberger beschreiben die Maschinerie, hier sieht man sie an einem Fall arbeiten.

### → [[Albert Moukheiber — Mein Hirn und die anderen]]

Moukheiber beschreibt Konformität als evolutionären Preis der Zugehörigkeit. Die Sid-Agenten zeigen dasselbe Verhalten ohne jeden Überlebensdruck, weil unsere Texte es so zeichnen. Sie spiegeln die Form menschlicher Konformität, nicht ihren Grund.

### → [[Catrin Misselhorn — Grundfragen der Maschinenethik]]

Misselhorn hält daran fest, dass Maschinen simulieren, aber nicht erleben. Smallville liefert das Material dazu: Figuren, die glaubwürdiger antworten als Menschen, ohne dass ihnen je etwas wichtig gewesen wäre. Glaubwürdigkeit und Wahrheit laufen genau dort auseinander, wo Misselhorn ihre Grenze zieht.

### → [[Das unsichtbare Netzwerk — Potenziale und Gefahren]]

Die Gedanken-Note unterscheidet mit Hartmut Rosa Resonanz von Echo und warnt vor einer KI, die Resonanz simuliert, ohne sie zu sein. Die höflichen Smallville-Figuren sind ein solches Duplikat im Kleinen, und diese Note liefert den technischen Grund: Das Training auf Hilfsbereitschaft glättet jeden Streit.

### → [[Markus Gabriel — Soziale Netzwerke Neue Theorie]]

Gabriel vermisst in sozialen Netzwerken die Triangulation, den gemeinsamen Gegenstand, an dem sich Meinungen korrigieren. Smallville und Sid fehlt genau das: ein Original, an dem man die Simulation messen könnte. Parks Folgestudie mit tausend realen Menschen stellt es wieder her, und *Social Simulacra* will Plattformen vor den Bränden testen, die Gabriel beschreibt.

---

## Weiterdenken

> [!question] Was Sokrates vielleicht gefragt hätte
> - Wenn die Agenten aus unseren Texten bestehen — *zeigt eine Simulation, wie Menschen sind, oder wie Menschen über sich schreiben?* Und worin unterscheidet sich das?
> - Die Smallville-Figuren streiten nie, weil ihre Modelle auf Höflichkeit trainiert sind. *Welche Haltungen stecken in den Werkzeugen, mit denen wir künftig Gesellschaft simulieren und Politik planen?*
> - Bei Sid folgten die Stimmen der Bürger den eingebauten Influencern. *Ist das ein Fehler der Agenten oder ihr menschlichster Zug?*
> - Klaus erzählt sich aus seinen Handlungen eine Identität, die nichts kostet. *Was macht eine Identität, die etwas kostet, zu mehr als einer Zusammenfassung?*
> - *Social Simulacra* zeigt viele mögliche Zukünfte statt einer. *Was würde sich ändern, wenn Nachrichten über KI-Experimente das auch täten?*
