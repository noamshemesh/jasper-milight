import milight
import re

PRIORITY = 10
WORDS = ["LIGHT", "LIGHTS", "ON", "OFF", "DIM", "WHITE", "FIRST", "SECOND", "THIRD", "FOURTH", "ALL"]

template = re.compile(r'.*\b(all|first|second|third|fourth)\b.*\blights\b.*\b(on|off|white|dim)\b.*', re.IGNORECASE)

words_to_numbers = {
    'all': 0,
    'first': 1,
    'second': 2,
    'third': 3,
    'forth': 4
}

def isValid(text):
    return bool(template.search(text))


def message(text, command, group):
    message = ''
    if command == 'dim':
        message += 'Dimming '
    elif command == 'white':
        message += 'Setting '
    else:
        message += 'Turning '

    if group == 'all':
        message += 'all lights '
    else:
        message += group + ' group '

    if command != 'dim':
        if command == 'white':
            message += 'to white'
        else:
            message += command

    return message


def handle(text, mic, profile):
    ip = profile['milight']['ip']
    port = profile['milight']['port'] or 8899
    wait_duration = profile['milight']['wait_duration'] or 200
    bulb_type = profile['milight']['bulb_type'] or ['rgbw']
    controller = milight.MiLight({'host': ip, 'port': port}, wait_duration=wait_duration)
    light = milight.LightBulb(bulb_type)

    m = template.search(text)
    light_group_string = m.group(0)
    command = m.group(1).lower()

    if not light_group_string:
        light_group_string = 'all'
    light_group_string = light_group_string.lower()
    light_group_int = words_to_numbers[light_group_string]

    try:
        if command == 'dim':
            controller.send(light.brightness(50, light_group_int))
        else:
            controller.send(light[command](light_group_string))
        mic.say(message(text, command, light_group_string))
    except:
        mic.say('Fail to send command to lights')
