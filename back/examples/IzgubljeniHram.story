adventure IzgubljeniHram

// settings
define player_hit_range = [1, 10]
define boss_hit_range = [1, 6]

// resources
strength snaga = 45
gold zlato = 40
luck sreca = 4

// stats
boss_strength boss_hp = 60

// weapons
weapon Mac value 15 hit_points 5
weapon Stit value 10 hit_points 3
weapon SvetiGral value 30 hit_points 10

// treasures
treasure Dijamant weight 5
treasure MisteriozniPoklon weight 3
treasure ZlatnaMaske weight 7
treasure SvetiRunes weight 4

// rooms
room Ulaz {
    imagePath "ulaz.jpg"
    header "Ulaz u riznicu"
    body "Na ulazu stoji misteriozni čuvar. Prvi izbor može ti obezbediti blago ili opasnost."

    option "Kupi Mač (-15 zlata)"
        [zlato >= 15]
        buy Mac
        goto HodnikIskusenja;

    option "Uzmi Dijamant (+200 zlata, -5 snage)"
        take Dijamant
            set zlato = zlato + 200
        goto HodnikIskusenja;

    option "Pretraži tamni ugao"
        take MisteriozniPoklon
            set zlato = zlato + random(5, 15)
            set snaga = snaga - 2
        goto HodnikIskusenja;

    option "Kreni dalje bez rizika"
        goto HodnikIskusenja;
}

room HodnikIskusenja {
    imagePath "hodnik.png"
    header "Hodnik Iskušenja"
    body "Stepenište je prekriveno zlatom i magijom. Svaki izbor menja sudbinu igre."

    option "Pokupi Zlatnu Masku (+150 zlata, -7 snage)"
        take ZlatnaMaske
            set zlato = zlato + 150
        goto OltarSudbine;

    option "Uzmi Misteriozni Poklon (+rendom zlata, -3 snage)"
        take MisteriozniPoklon
            set zlato = zlato + (zlato / 10 + (random(1, 5) * 3))
        goto OltarSudbine;

    option "Pokušaj da preskočiš zakrivljeni prolaz"
        [snaga > 10]
        take MisteriozniPoklon
            set snaga = snaga - 5
        goto OltarSudbine;

    option "Ignoriši blago i štedi snagu"
        goto OltarSudbine;
}

room OltarSudbine {
    imagePath "oltar.png"
    header "Oltar Sudbine"
    body "Oltar traži veru, ali istovremeno nudi magični izazov."

    option "Moli se za sreću"
        take MisteriozniPoklon
            set sreca = random(1, 2)
        goto IshodMolitve;

    option "Zaželi snagu pred čuvarem"
        take SvetiRunes
            set snaga = snaga + 4
        goto Predvorje;

    option "Samo prođi ka čuvaru"
        goto Predvorje;
}

room IshodMolitve {
    imagePath "glas.png"
    header "Glas Bogova"
    body "Sudbina nije jasna. Tvoja sreća će razjasniti put."

    option "Blagoslovljen si! (+15 sreće)"
        [sreca == 1]
        take Dijamant
            set sreca = sreca + 15
        goto Predvorje;

    option "Proklet si! (sreća == 2)"
        [sreca == 2]
        take Dijamant
            set sreca = 1
        goto Predvorje;
}

room Predvorje {
    imagePath "trgovac.png"
    header "Dvorana Trgovca"
    body "Pred tobom je poslednja prilika da ojačaš opremu pre arene."

    option "Kupi Štit (-10 zlata)"
        [zlato >= 10]
        buy Stit
        goto BossArena;

    option "Kupi Sveti Gral (-30 zlata)"
        [zlato >= 30]
        buy SvetiGral
        goto BossArena;

    option "Zadrži zlato i spremi se na borbu"
        goto BossArena;
}

room BossArena {
    imagePath "arena.png"
    header "Finalni Obračun"
    body "Džinovski kameni čuvar se budi! Sada će se sve tvoje odluke isplatiti ili obiti o glavu."

    fight "UDARI BOSS-A"
        player_hit_range
        [snaga > 0]
        win Pobeda
        lose Poraz
}

room Pobeda {
    imagePath "pobeda.png"
    header "Pobeda!"
    body "Čuvar se srušio! Izlaziš iz hrama sa slavom i plijenom."

    option "Uzmi Blago"
        take SvetiRunes
            set zlato = zlato + 50
        goto Ulaz;

    option "Završi avanturu"
        goto Ulaz;
}

room Poraz {
    imagePath "poraz.png"
    header "Poraz"
    body "Čuvar te je savladao. Tvoje telo postaje deo hrama."

    option "Vaskrsni na ulazu"
        restart
        goto Ulaz;
}
