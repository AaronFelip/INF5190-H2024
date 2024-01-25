function trierParNom() {

    var tableau = document.getElementById('table');
    var lignes = tableau.rows;
    var permutation, index;

    do {

        permutation = false

        for( index=1; index < lignes.length - 1; index++ ){
             var celluleActuelle = lignes[ index ].getElementsByTagName( "td" )[ 0 ];
             var celluleSuivante = lignes[ index + 1 ].getElementsByTagName( "td" )[ 0 ];

             if( celluleActuelle.innerHTML.toLowerCase() >
                        celluleSuivante.innerHTML.toLowerCase() ) {
                 lignes[ index ].parentNode.insertBefore( lignes[ index + 1 ], lignes[ index ]);

                 permutation = true;

             }

        }

    } while( permutation )
}