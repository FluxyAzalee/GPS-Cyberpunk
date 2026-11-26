<?php
// Petit relais pour lire les données des bus Sitac depuis le navigateur (ajoute l'autorisation CORS)
//   proxy-bus.php            -> position des bus en temps réel
//   proxy-bus.php?type=gtfs  -> horaires théoriques (pour connaître le numéro des lignes)
header('Access-Control-Allow-Origin: *');
if (isset($_GET['type']) && $_GET['type'] === 'gtfs') {
    header('Content-Type: application/zip');
    echo file_get_contents('https://zenbus.net/gtfs/static/download.zip?dataset=sitac-calais-rt&src=true');
} else {
    header('Content-Type: application/octet-stream');
    echo file_get_contents('https://zenbus.net/gtfs/rt/poll.proto?dataset=sitac-calais-rt&src=true');
}
