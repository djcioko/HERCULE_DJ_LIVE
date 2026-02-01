# ===================== MUSIC DB =====================
# Lista ta completă cu toate piesele, eliminând duplicatele
MUSIC_DB = list(set([
    "Bruno Mars  - Marry You",
    "Hermes House Band & DJ Otzi - Live Is Life",
    "Pharrell Williams -  Happy",
    "Daft Punk - Get Lucky",
    "Chubby Checker  - The Twist",
    "TNN - La Cucamarcha",
    "Whitney Houston - I  Wanna Dance With Somebody",
    "Robin Thick featuring Pharrell & T.I.-  Blurred Lines",
    "Kaoma - Banto",
    "Village People  - Y.M.C.A.",
    "T-Rio - (Choopeta) Mamae Eu Quero",
    "Taylor Swift - Shake It Off",
    "Dos Amigos - Mambo",
    "Michel Telo - A si tu pego",
    "House Of Pain - Jump Around",
    "Queen – We are the champions",
    "Leonard Cohen - Dance Me To The End Of Love",
    "Black Eyed Peas  - I Gotta Feeling",
    "Michel Telo - Bara bere",
    "Louis Prima - Jungle Book",
    "Cupid  - Cupid Shuffle",
    "Bon Jovi Livin' On A Prayer",
    "Marcela Morelo - Corazon Salvaje",
    "Monkey Circus - El Ritmo Hafanana",
    "Van Morrison Brown Eyed Girl",
    "Enrique Iglesias  - Bailando",
    # ... pune toate celelalte melodii aici, în aceeași manieră
]))

# ===================== SONG PICKER =====================
# La fiecare scanare, extrage random o piesă și o elimină din listă
def pick_song(img: Image.Image):
    """Alege piesa pe baza de culoare + 20% fata, fără duplicate"""
    color = dominant_color(img)
    face = face_emotion(img)

    # Opțional: poți filtra pe baza emoției
    pool = MUSIC_DB.copy()  # folosim toate piesele
    if face in ["happy","neutral"]:
        pass  # putem adăuga logica de filtrare, dacă vrei
    elif face in ["sad","angry"]:
        pass  # idem

    if pool:
        song = random.choice(pool)
        MUSIC_DB.remove(song)  # eliminăm ca să nu se mai repete
        return song
    else:
        return "No more songs available"
