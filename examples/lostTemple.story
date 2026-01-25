adventure LostTemple

var strength = 10 
var gold = 0

item Sword weight 15
item SmallKey weight 1

room Entrance {
    imagePath "C://Users/user/example/path/to/background/room1.png"
    header "Temple Entrance"
    body "In front of you is a dark tunnel and a pedestal with an idol."
    
    option "Take the golden idol" goto Corridor take Sword set gold = gold + 100 set strength = strength - 5;
    option "Just walk past" goto Corridor;
}

room Corridor {
    imagePath "C://Users/user/example/path/to/background/room2.png"
    header "Narrow Passage"
    body "The ground is shaking. You must be fast."
    
    option "Run to the exit" [strength > 5] goto Surface;
    option "Crawl slowly" goto LostGame;
}

room Surface {
    imagePath "C://Users/user/example/path/to/background/room3.png"
    header "Freedom"
    body "You have exited the temple. Congratulations!"
    option "End" goto Surface;
}

room LostGame {
    imagePath ""
    header "Game end"
    body "You have lost the game. Better luck next time"
    option "end" goto LostGame;
}