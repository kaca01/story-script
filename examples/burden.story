adventure HeavyBurden

// 1. Testing Variables (name, ID, INT)
var health = 100
var energy = 50
var has_sword = 0
var gold = 10

// 2. Testing Items (name, ID, weight)
item Sword weight 15
item Potion weight 2
item Coin weight 1

// 3. Testing GlobalRules (name, assignments)
rule Fatigue {
    energy = energy - 5
    health = health - (2 + 1)
}

rule Healing {
    health = 100
}

// 4. Testing Rooms and its elements
room StartingRoom {
    imagePath "assets/start.png"
    header "Adventure Start"
    body "You are in a test room. Here we are checking all options."

    // Option without condition, with 'take' and 'set' Assignment
    option "Take the sword" goto StartingRoom take Sword set has_sword = 1;

    // Option with Condition and using a GlobalRule
    option "Go to the hallway" [energy >= 10] goto Hallway set Fatigue;
}

room Hallway {
    imagePath "assets/hallway.png"
    header "Dark Passage"
    body "We are testing complex arithmetic and multiple actions."

    // Testing Expression: operator priorities, parentheses, variables, INT
    option "Practice with sword" [has_sword == 1] goto Hallway 
        set energy = (energy * 2) / (5 + 5) 
        set gold = gold + 10 * 2;

    // Testing multiple 'set' actions: Assignment and GlobalRule together
    option "Rest" goto StartingRoom 
        set Healing
        set energy = 100;
}

/* 5. Testing Comment (Block comment)
   The LSP should recognize and skip this.
*/

// Single line comment at the end of the file