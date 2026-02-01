# StoryScript

## 1. Opis projekta
StoryScript omogućava kreiranje kompleksnih nelinearnih narativa (tekstualnih RPG igara) - definiciju pravila svijeta, sistema inventara i uslovnih grananja zasnovanih na stanju igrača.
Projekat obuhvata razvoj meta-modela (gramatike), statičku analizu ispravnosti priče (validaciju) i runtime engine-a koji interpretira kod i vodi korisnika kroz igru.

## 2. Tehnologije
- Python 3.x
- textX: Alat za definisanje gramatike i generisanje meta-modela
- Jinja2 Za generisanje HTML/JS verzije igre
- LSP (Language Server Protocol): Omogućava podršku unutar VS Code editora za specifični jezik, uključujući syntax highlighting, error chacking, autocomplite, go to definition

## 3. Primjer
```
adventure IzgubljeniHram

// --- Podešavanja za kreatora ---
define player_hit_range = [1, 10]
define boss_hit_range = [1, 5]

// --- Resursi igrača ---
strength snaga = 25     // Početna izdržljivost
score zlato = 50        // Početni kapital za kupovinu oružja
luck sreca = 5          

// --- Boss statistika ---
boss_strength boss_hp = 40

// --- Predmeti ---
weapon Mac value 15 hit_points 5
weapon Stit value 10 hit_points 3
weapon SvetiGral value 30 hit_points 10

treasure Dijamant weight 5
treasure MisteriozniPoklon weight 3
treasure ZlatnaMaske weight 7

// --- Sobe ---

room Ulaz {
    header "Ulaz u riznicu"
    body "U senci vrata nalaze se osnovni predmeti. Svaki izbor ima cenu u zlatu ili snazi."
    
    option "Kupi Mač (-15 zlata)" [zlato >= 15] take Mac set zlato -= 15 goto HodnikIskusenja
    option "Uzmi Dijamant (+200 zlata, -5 snage)" take Dijamant set zlato += 200 set snaga -= 5 goto HodnikIskusenja
    option "Kreni dalje bez ičega" goto HodnikIskusenja
}

room HodnikIskusenja {
    header "Hodnik Iskušenja"
    body "Pod je prekriven zlatnicima, ali vazduh je težak i iscrpljuje vas. Tvoja snaga: {snaga}."

    option "Pokupi Zlatnu Masku (+150 zlata, -7 snage)" take ZlatnaMaske set zlato += 150 set snaga -= 7 goto OltarSudbine
    option "Uzmi Misteriozni Poklon (-3 snage)" take MisteriozniPoklon set zlato += zlato / 10 + (random(1, 5) * 3) set snaga -= 3 goto OltarSudbine
    option "Ignoriši blago i štedi snagu" goto OltarSudbine
}

room OltarSudbine {
    header "Oltar Sudbine"
    body "Ovaj oltar ne prima zlato, već traži veru. Možeš dobiti veliku sreću ili izgubiti tlo pod nogama."

    // Kockanje sa srecom - direktno utiče na formulu napada u BossAreni
    option "Moli se za sreću (Random -5 ili +15)" set $ishod = random(1, 2) goto IshodMolitve
    option "Samo prođi ka čuvaru" goto Predvorje
}

room IshodMolitve {
    header "Glas Bogova"
    body "Osetili ste promenu u svojoj auri."

    option "Blagoslovljen si! (+15 sreće)" [$ishod == 1] set sreca += 15 goto Predvorje
    option "Proklet si! (-5 sreće)" [$ishod == 2] set sreca -= 5 goto Predvorje
}

room Predvorje {
    header "Dvorana Trgovca"
    body "Poslednja stanica. Ovde tvoje sakupljeno zlato dobija smisao. Tvoje zlato: {zlato}."

    option "Kupi Štit (-10 zlata)" [zlato >= 10] take Stit set zlato -= 10 goto BossArena
    option "Kupi Sveti Gral (-30 zlata)" [zlato >= 30] take SvetiGral set zlato -= 30 goto BossArena
    option "Uđi u arenu spreman" goto BossArena
}

room BossArena {
    header "Finalni Obračun"
    body "Džinovski kameni čuvar se budi! Boss HP: {boss_hp}. Tvoja Snaga: {snaga}. Bonus Sreće: {sreca * 0.1}."

    fight "UDARI BOSS-A" player_hit_range [snaga > 0] win Pobeda loose Poraz
    // navodi se hit range player-a, drugi se automatski uzima kao hit range boss-a
    // fight dio ce engine odraditi
    // nakon svakog udarca korisnika, udara boss
    // prije svog udarca, korisnik moze da izabere nesto od weapon-a i da to iskoristi samo jednom
    // kada korisnik iskoristi weapon, on mu se brise iz inventara
}

room Pobeda {
    header "Pobeda!"
    body "Čuvar se srušio! Izlaziš iz hrama sa {zlato} zlata i legendarnom slavom."
    option "Predji na sledeću avanturu" next SledecaMisija // moze se uvezati vise  avantura
    // u sljedecu avanturu se moze prenijeti sreca i zlato * 0.5, a strength se restartuje
}

room Poraz {
    header "Smrt u hramu"
    body "Tvoje telo je postalo deo temelja hrama."
    option "Vaskrsni na ulazu" goto Ulaz restart  // restart brise inventar i restartuje parametre avanture
}
```

