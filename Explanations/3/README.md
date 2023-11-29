# TP3 SECU : SVP soyez cools

Bon c'est le titre du TP. Je le redis là : SVP soyez cools.

Ce que je vous demande dans ce TP, c'est discutable. Soyez cools.

Faisons simple : un exercice de prises d'informations en situation réelle. Prouvez-moi que vous êtes des vrais hackerz. Je veux un état des lieux du réseau YNOV.

Soyez cools, respectez **scrupuleusement** les règles suivantes :

- **pas de scans réseau répétés**, soyez très très parcimonieux avec `nmap`
  - `nmap` il envoie des trames dans tous les sens
  - vous devez maîtriser la commande `nmap` que vous envoyez
  - testez avec des VMs s'il faut, et Wireshark, faites le nécessaire pour PIGER
  - puis c'est super cramé sur un réseau un mec qui fait des `nmap`...
- **pas de scans de port agressif**
  - idem, `nmap` et le scan de port, c'est vite super violent pour la machine qui se fait scanner
  - si c'était pas cramé avec le scan réseau, là c'est cramé, tu testes la connexion de façon agressive sur 65535 ports...
  - préférez scan quelques ports spécifiques sur quelques machines spécifiques
  - faites des scans de ports entre vous avant de scan des random
  - attention avec le scan de range de ports
- **pas de comportement chelou de ouf**
  - j'sais pas moi, vous prenez pas pour des agents secrets non plus
  - restez dans les limites physiques de l'espace qui vous est attribué, et dans les limites légales et éthiques évidentes que l'exercice impose de titiller
  - ne rentrez pas dans une salle où il y a un cours
  - soyez discrets en fait quoi, éviter que les gens se demandent toute la journée c'est quoi ces 3 pelos qui se marrent avec leur PC à la main et un shell ouvert, qui se baladent toute la journée partout dans le bâtiment
  - think before, act fast
- **si vous trouvez vraiment un truc vous ne l'exploitez pas**
  - ça tombe sous le sens SVP, on fait un exercice de prises d'informations

➜ **Globalement, une bonne démarche à adopter :**

- cherchez des idées
- faites de la veille
- tester des techniques en local
  - entre vous
  - avec des VMs
- une fois la technique sûre, vous l'utilisez pour récolter des informations
- encore une fois ça doit être discret, rapide, efficace

## Rendu

🌞 **Je veux un rapport format Markdown**

➜ **Vous avez jusqu'à la date de rendu de TP pour fournir un rapport**

- le plus détaillé possible
- un truc lisible, pas un bordel, savoir faire des rapports, ça fait partie du skill j'vous assure
- ciblé sur le réseau que je vous communiquerai en cours
- c'est une démarche de prise d'informations, mais qui est écrite avec la recherche de trous de sécu/d'exploitation en tête
- soulignez si vous trouvez des choses à risque ou douteuses en terme de sécurité

➜ **Trucs à priori élémentaires à inclure dans le rapport :**

- adresses MAC et IP de tous les clients du réseau
  - y'aura plein de clients qui bougent (les étudiants qui vont et viennent)
  - repérer les équipements qui ne bougent pas (routeurs, serveurs, PC de la pédagogie, etc.) qui seraient joignables
- essayer d'identifier si d'autres LANs sont joignables ou si on est isolés
- ce qui serait amusant d'inclure :
- les bornes WiFi (emplacement, adresse MAC)
- les switches apparents s'il y en a
- est-ce qu'il y a des ports RJ45 accessibles qui fonctionnent ? (essayez de récup une IP en DHCP, ou try IP statique cohérente)
- emplacement physique de la salle serveur (vous n'y rentrez pas EVIDEMMENT, même pas tu touches la poignée)

➜ **Pourquoi pas tester :**

- du scan de ports sur quelques machines, choisissez bien, soyez extrêmement parcimonieux, please
- détection d'OS pour les machines du réseau
- est-ce qu'il y a pas d'autres équipements connectés par-ci par-là que vous pouvez pas joindre depuis le réseau, mais qui y sont manifestement connectés

**Soyez créatifs.**
