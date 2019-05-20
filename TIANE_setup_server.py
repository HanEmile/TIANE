#!/usr/bin/env python3
from Crypto import Random
import shutil
import base64
import time
import json
import sys
import os
import argparse


def generate_key(length):
    key = Random.get_random_bytes(length)
    key_encoded = base64.b64encode(key)
    key_string = key_encoded.decode('utf-8')
    return key_string

def ja_nein_frage(fragentext, default):
    while True:
        eingabe = input(fragentext)
        if eingabe == '' or eingabe == ' ':
            return default
        elif 'j' in eingabe.lower() or 'y' in eingabe.lower():
            return True
        elif 'n' in eingabe.lower():
            return False
        else:
            print('Das habe ich leider nicht verstanden.')

def frage_erfordert_antwort(fragentext):
    while True:
        eingabe = input(fragentext)
        if eingabe == '' or eingabe == ' ':
            print('Bitte gib etwas ein.')
        else:
            return eingabe

def frage_mit_default(fragentext, default):
    eingabe = input(fragentext)
    if eingabe == '' or eingabe == ' ':
        return default
    else:
        return eingabe

def frage_nach_zahl(fragentext, default, allowed_answers=None):
    while True:
        eingabe = input(fragentext)
        if eingabe == '' or eingabe == ' ':
            return default
        try:
            eingabe = int(eingabe)
        except:
            print('Bitte gib eine Zahl ein.')
            continue
        if not allowed_answers == None:
            if not eingabe in allowed_answers:
                print('Bitte gib eine dieser Zahlen ein: {}'.format(allowed_answers))
                continue
        return eingabe

def bedingt_kopieren(ursprung, ziel, copy):
    if copy:
        if os.path.exists(ziel):
            return
        else:
            shutil.copy(ursprung, ziel)
    else:
        if os.path.exists(ziel):
            os.remove(ziel)

def tf2jn(tf):
    return "Ja" if tf else "Nein"

def end_config(config_data):
    print('Die Konfiguration deines {}-Servers ist abgeschlossen. Als nächstes solltest du mit den entsprechenden Assistenten Räume oder Nutzer einrichten.'.format(config_data['System_name']))
    text = input('[ENTER drücken zum beenden]')
    print('\nDie neuen Daten werden gespeichert...')
    with open('server/TIANE_config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print('\n[{}] Auf wiedersehen!\n'.format(config_data['System_name'].upper()))
    sys.exit()

########################### PARSER ############################

# Definiere einen neuen argument parser
parse = argparse.ArgumentParser(description="Server Setup", add_help=False)

# Definiere die Argumente
parse.add_argument('--name', help="Name des Sprachassistenten")
parse.add_argument('--server_name', help="Name des Servers")
parse.add_argument('--activation_phrase', help="Ansprache")
parse.add_argument('--location', help="Wohnort (für Wettervorhersagen)")
parse.add_argument('--keylength', help="Länge des Schlüssels", choices=["8", "16", "32"])
parse.add_argument('--telegram_key', help="Telegram Key (@BotFather anschreiben)")

parse.add_argument('-camera', action="store_true", help="Nutze das Kamera Modul")
parse.add_argument('-nocamera', action="store_true", help="Nutze nicht das Kamera Modul")
parse.add_argument('-facerec', action="store_true", help="Nutze das Gesichteserkennungs Modul")
parse.add_argument('-ui', action="store_true", help="Zeige die Kamera-feeds an") 

parse.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='Zeigt diese hilfe Nachricht an und beendet das Program')

# Parse die Argumente und speichere sie entsprechend
args = parse.parse_args()
system_name = args.name
server_name = args.server_name
activation_phrase = args.activation_phrase
location = args.location
keylength = args.keylength
telegram_key = args.telegram_key

camera = args.camera
nocamera = args.nocamera
facerec = args.facerec
ui = args.ui

########################### ANFANG ###########################
print('Willkommen zum Setup-Assistenten für deinen neuen Sprachassistenten.\n'
      'Im ersten Schritt geht es um die Einrichtung deines TIANE-Servers. \n'
      'Dieser Setup-Assistent wird dich mit Fragen durch die Einrichtung führen.\n'
      'Bitte gib deine Antworten ein und bestätige sie mit [ENTER].\n'
      'Wenn du bei einer Frage die vorgegebene Standard-Antwort übernehmen willst, reicht es, wenn du einfach [ENTER] drückst, ohne etwas einzugeben.')
