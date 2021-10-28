# Top 10 des animaux marins les plus dangereux
![Des animaux marins](assets/bandeau.jpg) <br>
> En équipe avec
>> Quentin Seurt et Pierre Le Monnier: Site Bubble, Front-end <br>
>> Dylan Bourdais, Nolann Colliou et Cindy Billerait: Interface pygame Back-end <br>
<br>

<p style="font-size:xx-large">Notre programme</p>
<p style="font-size:large">
    Nous avons décidé de créer un dictionnaire recensant le top 10 des espèces marines les plus dangereuses pour avoir accès à leurs caractéristiques et être en mesure de les reconnaître ou/et de les localiser.
    <br>
    Pour cela, nous avons commencé par rassembler les informations sur un fichier csv à partir duquel nous avons extrait les données pour en faire une base de données via SQLite.
    <br> 
    Nous avons ensuite décidé de partir sur une interface graphique en python grâce à la bibliothèque pygame.
    <br>
    Nous avons ensuite commencé à rendre notre programme responsive.
    <br>
</p>
<details style="font-size:medium">
<summary style="font-size: xx-large">Informations techniques</summary> 
<div style="font-size:large">
  Bibliothèques principales utilisées : 
  <ul>
      <li>Pygame</li>
      <li>Time</li>
      <li>SQLite3</li>
  </ul>
  Bibliothèque secondaire utilisée :
  <ul>
      <li>PyAutoGui</li>
  </ul>
  Nous avons eu besoin de créer différentes classes : Bouton, Recherche (input)
  <br>
  <br>
  <summary>Points à améliorer : </summary>
  <ul>
      <li>Animations des boutons quand ils sont survolés</li>
      <li>Finir le responsive</li>
      <li>Affichage plus dynamique</li>
  </ul>
</div>
</details>
<details style="font-size:medium">
<summary style="font-size:xx-large">Fonctionnement</summary>
<ol type="I" style="font-size:large">
  <li>
    Pour chercher une espèce animale
    <ol>
        <li>Entrer un animal parmi la liste donnée, dans la barre de recherche</li>
        <li>Appuyer sur le bouton valider</li>
    </ol>
  </li>
  <li>
    Pour consulter directement le dictionnaire
    <ol>
        <li>Cliquer sur le bouton Dictionnaire</li>
    </ol>
  </li>
  <li>
    Pour naviguer sdans le dictionnaire
    <ol>
        <li>
        Appuyer sur les flèches droite/gauche de votre clavier
        <br>
        Ou cliquer sur les bords droit/gauche de la page
        </li>
        <li>Appuyer sur la grande flèche retour pour revenir en arrière</li>
        <li>Appuyer sur la croix ou echap pour fermer le dictionnaire</li>
    </ol>
  </li>
</ol>


</details>