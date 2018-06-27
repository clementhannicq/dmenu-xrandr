import re
from subprocess import check_output, call

outputLine = re.compile('^([^ ]*) (connected|disconnected)( primary)?( \d+x\d+\+\d+\+\d+)?.*$')
modeLine = re.compile('^ +([^ ]+)')


def get_xrandr():
    outputs = {}

    raw_xrandr = check_output(['xrandr'])

    current_output = None

    for line in str(raw_xrandr).split("\\n"):
        if re.match(outputLine, line):
            (outputName, status, isPrimary, isMapped) = re.match(outputLine, line).groups()
            outputs[outputName] = {
                'name': outputName,
                'modes': [],
                'isMapped': bool(isMapped),
                'isConnected': status == 'connected',
                'isPrimary': bool(isPrimary)
            }
            current_output = outputName
        elif re.match(modeLine, line) and current_output:
            (mode,) = re.match(modeLine, line).groups()
            outputs[current_output]['modes'].append(mode)

    return outputs


def set_mode(output, mode):
    call(['xrandr', '--output', output, '--mode', mode])


def set_position(output, position, reference, auto_mode=False):
    command = ['xrandr', '--output', output, position, reference]
    if auto_mode:
        command.append('--auto')
    call(command)


def set_off(output):
    call(['xrandr', '--output', output, '--off'])