time.sleep(1)
text = input('[ENTER drücken zum fortfahren]')

if not os.path.exists('server/TIANE_config.json'):
    print('\n[ERROR] Die nötigen Dateien (Ordner "server") für diesen Setup-Schritt konnten nicht gefunden werden.\n'
          'Hast du die Dateien heruntergeladen?\n'
          'Befindet sich das Setup-Skript im richtigen Ordner?')
    text = input('[ENTER drücken zum beenden]')
    sys.exit()

with open('server/TIANE_config.json', 'r') as config_file:
    config_data = json.load(config_file)

if system_name != None:
    config_data['System_name'] = system_name 
    print(f"name: {system_name}")
else:
    default_name = config_data['System_name']
    system_name = input('\nBitte gib einen Namen für deinen Sprachassistenten ein (z.B. "TIANE", "Alexa" oder "J.A.R.V.I.S") '
                        '[Standard ist "{}"]: '.format(default_name))
    if system_name == '' or system_name == ' ':
        config_data['System_name'] = default_name
        system_name = default_name
    else:
        config_data['System_name'] = system_name
    config_data['Local_storage']['system_name'] = system_name
    print('Okay, dein neuer Sprachassistent wird {} heißen.\n'.format(system_name))
    time.sleep(1)

if server_name != None:
    config_data['Server_name'] = server_name 
    print(f"server_name: {server_name}")
else:
    default_name = config_data['Server_name']
    if default_name == '':
        default_name = system_name.upper() + '_SERVER'
    server_name = input('\nBitte gib einen Namen für deinen {}-Server ein [Standard ist "{}"]: '.format(system_name, default_name))
    if server_name == '' or server_name == ' ' or type(server_name) != type('text'):
        config_data['Server_name'] = default_name
        server_name = default_name
    else:
        config_data['Server_name'] = server_name
    config_data['Local_storage']['server_name'] = server_name
    print('Okay, dein {}-Server wird {} heißen.\n'.format(system_name, server_name))
    time.sleep(1)

if activation_phrase != None:
    config_data['Activation_Phrase'] = activation_phrase 
    print(f"activation_phrase: {activation_phrase}")
else:
    default_phrase = config_data['Activation_Phrase']
    if default_phrase == '':
        default_phrase = 'Hey ' + system_name + '!'
    activation_phrase = input('\nWie möchtest du {} in Zukunft ansprechen? [Standard ist "{}"]: '.format(system_name, default_phrase))
    if activation_phrase == '' or activation_phrase == ' ' or type(activation_phrase) != type('text'):
        config_data['Activation_Phrase'] = default_phrase
        activation_phrase = default_phrase
    else:
        config_data['Activation_Phrase'] = activation_phrase
    config_data['Local_storage']['activation_phrase'] = activation_phrase
    print('Okay, du kannst {} später mit "{}" ansprechen.'.format(system_name, activation_phrase))
    time.sleep(0.5)
    print('(Info: Damit dein Sprachassistent auf diese Ansprache auch tatsächlich reagiert, musst du '
          'zunächst ein Stimmmodell trainieren (siehe Installationsanleitung))\n')
    time.sleep(1)

if location != None:
    config_data['Home_location'] = location 
    print(f"location: {location}")
else:
    default_location = config_data['Home_location']
    if not default_location == 'None':
        location = input('\nBitte gib deinen Wohnort ein (optional, hilfreich für Funktionen wie Wettervorhersagen) [Standard ist "{}"]: '.format(default_location))
        if location == '' or location == ' ' or type(location) != type('text'):
            config_data['Home_location'] = default_name
            location = default_location
        else:
            config_data['Home_location'] = location
    else:
        location = input('\nBitte gib deinen Wohnort ein (optional, hilfreich für Funktionen wie Wettervorhersagen): ')
        if location == '' or location == ' ' or type(location) != type('text'):
            config_data['Home_location'] = default_location
            location = default_location
        else:
            config_data['Home_location'] = location
    config_data['Local_storage']['home_location'] = location
    if location == 'None':
        print('Okay, du hast keinen Wohnort festgelegt.\n')
    else:
        print('Okay, {} wird "{}" als deinen Wohnort annehmen.\n'.format(system_name, location))
    time.sleep(1)

