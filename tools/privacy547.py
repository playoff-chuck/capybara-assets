#!/usr/bin/env python3
"""09.11.2026 23:02 (Martin «Datenschutzerklärung ja»): ES/PT/RU um die fehlenden Abschnitte
«Cloud-Sicherung» und «Fehler- und Nutzungsprotokoll» ergänzen (wie EN/DE), Kurzfassung angleichen.
Aufruf: python3 privacy547.py /srv/site/privacy/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

# Kurzfassung
rep('<li>Tu progreso se guarda en tu dispositivo.</li>',
    '<li>Tu progreso se guarda en tu dispositivo y, como copia de seguridad, en nuestro servidor bajo un código de restauración aleatorio, sin tu nombre.</li>')
rep('<li>Recogemos estadísticas anónimas de partidas (por ejemplo, oleada alcanzada, causa del fin de partida, oro) para equilibrar el juego. No contienen datos personales.</li>',
    '<li>Recogemos estadísticas anónimas de partidas (por ejemplo, oleada alcanzada, causa del fin de partida, oro) y un registro anónimo de errores para equilibrar el juego y corregir fallos. No contienen datos personales.</li>')
rep('<li>Seu progresso fica salvo no seu aparelho.</li>',
    '<li>Seu progresso fica salvo no seu aparelho e, como backup, no nosso servidor sob um código de restauração aleatório, sem seu nome.</li>')
rep('<li>Coletamos estatísticas anônimas das partidas (por exemplo, onda alcançada, causa do fim de jogo, ouro) para equilibrar o jogo. Elas não contêm dados pessoais.</li>',
    '<li>Coletamos estatísticas anônimas das partidas (por exemplo, onda alcançada, causa do fim de jogo, ouro) e um registro anônimo de erros para equilibrar o jogo e corrigir falhas. Elas não contêm dados pessoais.</li>')
rep('<li>Прогресс игры хранится на вашем устройстве.</li>',
    '<li>Прогресс игры хранится на вашем устройстве и, как резервная копия, на нашем сервере под случайным кодом восстановления — без вашего имени.</li>')
rep('<li>Мы собираем анонимную статистику раундов (например, достигнутая волна, причина окончания игры, золото), чтобы настраивать баланс. Она не содержит персональных данных.</li>',
    '<li>Мы собираем анонимную статистику раундов (например, достигнутая волна, причина окончания игры, золото) и анонимный журнал ошибок, чтобы настраивать баланс и исправлять ошибки. Они не содержат персональных данных.</li>')

ES = '''<h2>Copia de seguridad en la nube de tu progreso</h2>
<p>Para que tu progreso no se pierda nunca (por ejemplo, al cambiar de teléfono), el juego guarda una copia de tus datos de juego locales en nuestro servidor: progreso, mejores resultados, medallas, ajustes y tu nombre inventado. La copia se guarda bajo un código de restauración aleatorio que solo tú ves en el juego (☁ Cloud save). Solo guardamos una huella (hash) del código, nunca el código en sí, y ningún nombre, correo ni ID de dispositivo. Con el código puedes restaurar tu progreso en cualquier dispositivo. Guardamos las cinco últimas copias por código; se borran 24 meses después de la última actualización, o antes si nos lo pides y nos envías el código.</p>
<h2>Registro anónimo de errores y de uso</h2>
<p>Para encontrar y corregir fallos, el juego envía notas técnicas breves a nuestro servidor: mensajes de error del juego, la oleada y la pantalla en la que sales o vuelves, la versión del juego, una descripción aproximada del dispositivo (versión del sistema operativo y del navegador, tamaño de pantalla, clase de memoria) y un número de sesión aleatorio que se crea de nuevo en cada inicio y no se guarda en tu dispositivo. No se envía ningún nombre, número de jugador, ID de publicidad ni otro identificador. Solo usamos el registro de forma agregada. Las entradas se borran como máximo a los 90 días.</p>
'''
PT = '''<h2>Backup na nuvem do seu progresso</h2>
<p>Para que seu progresso nunca se perca (por exemplo, ao trocar de celular), o jogo faz um backup dos seus dados de jogo locais no nosso servidor: progresso, melhores resultados, medalhas, configurações e seu apelido inventado. O backup fica sob um código de restauração aleatório que só você vê no jogo (☁ Cloud save). Guardamos apenas uma impressão digital (hash) do código, nunca o código em si, e nenhum nome, e-mail ou ID do aparelho. Com o código você pode restaurar seu progresso em qualquer aparelho. Mantemos os cinco últimos backups por código; eles são apagados 24 meses após a última atualização, ou antes, se você pedir e enviar o código.</p>
<h2>Registro anônimo de erros e de uso</h2>
<p>Para encontrar e corrigir falhas, o jogo envia notas técnicas curtas ao nosso servidor: mensagens de erro do jogo, a onda e a tela em que você sai ou volta, a versão do jogo, uma descrição aproximada do aparelho (versão do sistema operacional e do navegador, tamanho da tela, classe de memória) e um número de sessão aleatório criado a cada início e não salvo no seu aparelho. Nenhum apelido, número de jogador, ID de publicidade ou outro identificador é enviado. Usamos o registro apenas de forma agregada. Os registros são apagados em no máximo 90 dias.</p>
'''
RU = '''<h2>Облачная копия прогресса</h2>
<p>Чтобы прогресс никогда не потерялся (например, при смене телефона), игра сохраняет копию ваших локальных игровых данных на нашем сервере: прогресс, лучшие результаты, медали, настройки и ваш придуманный позывной. Копия хранится под случайным кодом восстановления, который видите только вы в игре (☁ Cloud save). Мы храним только отпечаток (хеш) кода, но не сам код, и никакого имени, e-mail или идентификатора устройства. С помощью кода вы можете восстановить прогресс на любом устройстве. Мы храним пять последних копий на код; они удаляются через 24 месяца после последнего обновления или раньше, если вы попросите об этом и пришлёте код.</p>
<h2>Анонимный журнал ошибок и использования</h2>
<p>Чтобы находить и исправлять ошибки, игра отправляет на наш сервер короткие технические заметки: сообщения об ошибках игры, волну и экран, на котором вы выходите из игры или возвращаетесь, версию игры, примерное описание устройства (версия операционной системы и браузера, размер экрана, класс памяти) и случайный номер сеанса, который создаётся заново при каждом запуске и не сохраняется на устройстве. Позывной, номер игрока, рекламный идентификатор и другие идентификаторы не передаются. Мы используем журнал только в обобщённом виде. Записи удаляются не позднее чем через 90 дней.</p>
'''
rep('<h2>Perfil de jugador y número de jugador</h2>', ES + '<h2>Perfil de jugador y número de jugador</h2>')
rep('<h2>Perfil de jogador e número de jogador</h2>', PT + '<h2>Perfil de jogador e número de jogador</h2>')
rep('<h2>Профиль игрока и номер игрока</h2>', RU + '<h2>Профиль игрока и номер игрока</h2>')
open(p, "w", encoding="utf-8").write(s); print("ok privacy547")
