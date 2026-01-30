# StoryScript

## 1. Opis projekta
StoryScript omogućava kreiranje kompleksnih nelinearnih narativa (tekstualnih RPG igara) - definiciju pravila svijeta, sistema inventara i uslovnih grananja zasnovanih na stanju igrača.
Projekat obuhvata razvoj meta-modela (gramatike), statičku analizu ispravnosti priče (validaciju) i runtime engine-a koji interpretira kod i vodi korisnika kroz igru.
## 2. Tehnologije
- Python 3.x
- textX: Alat za definisanje gramatike i generisanje meta-modela
- Jinja2 Za generisanje HTML/JS verzije igre

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

    fight "UDARI BOSS-A" [snaga > 0] win Pobeda loose Poraz
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
### 4. 1. Varijable kao "Stanje svijeta"
U linijama _var snaga = 10_ i _var zlato = 0_, definišemo globalne registre.
Zlato služi kao skor (score). To je varijabla koju igrač želi da poveća.
Snaga služi kao resurs. To je varijabla koja ograničava šta igrač može da uradi.
### 4.2. "Mač" i mehanika težine
U gramatici je definisano: _item Mac weight 15_. Kada igrač izabere opciju: _option "Uzmi mac" goto Hodnik take Mac set zlato = 100_
dešavaju se tri stvari odjednom:
- Promjena lokacije: Igrač se seli u Hodnik.
- Inventory update: U listu predmeta mu se dodaje Mac .
- Variable update: Njegovo zlato skače sa 0 na 100.
## 5. Funkcionalnosti
### 5.1. Definicija gramatike
Izrada .tx fajla sa pravilima
### 5.2. Statička analiza - implemntacija validatora koji provjerava:
- Postojanje svih ciljnih soba (target=[Room]).
- Ciklične reference koje mogu blokirati igru.
- Da li težina predmeta prelazi kapacitet ako se definiše limit.
### 5.3. State Machine Engine
Razvoj Python klase koja učitava model i čuva trenutno stanje (inventory, varijable, trenutna soba).
### 5.4. Kreiranje CLI petlje koja:
Čisti ekran i ispisuje header/body.
Filtrira opcije (prikazuje samo one čiji je Condition ispunjen).
Obrađuje unos i ažurira varijable sistema.