if keylength in ["8", "16", "32"]:
    key_len = keylength
    config_data['TNetwork_Key'] = generate_key(int(key_len))
    print(f"keylength: {keylength}")
else:
    print('Als nächstes geht es um die Generierung eines Schlüssels für die sichere Kommunikation zwischen deinen {}-Geräten.'.format(system_name))
    text = input('[ENTER drücken zum fortfahren]')
    if not config_data['TNetwork_Key'] == '':
        print('\nACHTUNG: Es wurde bereits eine vorhandene Konfiguration erkannt.\n'
              'Möchtest du einen neuen Schlüssel generieren? Wenn du "Ja" auswählst, musst du Räume, die du bereits mit dem Setup-Assistenten eingerichtet hast, neu einrichten.')
        antwort = ja_nein_frage('Neuen Schlüssel generieren [Ja / Nein]? [Standard ist "Nein"]: ', False)
        if antwort == True:
            print('\nBitte gib die Länge für deinen neuen Schlüssel (in Byte) ein.\n'
                  'Erlaubte Längen sind 8, 16 und 32 Byte.\n'
                  'Ein längerer Schlüssel ist deutlich sicherer, kann aber auf manchen Geräten zu Geschwindigkeitsproblemen führen.')
            key_len = frage_nach_zahl('Länge des Sicherheitsschlüssels (8, 16 oder 32) [Standard ist 32]: ', 32, allowed_answers=[8,16,32])
            print('Ein neuer Schlüssel der Länge {} wird generiert...\n'.format(key_len))
            config_data['TNetwork_Key'] = generate_key(key_len)
            time.sleep(1)
        else:
            print('Es wird kein neuer Schlüssel generiert.\n')
            time.sleep(1)
    else:
        print('\nBitte gib die Länge für deinen neuen Schlüssel (in Byte) ein.\n'
              'Erlaubte Längen sind 8, 16 und 32 Byte.\n'
              'Ein längerer Schlüssel ist deutlich sicherer, kann aber auf manchen Geräten zu Geschwindigkeitsproblemen führen.')
        key_len = frage_nach_zahl('Länge des Sicherheitsschlüssels (8, 16 oder 32) [Standard ist 32]: ', 32, allowed_answers=[8,16,32])
        print('Ein neuer Schlüssel der Länge {} wird generiert...\n'.format(key_len))
        config_data['TNetwork_Key'] = generate_key(key_len)
        time.sleep(1.5)

if telegram_key != None:
    config_data['telegram_key'] = telegram_key 
    print(f"telegram_key: {telegram_key}")
else:
    default = config_data['telegram']
    antwort = ja_nein_frage('Möchtest du deinen Sprachassistenten via Telegram anschreiben können (Voraussetzung: telepot installiert) [Ja / Nein]? [Standard ist "{}"]: '.format(tf2jn(default)), default)
    config_data['telegram'] = antwort
    if antwort == True:
        print('Okay, du wirst später mit {} auf Telegram schreiben können. Dafür braucht dein Sprachassistent aber zuerst einen Telegram-Account: Schreibe dafür am besten einfach "@BotFather" auf Telegram an.\n'.format(system_name))
        time.sleep(1)

        default = config_data['telegram_key']
        if default == '':
            key = frage_erfordert_antwort('Bitte füge das Bot-Token ein, das du von @BotFather erhalten hast: ')
        else:
            key = frage_mit_default('Bitte füge das Bot-Token ein, das du von @BotFather erhalten hast [Standard ist "{}"]: '.format(default), default)
        config_data['telegram_key'] = key
        print('\n')
    else:
        print('Okay, für {} wird keine Telegram-Unterstützung eingerichtet.\n'.format(system_name))
    time.sleep(1)

if camera == True or facerec == True or ui == True or nocamera == True:
    pass
