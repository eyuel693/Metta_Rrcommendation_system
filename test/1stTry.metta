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
(director the-martian ryan-gosling)  ; Wait — actually directed by Ridley Scott! Fixed below
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

; ——— CORRECTED: the-martian director ———
(director the-martian ridley-scott)

; ——— ACTORS (optional, for future expansion) ———
(stars inception leonardo-di-caprio)
(stars interstellar matthew-mcconaughey)
(stars the-dark-knight christian-bale)
(stars the-matrix keanu-reeves)
(stars avatar sam-worthington)
(stars titanic leonardo-di-caprio)
(stars la-la-land emma-stone)
(stars john-wick keanu-reeves)

; ——— THEMES / TAGS (for content expansion) ———
(tag inception mind-bending)
(tag inception time)
(tag interstellar space)
(tag interstellar survival)
(tag the-martian survival)
(tag the-martian science)
(tag the-dark-knight heroism)
(tag the-dark-knight chaos)
(tag avatar alien-world)
(tag titanic love)
(tag titanic tragedy)
(tag her romance)
(tag her ai)

(= (length $list)
   (if (== $list ())
       0
       (let* ((($h $t) (decons-atom $list)))
           (+ 1 (length $t))
       )
   )
)

(= (popularity $movie $count)
   (length (collect &self (likes $user $movie)))
)





; ——— CONTENT-BASED: BY GENRE ———
(= (content-similarity $user $movie)
   (match &self (likes $user $liked)
      (match &self (genre $liked $g)
         (match &self (genre $movie $g)
            $movie
         )
      )
   )
)

; ——— CONTENT-BASED: BY DIRECTOR ———
(= (director-match $user $movie)
   (match &self (likes $user $liked)
      (match &self (director $liked $d)
         (match &self (director $movie $d)
            $movie
         )
      )
   )
)

; ——— COLLABORATIVE: SIMILAR USER ———
(= (similar-user $user1 $user2)
   (if (== $user1 $user2)
       ()
       (match &self (likes $user1 $movie)
          (match &self (likes $user2 $movie)
             $user2
          )
       )
   )
)

; ——— COLLABORATIVE RECOMMENDATION ———
(= (collaborative-rec $user $movie)
   (match &self (similar-user $user $other)
      (match &self (likes $other $movie)
         $movie
      )
   )
)

; ——— HYBRID RECOMMENDATION ———
(= (recommend-to $user $movie)
   (content-similarity $user $movie))

(= (recommend-to $user $movie)
   (director-match $user $movie))

(= (recommend-to $user $movie)
   (collaborative-rec $user $movie))

; ——— QUERIES ———
!(recommend-to alice $movie)
!(recommend-to bob $movie)
!(recommend-to eve $movie)
!(popularity the-matrix $count)



