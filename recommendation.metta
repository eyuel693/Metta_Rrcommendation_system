; ——— MOVIE GENRES ———
(genre inception sci-fi)
(genre interstellar sci-fi)
(genre the-martian sci-fi)
(genre avatar sci-fi)
(genre the-matrix sci-fi)
(genre blade-runner-2049 sci-fi)
(genre the-dark-knight action)
(genre john-wick action)
(genre jurassic-park adventure)
(genre titanic romance)
(genre la-la-land romance)
(genre the-revenant adventure)
(genre her romance)
(watched alice inception)
(watched alice interstellar)
(watched alice the-martian)
(watched alice avatar)
(preference alice "Sci-Fi")

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

; ——— USERS & THEIR LIKES ———
(likes alice inception)
(likes alice interstellar)
(likes alice the-martian)
(likes alice avatar)

(likes bob inception)
(likes bob avatar)
(likes bob titanic)
(likes bob jurassic-park)

(likes eve avatar)
(likes eve titanic)
(likes eve la-la-land)
(likes eve the-revenant)

(likes jener inception)
(likes jener interstellar)
(likes jener the-matrix)
(likes jener blade-runner-2049)
(likes jener the-dark-knight)

(likes charlie the-matrix)
(likes charlie john-wick)
(likes charlie blade-runner-2049)
(likes charlie the-dark-knight)

(likes diana jurassic-park)
(likes diana the-martian)
(likes diana interstellar)
(likes diana inception)

(likes frank la-la-land)
(likes frank titanic)
(likes frank the-revenant)
(likes frank her)
(likes frank avatar)

; ——— MOVIE GENRES ———
(genre inception sci-fi)
(genre interstellar sci-fi)
(genre the-martian sci-fi)
(genre avatar sci-fi)
(genre the-matrix sci-fi)
(genre blade-runner-2049 sci-fi)
(genre the-dark-knight action)
(genre john-wick action)
(genre jurassic-park adventure)
(genre titanic romance)
(genre la-la-land romance)
(genre the-revenant adventure)
(genre her romance)

; ——— DIRECTORS ———
(director inception christopher-nolan)
(director interstellar christopher-nolan)
(director the-martian ridley-scott)
(director avatar james-cameron)
(director the-matrix lana-wachowski)
(director the-dark-knight christopher-nolan)
(director blade-runner-2049 denis-villeneuve)
(director john-wick david-leitch)
(director jurassic-park steven-spielberg)
(director titanic james-cameron)
(director la-la-land damien-chazelle)
(director the-revenant alejandro-gonzalez-inarritu)
(director her spike-jones)

; ——— RATINGS (1-10 scale) ———
(rating inception 8.8)
(rating interstellar 8.6)
(rating the-martian 8.0)
(rating avatar 7.8)
(rating the-matrix 8.7)
(rating blade-runner-2049 8.0)
(rating the-dark-knight 9.0)
(rating john-wick 7.4)
(rating jurassic-park 8.1)
(rating titanic 7.8)
(rating la-la-land 8.0)
(rating the-revenant 8.0)
(rating her 8.0)

; ——— UTILITY FUNCTIONS ———
(= (length $list)
   (if (== $list ())
       0
       (let* ((($h $t) (decons-atom $list)))
           (+ 1 (length $t))
       )
   )
)

; ——— POPULARITY FUNCTIONS ———
(= (popularity $movie $count)
   (length (collect &self (likes $user $movie)))
)

; ——— CONTENT-BASED RECOMMENDATION ———
(= (content-similarity $user $movie)
   (match &self (likes $user $liked)
      (match &self (genre $liked $g)
         (match &self (genre $movie $g)
            $movie
         )
      )
   )
)

(= (director-match $user $movie)
   (match &self (likes $user $liked)
      (match &self (director $liked $d)
         (match &self (director $movie $d)
            $movie
         )
      )
   )
)

; ——— COLLABORATIVE FILTERING ———
(= (similar-users $user1 $user2)
   (if (== $user1 $user2)
       false
       (match &self (likes $user1 $movie)
          (match &self (likes $user2 $movie)
             $user2
          )
       )
   )
)

(= (collaborative-rec $user $movie)
   (match &self (similar-users $user $other)
      (match &self (likes $other $movie)
         $movie
      )
   )
)

; ——— HYBRID RECOMMENDATION SYSTEM ———
(= (recommend-to $user $movie)
   (content-similarity $user $movie))

(= (recommend-to $user $movie)
   (director-match $user $movie))

(= (recommend-to $user $movie)
   (collaborative-rec $user $movie))

; ——— FILTER OUT ALREADY LIKED MOVIES ———
(= (filter-recommendations $user $movie)
   (match &self (recommend-to $user $movie)
      (if (== (collect &self (likes $user $movie)) ())
          $movie
      )
   )
)

; ——— SIMPLE EXPLANATION FUNCTIONS ———
(= (explain-genre $user $movie $explanation)
   (match &self (likes $user $liked)
      (match &self (genre $liked $g)
         (match &self (genre $movie $g)
            (= $explanation (str "Similar genre to " $liked))
         )
      )
   )
)

(= (explain-director $user $movie $explanation)
   (match &self (likes $user $liked)
      (match &self (director $liked $d)
         (match &self (director $movie $d)
            (= $explanation (str "Same director as " $liked))
         )
      )
   )
)

(= (explain-collab $user $movie $explanation)
   (match &self (similar-users $user $other)
      (match &self (likes $other $movie)
         (= $explanation (str "Similar user " $other " likes this"))
      )
   )
)

(= (get-rating $movie $score)
   (match &self (rating $movie $score)
      $score
   )
)

; ——— WORKING RECOMMENDATION FUNCTION ———
(= (new-recommendation $user $movie)
   (match &self (similar-users $user $other)
      (match &self (likes $other $movie)
         (if (== (collect &self (likes $user $movie)) ())
             $movie
         )
      )
   )
)

; ——— QUERIES ———
; Basic recommendations
;!(recommend-to alice $movie)
;!(recommend-to bob $movie)
;!(recommend-to eve $movie)



; Similar users
;!(similar-users alice $user)
;!(similar-users bob $user)
;!(similar-users eve $user)


; Rating queries
;!(get-rating the-matrix $score)
;!(get-rating inception $score)
;!(get-rating titanic $score)
!(content-similarity alice $movie)


;!(match &self (watched $user $movie) $user)

;!(explain-collab eve $movie $explanation)