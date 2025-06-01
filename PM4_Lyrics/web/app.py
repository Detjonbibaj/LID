from flask import Flask, render_template , request, jsonify
from pymongo import MongoClient
from flask_caching import Cache
from collections import Counter
from itertools import chain
from bson.son import SON

app = Flask(__name__)

# Flask-Caching konfigurieren
app.config['CACHE_TYPE'] = 'simple'  # Einfache Cache-Option für Entwicklungszwecke
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  # Cache für 1 Stunde speichern
cache = Cache(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["data"]
songs_collection = db["genius"]

ARTISTS_BY_GENRE_AND_LANGUAGE = {
    "rb": {
        "de": [
        "Niqo Nuevo", "Ramsi Aliani", "Joy Denalane", "SKA 510", "Seeed",
        "Mashanda", "Search Yiu", "Elisa Loah", "Nico Gomez", "BILLA JOE"
        ],
        "en": [
        "The Weeknd", "Drake", "Chris Brown", "Summer Walker",
        "Miguel", "Jhen Aiko", "Omarion", "Rihanna", "Stevie Wonder"
        ],
        "es": [
        "Jesse Baez", "Paulo Londra", "Andresito Otro Corte & Pablo Chill-E",
        "Kali Uchis", "Lyanno", "ELYSANIJ", "Yung Beef",
        "Rich Vagos, Samantha Barrn & Jayrick", "Motherflowers", "Abhir Hathi & Mayo"
        ],
        "fr": [
        "Tayc", "Dadju", "Noah Lunsi", "La Synesia", "Marwa Loud",
        "KeBlack", "Franglish", "DJ FASH-ONE", "Kayna Samet", "Driks"
        ],
        "it": [
        "Gemitaiz", "Madame", "Funk Shui Project & Davide Shorty", "Martina May",
        "Joan Thiele", "Neri Per Caso", "Keyna", "Frah Quintale", "ISIDE", "Guido Cagiva"
        ]
  },
  "country": {
        "de": [
        "Hank Hberle Jr.", "Franzi25", "Larry Schuba und Western Union"
        ],
        "en": [
        "Brad Paisley", "Taylor Swift", "Cody Jinks", "Shania Twain",
        "Florida Georgia Line", "Morgan Wallen", "Hank Williams",
        "Steve Earle", "Brooks & Dunn", "John Prine"
        ],
        "es": [
        "Natanael Cano", "C. Tangana, Carin Leon & Adriel Favela", "Eslabon Armado",
        "Jos Alfredo Jimnez", "Chalino Snchez", "WOW (Fictional)",
        "Alejandro Fernndez", "Natanael Cano & La Nueva Era", "T3R Elemento", "Velvetine"
        ],
        "fr": [
        "Baptiste W. Hamon", "Avec pas d'casque", "Jewel Usain", "Baaziz", "Canailles",
        "N i g g o", "Le Donjon de Naheulbeuk", "Mawndo Celestin", "P'tit Belliveau", "Tire le coyote"
        ],
        "it": [
        "William Onyeabor", "Alfredo Catalani"
        ]
  },
  "pop": {
    "de": [
      "Wir sind Helden", "Modo", "Falco", "Ramon Roselly", "Xavier Naidoo",
      "Hannes Wader", "Stereoact", "Shirin David", "Helene Fischer", "LEA"
    ],
    "en": [
      "Lorde", "Joji", "Ed Sheeran", "Lana Del Rey", "Taylor Swift",
      "Harry Styles", "Miley Cyrus", "Lady Gaga", "Billie Eilish", "Ariana Grande"
    ],
    "es": [
      "Wolfine", "Matias Ft. Trapzongo", "Gael Garca Bernal", "Anuel AA",
      "Arcngel & Bad Bunny", "CNCO", "Aventura"
    ],
    "fr": [
      "PNL", "Gims", "Angle", "Jacques Brel", "Franoise Hardy",
      "Stromae", "Charles Aznavour", "Frro Delavega", "Julien Dor", "Souf"
    ],
    "it": [
      "Motta", "Gazzelle", "Coez", "Rosa Chemical", "PSICOLOGI",
      "Pinguini Tattici Nucleari", "Calcutta", "Il Pagante", "Elisa & Carl Brave", "COLAPESCEDIMARTINO"
    ]
  },
  "rap": {
    "de": [
      "Kollegah", "Samra", "Bushido", "Genetikk", "Marteria",
      "Luciano", "SpongeBOZZ", "Sa4", "RAF Camora", "Bonez MC"
    ],
    "en": [
      "Drake", "Kanye West", "J. Cole", "Kendrick Lamar", "Rae Sremmurd",
      "Eminem", "iLOVEFRiDAY", "JAY-Z", "Chance the Rapper", "Lil Wayne"
    ],
    "es": [
      "Jon Z", "Cartel de Santa", "Calle 13", "Residente", "Coscu",
      "Almighty", "Yung Beef", "Darell & Anuel AA", "Natos y Waor", "Lenny Tavrez"
    ],
    "fr": [
      "JuL", "Nekfeu", "Booba", "PNL", "13 Organis",
      "Gims", "Vald", "Lacrim", "Ninho", "Rohff"
    ],
    "it": [
      "MadMan", "Dark Polo Gang", "IZI", "Gemitaiz", "Nitro",
      "Gu", "Gemitaiz & MadMan", "Marracash", "Sfera Ebbasta", "Noyz Narcos"
    ]
  },
  "rock": {
    "de": [
      "Rammstein", "Die rzte", "AnnenMayKantereit", "Bhse Onkelz", "Revolverheld",
      "Glasperlenspiel", "Frei.Wild", "Jennifer Rostock", "Adel Tawil", "Die Toten Hosen"
    ],
    "en": [
      "The Killers", "Arctic Monkeys", "Smash Mouth", "The Cranberries", "Billy Joel",
      "Rage Against the Machine", "Jason Mraz", "Bruce Springsteen", "5 Seconds of Summer", "Fall Out Boy"
    ],
    "es": [
      "Perras on the Beach", "El Mat a un Polica Motorizado", "Buena Vista Social Club",
      "Los Planetas", "Shakira", "Jesse & Joy", "Ricky Martin", "Ska-P", "Carolina Durante", "Nicols y Los Fumadores"
    ],
    "fr": [
      "FAUVE", "Noir Dsir", "Daniel Balavoine", "Ultra Vomit", "Renaud",
      "Shaka Ponk", "Twin Twin", "Fishbach", "Saez", "Georges Brassens"
    ],
    "it": [
      "Pinguini Tattici Nucleari", "Katya Zamolodchikova", "Loredana Bert", "Elio e le Storie Tese",
      "Fast Animals and Slow Kids", "Ministri", "GOMMA", "La Quiete", "Ultima Frontiera", "Fine Before You Came"
    ]
  },
  "misc": {
    "de": [
      "Julia Engelmann", "matza", "Georg Bchner", "Faber",
      "Joseph von Eichendorff", "Carsten Erobique Meyer",
      "Der Sprechgesangskurier", "Sorgenschall"
    ],
    "en": [
      "William Golding", "F. Scott Fitzgerald", "Childish Gambino",
      "Harper Lee", "Martin Luther King Jr.", "Wilfred Owen", "Carol Ann Duffy"
    ],
    "es": [
      "Federico Garca Lorca", "Julio Cortzar", "Mime871", "Gerardo Ortiz", "Jos Mart",
      "Jorge Manrique", "Arcngel", "Banda MS de Sergio Lizrraga", "Robert Laboy Jr", "Rubn Daro"
    ],
    "fr": [
      "Jacques Prvert", "Franck Ribry", "Michel Hazanavicius", "Jean de La Fontaine", "Joachim du Bellay",
      "JuL", "Robert Desnos", "Erving Goffman", "Sidiki Diabat", "Prince Kader"
    ],
    "it": [
      "AURORA (IT)", "Enzo Dong", "Salmo", "IOSONOUNCANE", "Ermal Meta",
      "XVI Religion", "Giacomo Leopardi", "L'officina della camomilla", "Storm{O}"
    ]
  }
}



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@cache.cached(timeout=3600)
@app.route('/api/genres')
def get_genres():
    genres = db["top_words_by_artist_real"].distinct("tag")
    return jsonify(sorted(genres))

@cache.cached(timeout=3600)
@app.route('/api/artists/<genre>/<language>')
def get_artists_by_genre_and_language(genre, language):
    # Falls es keine Künstler für das Genre und die Sprache gibt, Standardwert zurückgeben
    artists = ARTISTS_BY_GENRE_AND_LANGUAGE.get(genre, {}).get(language, [])
    return jsonify(sorted(artists))

@cache.cached(timeout=3600)
@app.route('/api/top_words/<genre>/<artist>/<language>')
def get_top_words(genre, artist, language):
    # Bei der Anfrage für Top-Wörter auch die Sprache berücksichtigen
    doc = db["top_words_by_artist_real"].find_one({"tag": genre, "artist": artist})
    if not doc:
        return jsonify([])
    # Beispiel: Sprache wird hier ignoriert, aber du kannst sie bei Bedarf für zusätzliche Logik verwenden
    return jsonify(doc.get("top_words", []))

@cache.cached(timeout=3600)
@app.route('/api/top_words_by_genre/<genre>')
def get_top_words_by_genre(genre):
    docs = db["top_words_by_artist_real"].find({"tag": genre})
    word_counter = Counter()

    for doc in docs:
        word_list = doc.get("top_words", [])
        for word, count in word_list:
            word_counter[word] += count

    top_10 = word_counter.most_common(10)
    return jsonify(top_10)


@app.route('/api/sentiment_by_year/<lang>/<genre>')
def sentiment_by_year_dynamic(lang, genre):
    collection_map = {
        "de": "song_sentiment_analysis_de",
        "en": "song_sentiment_analysis_en",
        "es": "song_sentiment_analysis_es",
        "it": "song_sentiment_analysis_it"
    }
    
    collection_name = collection_map.get(lang)
    if not collection_name:
        return jsonify({"error": "Ungültige Sprache"}), 400

    match_stage = {}
    if genre != "all":
        match_stage["tag"] = genre
    else:
        match_stage["year"] = {"$gte": 1950}

    pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": "$year",
            "average_sentiment": {"$avg": "$sentiment_score"}
        }},
        {"$sort": SON([("_id", 1)])}
    ]
    result = list(db[collection_name].aggregate(pipeline))
    return jsonify(result)


