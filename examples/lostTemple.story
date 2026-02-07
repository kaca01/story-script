adventure IzgubljeniHram

// settings
define player_hit_range = [1, 10]
define boss_hit_range = [1, 5]

// resources
strength snaga = 40
gold zlato = 50
luck sreca = 5

// stats
boss_strength boss_hp = 45

// weapons
weapon Mac value 15 hit_points 5
weapon Stit value 10 hit_points 3
weapon SvetiGral value 30 hit_points 10

// treasures
treasure Dijamant weight 5
treasure MisteriozniPoklon weight 3
treasure ZlatnaMaske weight 7

// rooms
room Ulaz {
    imagePath "ulaz.png"
    header "Ulaz u riznicu"
    body "U senci vrata nalaze se osnovni predmeti. Svaki izbor ima cenu u zlatu ili snazi."

    option "Kupi Mač (-15 zlata)"
        [zlato >= 15]
        buy Mac
        goto HodnikIskusenja;

    option "Uzmi Dijamant (+200 zlata, -5 snage)"
        take Dijamant
            set zlato = zlato + 200
        goto HodnikIskusenja;

    option "Kreni dalje bez ičega"
        goto HodnikIskusenja;
}

room HodnikIskusenja {
    imagePath "hodnik.png"
    header "Hodnik Iskušenja"
    body "Pod je prekriven zlatnicima, ali vazduh je težak i iscrpljuje vas."

    option "Pokupi Zlatnu Masku (+150 zlata, -7 snage)"
        take ZlatnaMaske
            set zlato = zlato + 150
        goto OltarSudbine;

    option "Uzmi Misteriozni Poklon (+rendom zlato, -3 snage)"
        take MisteriozniPoklon
            set zlato = zlato + (zlato / 10 + (random(1, 5) * 3))
        goto OltarSudbine;

    option "Ignoriši blago i štedi snagu"
        goto OltarSudbine;
}

room OltarSudbine {
    imagePath "oltar.png"
    header "Oltar Sudbine"
    body "Ovaj oltar traži veru."

    option "Moli se za sreću"
        take MisteriozniPoklon
            set sreca = random(1, 2)
        goto IshodMolitve;

    option "Samo prođi ka čuvaru"
        goto Predvorje;
}

room IshodMolitve {
    imagePath "glas.png"
    header "Glas Bogova"
    body "Osetili ste promenu u svojoj auri."

    option "Blagoslovljen si! (+15 sreće)"
        [sreca == 1]
        take Dijamant
            set sreca = sreca + 15
        goto Predvorje;

    option "Proklet si! (sreća == 1)"
        [sreca == 2]
        take Dijamant
            set sreca = 1
        goto Predvorje;
}

room Predvorje {
    imagePath "trgovac.png"
    header "Dvorana Trgovca"
    body "Poslednja stanica pre arene."

    option "Kupi Štit (-10 zlata)"
        [zlato >= 10]
        buy Stit
        goto BossArena;

    option "Kupi Sveti Gral (-30 zlata)"
        [zlato >= 30]
        buy SvetiGral
        goto BossArena;

    option "Uđi u arenu spreman"
        goto BossArena;
}

room BossArena {
    imagePath "arena.png"
    header "Finalni Obračun"
    body "Džinovski kameni čuvar se budi!"

    fight "UDARI BOSS-A"
        player_hit_range
        [snaga > 0]
        win Pobeda
        lose Poraz
}

room Pobeda {
    imagePath "pobeda.png"
    header "Pobeda!"
    body "Čuvar se srušio! Izlaziš iz hrama sa slavom."

    option "Završi avanturu"
        goto Ulaz;
}

room Poraz {
    imagePath "poraz.png"
    header "Smrt u hramu"
    body "Tvoje telo je postalo deo temelja hrama."

    option "Vaskrsni na ulazu"
        restart
        goto Ulaz;
}
