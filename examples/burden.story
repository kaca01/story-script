adventure HeavyBurden

var strength = 2
var gold = 100

item HugeBoulder weight 500

room Dungeon {
    imagePath "assets/dungeon.png"
    header "Deep Dungeon"
    body "You are holding a boulder. You feel very weak."
    option "Climb the rope" [strength > 5] goto Surface
    option "Drop everything" goto Dungeon set strength = 10
}

room Surface {
    imagePath "assets/sun.png"
    header "Safe at last"
    body "You made it out!"
    option "End" goto Surface
}