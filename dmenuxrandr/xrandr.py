import re
from subprocess import check_output, call

outputLine = re.compile(r'^([^ ]*) (connected|disconnected)( primary)?( \d+x\d+\+\d+\+\d+)?.*$')
modeLine = re.compile(r'^ +([^ ]+)')


def get_xrandr():
    """
    Gets the current monitors status as a dict { [monitorName]: { name, isMapped, isConnected, isPrimary, modes } where:
        name is the output name (example: DP1) as a string
        isMapped is a boolean describing whether the output is configured to display something
        isConnected is a boolean describing whether there is a monitor connected to that output
        isPrimary is a boolean set to True if that output is the primary output
        modes is an array of possible output modes as strings (in the "1234x456" format
    @return:
    """
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


def set_mode(output: str, mode: str):
    """
    Changes the mode for the specified output
    @param output: The output name
    @param mode: The mode to switch to (example: "1920w1080")
    @return: Nothing
    """
    call(['xrandr', '--output', output, '--mode', mode])


def set_position(output: str, position: str, reference: str, auto_mode=False):
    """
    Moves the output relatively to another
    @param output: The output to move
    @param position: The position to move it to (example "--above"):
    @param reference: The output to use as a reference
    @param auto_mode: Whether to add a --auto flag, usefull for unMapped outputs, defaults to False
    @return: Nothing
    """
    command = ['xrandr', '--output', output, position, reference]
    if auto_mode:
        command.append('--auto')
    call(command)


def set_off(output: str):
    """
    Turns off an output (effectively unMapping it)
    @param output: The output to deactivate
    @return: Nothing
    """
    call(['xrandr', '--output', output, '--off'])