else:
    print('\nIm letzten Schritt kannst du festlegen, welche der mitgelieferten optionalen Module dein Sprachassistent verwenden soll.\n'
          'Du kannst die verwendeten Module jederzeit im Ordner "server/modules(/continuous)" einsehen und bearbeiten, '
          'optionale Module, die du bei dieser Einrichtung noch nicht auswählst, finden sich im Ordner "server/resources/optional_modules".')
    text = input('[ENTER drücken zum fortfahren]')

print('\n')

if nocamera == True:
    pass
else:
    if camera == True:
        config_data['use_cameras'] = True
        print(f"use cameras: {camera}")
        bedingt_kopieren('server/resources/optional_modules/recieve_cameras.py', 'server/modules/continuous/recieve_cameras.py', True)

        if facerec == True:
            config_data['use_facerec'] = True 
            print(f"use facerec: {facerec}")
            bedingt_kopieren('server/resources/optional_modules/face_recognition.py', 'server/modules/continuous/face_recognition.py', True)
            bedingt_kopieren('server/resources/optional_modules/retrain_facerec.py', 'server/modules/retrain_facerec.py', True)
        else:
            default = config_data['use_facerec']
            antwort = ja_nein_frage('Soll dein Sprachassistent Gesichtserkennung verwenden (Voraussetzung: OpenCV, dlib, scikit-learn und face_recognition installiert) [Ja / Nein]? [Standard ist "{}"]: '.format(tf2jn(default)), default)
            config_data['use_facerec'] = antwort
            bedingt_kopieren('server/resources/optional_modules/face_recognition.py', 'server/modules/continuous/face_recognition.py', antwort)
            bedingt_kopieren('server/resources/optional_modules/retrain_facerec.py', 'server/modules/retrain_facerec.py', antwort)
            if antwort == True:
                print('Okay, dein {}-Server wird mit dem Modul "face_recognition.py" Gesichter in den Kamerabildern erkennen können.\n'.format(system_name))
            else:
                print('Okay, es werden keine Gesichtserkennungs-Funktionen verwendet.\n')
            time.sleep(1)

        if ui == True:
            config_data['use_interface'] = True 
            print(f"use ui: {ui}")
            bedingt_kopieren('server/resources/optional_modules/POI_Interface.py', 'server/modules/continuous/POI_Interface.py', True)
            bedingt_kopieren('server/resources/optional_modules/POI_Interface_controls.py', 'server/modules/POI_Interface_controls.py', True)

        else:
            default = config_data['use_interface']
            antwort = ja_nein_frage('Soll dein Sprachassistent ein Grafisches Interface zur Anzeige der Kamerabilder verwenden (Voraussetzung: OpenCV installiert) [Ja / Nein]? [Standard ist "{}"]: '.format(tf2jn(default)), default)
            config_data['use_interface'] = antwort
            bedingt_kopieren('server/resources/optional_modules/POI_Interface.py', 'server/modules/continuous/POI_Interface.py', antwort)
            bedingt_kopieren('server/resources/optional_modules/POI_Interface_controls.py', 'server/modules/POI_Interface_controls.py', antwort)
            if antwort == True:
                print('Okay, dein {}-Server wird mit dem Modul "POI_Interface.py" Kamerabilder und sonstige Daten in einem grafischen Interface anzeigen.\n'.format(system_name))
            else:
                print('Okay, es wird kein grafisches Interface verwendet.\n')
            time.sleep(1)

    else:
        default = config_data['use_cameras']
        antwort = ja_nein_frage('Soll dein Sprachassistent Kameras verwenden [Ja / Nein]? [Standard ist "{}"]: '.format(tf2jn(default)), default)
        config_data['use_cameras'] = antwort
        bedingt_kopieren('server/resources/optional_modules/recieve_cameras.py', 'server/modules/continuous/recieve_cameras.py', antwort)
        if antwort == True:
            print('Okay, dein {}-Server wird mit dem Modul "recieve_cameras.py" Kamerabilder von Räumen empfangen können.\n'.format(system_name))
            time.sleep(1)
        else:
            print('Okay, es werden keine Kamera-Funktionen verwendet.\n')
            time.sleep(1)

end_config(config_data)
