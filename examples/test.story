adventure TestZaborava

room Start {
    imagePath "start.png"
    header "Prazna soba"
    body "Ovde nema osnovnih statsa."
    option "Idi dalje" goto Kraj;
}

room Kraj {
    imagePath "kraj.png"
    header "Kraj"
    body "Stigao si."
    option "Kraj" goto Start;
}