@app.route('/api/complexity_vs_popularity/<language>/<genre>')
def complexity_vs_popularity(language, genre):
    # Erlaube nur bestimmte Sprachen, um Sicherheitslücken zu vermeiden
    valid_languages = ['de', 'en', 'fr', 'es', 'it']
    if language not in valid_languages:
        return jsonify({'error': 'Ungültige Sprache'}), 400

    # Dynamisch die Collection auswählen
    collection_name = f"sampled_subset_{language}"
    collection = db[collection_name]

    # Daten abrufen
    songs = collection.find({
        'language': language,
        'tag': genre,
        'views': {'$ne': None},
        'vocab_richness': {'$exists': True}
    }, {
        'title': 1,
        'artist': 1,
        'views': 1,
        'vocab_richness': 1,
        'avg_word_length': 1
    })

    # Ergebnis als JSON-Liste zurückgeben
    data = [{
        'title': s.get('title', 'Unknown'),
        'artist': s.get('artist', 'Unknown'),
        'views': s['views'],
        'vocab_richness': s['vocab_richness'],
        'avg_word_length': s.get('avg_word_length')
    } for s in songs]

    return jsonify(data)


@app.route('/api/lyrics_length_vs_views/<language>/<genre>')
def lyrics_length_vs_views(language, genre):
    collection = db[f"sampled_subset_{language}"]
    songs = collection.find({
        'tag': genre,
        'lyrics_word_count': {'$exists': True},
        'views': {'$ne': None},
        'vocab_richness': {'$exists': True}
    }, {
        'title': 1,
        'artist': 1,
        'lyrics_word_count': 1,
        'views': 1,
        'vocab_richness': 1
    })

    return jsonify([
        {
            'title': s.get('title', 'Unknown'),
            'artist': s.get('artist', 'Unknown'),
            'lyrics_word_count': s['lyrics_word_count'],
            'views': s['views'],
            'vocab_richness': s['vocab_richness']
        } for s in songs
    ])

  
if __name__ == '__main__':
    app.run(debug=True)