## 4. Opis primjera
Svaka avantura vodi igrača kroz niz soba u kojima donosi odluke koje direktno utiču na njegove resurse, tok igre i konačni ishod.
Igra započinje inicijalizacijom osnovnih parametara, uključujući statistike igrača, boss-a, raspone slučajnih vrednosti, kao i definiciju predmeta i blaga. 
Tok igre je organizovan kroz niz room sekcija, gde svaka soba ima narativni opis i skup mogućih opcija koje igrač može da izabere.
Svaka opcija može imati:
1. uslov za aktivaciju
2. promenu resursa (snaga, zlato, sreća)
3. dodavanje ili uklanjanje predmeta,
4. prelazak u drugu sobu

Igra sadrži i elemente slučajnosti i strategije, naročito u delu vezanom za molitvu na Oltaru sudbine i finalni obračun sa boss-om. 
Završetak avanture zavisi od ishoda borbe, pri čemu igrač može pobediti i nastaviti dalje ili doživeti poraz i restartovati igru.

## 5. Funkcionalnosti
Sistem podržava nekoliko naprednih mehanika koje igru čine dinamičnom:
### 5.1. Globalna podešavanja i resursi
1. Definisanje opsega štete: Mogućnost podešavanja minimalne i maksimalne štete za igrača i boss-a: `player_hit_range` i `boss_hit_range`.
2. Praćenje stanja: Igra u realnom vremenu prati `zlato`, `snagu` i `sreću`, čije se vrednosti menjaju zavisno od akcija igrača.
### 5.2. Ekonomija i inventar
Trgovina: Sobe poput `Ulaz` i `Predvorje` omogućavaju kupovinu predmeta (`weapon`) trošenjem zlata.
Sakupljanje blaga: Igrač može uzeti dragocenosti (`treasure`), ali uz penal (npr. gubitak snage), što stvara moralnu dilemu: da li se isplati rizikovati zdravlje za bogatstvo?
Upravljanje oružjem: Oružja imaju `hit_points` koji povećavaju štetu boss-a u borbi, ali su potrošna (brišu se iz inventara nakon upotrebe).
### 5.3. Dinamičnost i nasumičnost
Uslovne opcije: Neke akcije su dostupne samo ako igrač ima dovoljno resursa (npr. `[zlato >= 15]`).
Randomizacija: Korišćenje funkcije `random(min, max)` za određivanje ishoda molitve ili vrednosti "Misterioznog Poklona".
Logička grananja: Priča se grana na osnovu sreće (`room IshodMolitve`), gde igrač biva "blagosloven" ili "proklet".
### 5.4. Borbeni sistem
Interaktivna borba: Poseban `fight` tip akcije koji inicira automatski ili poluautomatski duel.
Modifikatori borbe: Borba uzima u obzir snagu igrača, HP boss-a i bonus sreće.
Ishodi: Jasno definisani putevi za `Pobeda` (prenos resursa u sledeću misiju) i `Poraz` (mogućnost vaskrsnuća i restarta).
### 5.5. Kontinuitet
Povezivanje avantura: Funkcionalnost `next SledecaMisija` omogućava prenos dela zlata i sreće u naredni nivo, dok se snaga resetuje.


