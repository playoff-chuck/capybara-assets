#!/usr/bin/env python3
"""V536 (Martin 09.11. 21:32): Datenschutzerklärung um das Spielerprofil mit Spieler-Nummer ergänzen (EN/ES/PT/DE/RU).
Aufruf: python3 privacy536.py /srv/site/privacy/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

# Gültigkeitsdatum
rep('Effective date: 4 November 2026.', 'Effective date: 9 November 2026.')
rep('Fecha de entrada en vigor: 4 de noviembre de 2026.', 'Fecha de entrada en vigor: 9 de noviembre de 2026.')
rep('Data de vigência: 4 de novembro de 2026.', 'Data de vigência: 9 de novembro de 2026.')
rep('Gültig ab: 4. November 2026.', 'Gültig ab: 9. November 2026.')
rep('Действует с 4 ноября 2026 г.', 'Действует с 9 ноября 2026 г.')

# Kurz gesagt: neuer Punkt
rep('<li>We do not sell or share data. Our server is in Finland (EU).</li>',
    '<li>The game keeps a player profile under a random player number (progress, play time, device description) so we can help players and improve the game – without your real name.</li>\n<li>We do not sell or share data. Our server is in Finland (EU).</li>')
rep('<li>No vendemos ni compartimos datos. Nuestro servidor está en Finlandia (UE).</li>',
    '<li>El juego guarda un perfil de jugador bajo un número de jugador aleatorio (progreso, tiempo de juego, descripción del dispositivo) para poder ayudarte y mejorar el juego, sin tu nombre real.</li>\n<li>No vendemos ni compartimos datos. Nuestro servidor está en Finlandia (UE).</li>')
rep('<li>Não vendemos nem compartilhamos dados. Nosso servidor fica na Finlândia (UE).</li>',
    '<li>O jogo mantém um perfil de jogador sob um número de jogador aleatório (progresso, tempo de jogo, descrição do aparelho) para podermos ajudar você e melhorar o jogo, sem seu nome real.</li>\n<li>Não vendemos nem compartilhamos dados. Nosso servidor fica na Finlândia (UE).</li>')
rep('<li>Wir verkaufen oder teilen keine Daten. Unser Server steht in Finnland (EU).</li>',
    '<li>Das Spiel führt ein Spielerprofil unter einer zufälligen Spieler-Nummer (Fortschritt, Spielzeit, Gerätebeschreibung), damit wir Spielern helfen und das Spiel verbessern können – ohne deinen echten Namen.</li>\n<li>Wir verkaufen oder teilen keine Daten. Unser Server steht in Finnland (EU).</li>')
rep('<li>Мы не продаём и не передаём данные. Наш сервер находится в Финляндии (ЕС).</li>',
    '<li>Игра ведёт профиль игрока под случайным номером игрока (прогресс, время игры, описание устройства), чтобы мы могли помогать игрокам и улучшать игру, — без вашего настоящего имени.</li>\n<li>Мы не продаём и не передаём данные. Наш сервер находится в Финляндии (ЕС).</li>')

# Daten auf dem Gerät: verlassen das Gerät nur wie unten beschrieben
rep('This data never leaves your device unless you take part in the world lists described below.', 'This data leaves your device only as described below.')
rep('Estos datos no salen de tu dispositivo salvo que participes en las listas mundiales descritas abajo.', 'Estos datos solo salen de tu dispositivo como se describe abajo.')
rep('Esses dados não saem do aparelho, a menos que você participe dos rankings descritos abaixo.', 'Esses dados só saem do aparelho da forma descrita abaixo.')
rep('Diese Daten verlassen dein Gerät nur, wenn du an den unten beschriebenen Weltlisten teilnimmst.', 'Diese Daten verlassen dein Gerät nur wie unten beschrieben.')
rep('Эти данные не покидают устройство, если вы не участвуете в мировых таблицах, описанных ниже.', 'Эти данные покидают устройство только так, как описано ниже.')

# Neuer Abschnitt vor «Server, IP …»
EN = '''<h2>Player profile and player number</h2>
<p>The game creates a random player number on your device (for example K7Q2-9HXM, shown in the settings under "Support info"). Under this number it regularly sends a player profile to our server: your made-up call sign, chosen hero and outfit, game language and version; your progress (current and best wave, checkpoint, stars, medals, squad level, missions, daily streak, number of invited friends, best Nuts levels); totals (splats, lines, waves, runs); play time and screen time (how long the game was open); number and cause of game overs; and a device description (operating system and version, device model, app or browser version, screen size, number of processor cores and memory class, device language and time zone). We also store when the profile was first and last received and how often the game was started.</p>
<p>The profile contains no real name, no e-mail, no advertising ID, no location and no IP address. It is pseudonymous personal data. Only the developer can view it, in a protected admin view; it is not shown to other players and not shared. We use it to see how far players get, to improve the game and to help you when you contact support. Legal basis: our legitimate interest in improving the game and supporting players (Art. 6(1)(f) GDPR). Profiles are deleted 24 months after the last update. You can object or ask for deletion at any time: send us your player number by e-mail.</p>
'''
ES = '''<h2>Perfil de jugador y número de jugador</h2>
<p>El juego crea en tu dispositivo un número de jugador aleatorio (por ejemplo K7Q2-9HXM, visible en los ajustes, en «Support info»). Con ese número envía periódicamente un perfil de jugador a nuestro servidor: tu nombre inventado, el héroe y el atuendo elegidos, el idioma y la versión del juego; tu progreso (oleada actual y mejor oleada, punto de control, estrellas, medallas, nivel de escuadrón, misiones, racha diaria, número de amigos invitados, mejores niveles de Nuts); totales (splats, líneas, oleadas, partidas); tiempo de juego y tiempo de pantalla (cuánto tiempo estuvo abierto el juego); número y causa de los fines de partida; y una descripción del dispositivo (sistema operativo y versión, modelo, versión de la app o del navegador, tamaño de pantalla, número de núcleos y clase de memoria, idioma del dispositivo y zona horaria). También guardamos cuándo se recibió el perfil por primera y última vez y cuántas veces se inició el juego.</p>
<p>El perfil no contiene nombre real, correo electrónico, ID de publicidad, ubicación ni dirección IP. Son datos personales seudónimos. Solo el desarrollador puede verlo, en una vista de administración protegida; no se muestra a otros jugadores ni se cede. Lo usamos para ver hasta dónde llegan los jugadores, mejorar el juego y ayudarte si contactas con soporte. Base jurídica: nuestro interés legítimo en mejorar el juego y atender a los jugadores (art. 6.1.f RGPD). Los perfiles se borran 24 meses después de la última actualización. Puedes oponerte o pedir su supresión en cualquier momento enviándonos tu número de jugador por correo.</p>
'''
PT = '''<h2>Perfil de jogador e número de jogador</h2>
<p>O jogo cria no seu aparelho um número de jogador aleatório (por exemplo K7Q2-9HXM, visível nas configurações, em «Support info»). Com esse número, ele envia regularmente um perfil de jogador ao nosso servidor: seu apelido inventado, herói e roupa escolhidos, idioma e versão do jogo; seu progresso (onda atual e melhor onda, checkpoint, estrelas, medalhas, nível do esquadrão, missões, sequência diária, número de amigos convidados, melhores níveis Nuts); totais (splats, linhas, ondas, partidas); tempo de jogo e tempo de tela (quanto tempo o jogo ficou aberto); número e causa dos fins de jogo; e uma descrição do aparelho (sistema operacional e versão, modelo, versão do app ou do navegador, tamanho da tela, número de núcleos e classe de memória, idioma do aparelho e fuso horário). Também guardamos quando o perfil foi recebido pela primeira e pela última vez e quantas vezes o jogo foi iniciado.</p>
<p>O perfil não contém nome real, e-mail, ID de publicidade, localização nem endereço IP. São dados pessoais pseudonimizados. Somente o desenvolvedor pode vê-lo, em uma área de administração protegida; ele não é mostrado a outros jogadores nem compartilhado. Usamos o perfil para ver até onde os jogadores chegam, melhorar o jogo e ajudar você se entrar em contato com o suporte. Base legal: nosso legítimo interesse em melhorar o jogo e atender os jogadores (art. 6(1)(f) do RGPD; no Brasil, art. 7, IX da LGPD). Os perfis são apagados 24 meses após a última atualização. Você pode se opor ou pedir a exclusão a qualquer momento enviando seu número de jogador por e-mail.</p>
'''
DE = '''<h2>Spielerprofil und Spieler-Nummer</h2>
<p>Das Spiel erzeugt auf deinem Gerät eine zufällige Spieler-Nummer (z. B. K7Q2-9HXM, zu sehen im Zahnrad-Menü unter „Support info“). Unter dieser Nummer sendet es regelmäßig ein Spielerprofil an unseren Server: dein ausgedachtes Rufzeichen, gewählte Figur und Outfit, Spielsprache und -version; deinen Fortschritt (aktuelle und beste Welle, Checkpoint, Sterne, Medaillen, Squad Level, Missionen, Daily-Kette, Zahl der geworbenen Freunde, beste Nuts-Level); Summen (Splats, Reihen, Wellen, Läufe); Spielzeit und Bildschirmzeit (wie lange das Spiel geöffnet war); Anzahl und Ursache der Spielenden (Game over); sowie eine Gerätebeschreibung (Betriebssystem und Version, Gerätemodell, App- bzw. Browserversion, Bildschirmgröße, Zahl der Prozessorkerne und Speicherklasse, Gerätesprache und Zeitzone). Außerdem speichern wir, wann das Profil zuerst und zuletzt eingegangen ist und wie oft das Spiel gestartet wurde.</p>
<p>Das Profil enthält keinen echten Namen, keine E-Mail, keine Werbe-ID, keinen Standort und keine IP-Adresse. Es sind pseudonyme personenbezogene Daten. Nur der Entwickler kann es in einer geschützten Admin-Ansicht sehen; es wird anderen Spielern nicht angezeigt und nicht weitergegeben. Wir nutzen es, um zu sehen, wie weit Spieler kommen, um das Spiel zu verbessern und um dir zu helfen, wenn du dich an den Support wendest. Rechtsgrundlage: unser berechtigtes Interesse an der Verbesserung des Spiels und der Betreuung der Spieler (Art. 6 Abs. 1 lit. f DSGVO). Profile werden 24 Monate nach der letzten Aktualisierung gelöscht. Du kannst jederzeit widersprechen oder die Löschung verlangen: schick uns dazu deine Spieler-Nummer per E-Mail.</p>
'''
RU = '''<h2>Профиль игрока и номер игрока</h2>
<p>Игра создаёт на вашем устройстве случайный номер игрока (например, K7Q2-9HXM, он виден в настройках в разделе «Support info»). Под этим номером игра регулярно отправляет на наш сервер профиль игрока: ваш придуманный позывной, выбранного героя и наряд, язык и версию игры; ваш прогресс (текущая и лучшая волна, контрольная точка, звёзды, медали, уровень отряда, миссии, ежедневная серия, число приглашённых друзей, лучшие уровни Дурдома); итоговые значения (сплэты, линии, волны, забеги); время игры и экранное время (сколько игра была открыта); число и причины окончаний игры; описание устройства (операционная система и версия, модель устройства, версия приложения или браузера, размер экрана, число ядер процессора и класс памяти, язык устройства и часовой пояс). Также мы храним, когда профиль был получен впервые и в последний раз и сколько раз запускалась игра.</p>
<p>Профиль не содержит настоящего имени, e-mail, рекламного идентификатора, местоположения и IP-адреса. Это псевдонимизированные персональные данные. Видеть профиль может только разработчик в защищённом административном разделе; другим игрокам он не показывается и третьим лицам не передаётся. Мы используем его, чтобы видеть, как далеко продвигаются игроки, улучшать игру и помогать вам при обращении в поддержку. Правовое основание: наш законный интерес в улучшении игры и поддержке игроков (ст. 6(1)(f) GDPR). Профили удаляются через 24 месяца после последнего обновления. Вы можете в любой момент возразить или потребовать удаления, прислав нам свой номер игрока по e-mail.</p>
'''
rep('<h2>Server, IP address, cookies</h2>', EN + '<h2>Server, IP address, cookies</h2>')
rep('<h2>Servidor, dirección IP, cookies</h2>', ES + '<h2>Servidor, dirección IP, cookies</h2>')
rep('<h2>Servidor, endereço IP, cookies</h2>', PT + '<h2>Servidor, endereço IP, cookies</h2>')
rep('<h2>Server, IP-Adresse, Cookies</h2>', DE + '<h2>Server, IP-Adresse, Cookies</h2>')
rep('<h2>Сервер, IP-адрес, cookies</h2>', RU + '<h2>Сервер, IP-адрес, cookies</h2>')
open(p, "w", encoding="utf-8").write(s); print("ok privacy536")
