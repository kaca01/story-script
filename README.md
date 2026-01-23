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

var snaga = 10  // resurs - ogranicava sta igrac moze da uradi
var zlato = 0   // score

item Mac weight 15
item MaliKljuc weight 1

room Ulaz {
    imagePath "C://Users/user/primjer/putanje/do/pozadine/sobe.png"
    header "Ulaz u hram"
    body "Ispred vas je mračan tunel i postolje sa idolom."
    
    option "Uzmi zlatni idol" goto Hodnik take Mac set zlato = 100
    option "Samo prođi pored" goto Hodnik
}

room Hodnik {
    imagePath "C://Users/user/primjer/putanje/do/pozadine/sobe2.png"
    header "Uski prolaz"
    body "Tlo se trese. Morate biti brzi."
    
    // Igrač može proći samo ako mu je snaga veća od 5 (npr. ako nije preopterećen)
    option "Potrči ka izlazu" [snaga > 5] goto Povrsina
    option "Puzi polako" goto Povrsina set snaga = 2
}

room Povrsina {
    imagePath "C://Users/user/primjer/putanje/do/pozadine/sobe3.png"
    header "Sloboda"
    body "Izašli ste iz hrama. Čestitamo!"
    option "Kraj" goto Povrsina
}
```

## 4. Opis primjera
### 4. 1. Varijable kao "Stanje svijeta"
U linijama _var snaga = 10_ i _var zlato = 0_, definišemo globalne registre.
Zlato služi kao skor (score). To je varijabla koju igrač želi da poveća.
Snaga služi kao resurs. To je varijabla koja ograničava šta igrač može da uradi.
### 4.2. "Mač" i mehanika težine
U gramatici smo definisali: _item Mac weight 15_. Kada igrač izabere opciju: _option "Uzmi mac" goto Hodnik take Mac set zlato = 100_
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


