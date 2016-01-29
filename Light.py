import milight
import re

PRIORITY = 10
WORDS = ["LIGHT", "LIGHTS", "ON", "OFF", "DIM", "WHITE", "FIRST", "SECOND", "THIRD", "FOURTH", "ALL"]

template = re.compile(r'.*\b(turn|all|first|second|third|fourth)\b.*\blights\b.*\b(on|off|white|dim)\b.*', re.IGNORECASE)

words_to_numbers = {
    'turn': 0,
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
    port = profile['milight']['port'] if hasattr(profile['milight'], 'port') else 8899
    wait_duration = profile['milight']['wait_duration'] if hasattr(profile['milight'], 'wait_duration') else 0.200
    bulb_type = profile['milight']['bulb_type'] if hasattr(profile['milight'], 'bulb_type') else ['rgbw']
    controller = milight.MiLight({'host': ip, 'port': port}, wait_duration=wait_duration)
    light = milight.LightBulb(bulb_type)

    m = template.search(text)
    light_group_string = m.group(1)
    command = m.group(2).lower()

    if not light_group_string:
        light_group_string = 'all'
    light_group_string = light_group_string.lower()
    light_group_int = words_to_numbers[light_group_string]

    try:
        if command == 'dim':
            controller.send(light.brightness(50, light_group_int))
        else:
            print('sending to controller ' + command + '(' + str(light_group_int) + ')')
            lightCommand = getattr(light, command)
            controller.send(lightCommand(light_group_int))
        mic.say(message(text, command, light_group_string))
    except Exception as e:
        print(e)
        mic.say('Fail to send command to lights')


# tests
#
# class Mic:
#     def say(a, b):
#         print(b)
#
#
# handle("all lights on", Mic(), {"milight": {"ip": "192.168.1.109"}})
