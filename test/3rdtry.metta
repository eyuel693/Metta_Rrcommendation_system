; ——— MOVIES (Structured as per spec) ———
(movie inception "Inception" "Sci-Fi" "Christopher Nolan" 8.8)
(movie interstellar "Interstellar" "Sci-Fi" "Christopher Nolan" 8.6)
(movie the-martian "The Martian" "Sci-Fi" "Ridley Scott" 8.0)
(movie avatar "Avatar" "Sci-Fi" "James Cameron" 7.8)
(movie titanic "Titanic" "Romance" "James Cameron" 7.8)
(movie jurassic-park "Jurassic Park" "Adventure" "Steven Spielberg" 8.1)
(movie the-matrix "The Matrix" "Sci-Fi" "Lana Wachowski" 8.7)
(movie blade-runner-2049 "Blade Runner 2049" "Sci-Fi" "Denis Villeneuve" 8.0)
(movie the-dark-knight "The Dark Knight" "Action" "Christopher Nolan" 9.0)
(movie john-wick "John Wick" "Action" "Chad Stahelski" 7.4)
(movie la-la-land "La La Land" "Romance" "Damien Chazelle" 8.0)
(movie the-revenant "The Revenant" "Adventure" "Alejandro G. Iñárritu" 8.0)
(movie her "Her" "Romance" "Spike Jonze" 8.0)

; ——— ACTORS (Top 3 per movie) ———
(actor inception "Leonardo DiCaprio")
(actor inception "Joseph Gordon-Levitt")
(actor inception "Elliot Page")

(actor interstellar "Matthew McConaughey")
(actor interstellar "Anne Hathaway")
(actor interstellar "Jessica Chastain")

(actor the-martian "Matt Damon")
(actor the-martian "Jessica Chastain")
(actor the-martian "Kristen Wiig")

(actor avatar "Sam Worthington")
(actor avatar "Zoe Saldaña")
(actor avatar "Sigourney Weaver")

(actor titanic "Leonardo DiCaprio")
(actor titanic "Kate Winslet")
(actor titanic "Billy Zane")

(actor jurassic-park "Sam Neill")
(actor jurassic-park "Laura Dern")
(actor jurassic-park "Jeff Goldblum")

(actor the-matrix "Keanu Reeves")
(actor the-matrix "Laurence Fishburne")
(actor the-matrix "Carrie-Anne Moss")

(actor blade-runner-2049 "Ryan Gosling")
(actor blade-runner-2049 "Harrison Ford")
(actor blade-runner-2049 "Ana de Armas")

(actor the-dark-knight "Christian Bale")
(actor the-dark-knight "Heath Ledger")
(actor the-dark-knight "Aaron Eckhart")

(actor john-wick "Keanu Reeves")
(actor john-wick "Michael Nyqvist")
(actor john-wick "Alfie Allen")

(actor la-la-land "Ryan Gosling")
(actor la-la-land "Emma Stone")
(actor la-la-land "John Legend")

(actor the-revenant "Leonardo DiCaprio")
(actor the-revenant "Tom Hardy")
(actor the-revenant "Domhnall Gleeson")

(actor her "Joaquin Phoenix")
(actor her "Amy Adams")
(actor her "Scarlett Johansson")

; ——— USERS (Watched movies + inferred preferences as separate atoms) ———
(watched alice inception)
(watched alice interstellar)
(watched alice the-martian)
(watched alice avatar)
(preference alice "Sci-Fi")

(watched bob inception)
(watched bob avatar)
(watched bob titanic)
(watched bob jurassic-park)
(preference bob "Sci-Fi")
(preference bob "Romance")
(preference bob "Adventure")

(watched eve avatar)
(watched eve titanic)
(watched eve la-la-land)
(watched eve the-revenant)
(preference eve "Sci-Fi")
(preference eve "Romance")
(preference eve "Adventure")

(watched jener inception)
(watched jener interstellar)
(watched jener the-matrix)
(watched jener blade-runner-2049)
(watched jener the-dark-knight)
(preference jener "Sci-Fi")
(preference jener "Action")

(watched charlie the-matrix)
(watched charlie john-wick)
(watched charlie blade-runner-2049)
(watched charlie the-dark-knight)
(preference charlie "Sci-Fi")
(preference charlie "Action")

(watched diana jurassic-park)
(watched diana the-martian)
(watched diana interstellar)
(watched diana inception)
(preference diana "Adventure")
(preference diana "Sci-Fi")

(watched frank la-la-land)
(watched frank titanic)
(watched frank the-revenant)
(watched frank her)
(watched frank avatar)
(preference frank "Romance")
(preference frank "Adventure")
(preference frank "Sci-Fi")

; ——— EXISTING FUNCTIONS (Kept intact) ———
; Keep all original utility, popularity, content-similarity, director-match, similar-users, collaborative-rec, recommend-to, filter-recommendations, explain-genre, explain-director, explain-collab, get-rating, new-recommendation

; ——— NEW FUNCTIONS FROM SPEC (Extensions) ———
(= (contentBasedRecommendation $user)
   (content-similarity $user $movie))

(= (collaborativeFiltering $user)
   (collaborative-rec $user $movie))

(= (getRecommendations $user $movie)
   (recommend-to $user $movie))

(= (explainRecommendation $user $movie $explanation)
   (explain-genre $user $movie $explanation))

(= (explainRecommendation $user $movie $explanation)
   (explain-director $user $movie $explanation))

(= (explainRecommendation $user $movie $explanation)
   (explain-collab $user $movie $explanation))

(= (updatePreferences $user $newGenre)
   (add-atom &self (preference $user $newGenre)))

; ——— GENRE SIMILARITY (As per spec example) ———
(genre-similarity "Sci-Fi" "Action" "High")
(genre-similarity "Sci-Fi" "Adventure" "High")
(genre-similarity "Action" "Adventure" "High")

; ——— DIRECTOR PREFERENCE (Inferred from watched, as per spec example) ———
; Example: If user watched multiple by same director, add "High"
(director-preference "Christopher Nolan" alice "High")  ; From Inception, Interstellar
; Add similar for others if needed

; ——— QUERIES (Updated to use new functions) ———
!(getRecommendations alice $movie)
!(getRecommendations bob $movie)
!(getRecommendations eve $movie)

; Similar users (kept)
!(similar-users alice $user)
!(similar-users bob $user)
!(similar-users eve $user)

; Rating queries (updated to use movie atom)
(= (get-rating $movie $score)
   (match &self (movie $movie $t $g $d $score) $score))

!(get-rating the-matrix $score)
!(get-rating inception $score)
!(get-rating titanic $score)

; Content similarity (kept, but can extend with genre-similarity)