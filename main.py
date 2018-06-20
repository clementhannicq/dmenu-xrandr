from itertools import chain

from prompt import prompt, InvalidValue
from xrandr import get_xrandr, set_off, set_mode, set_position

MOVE = 'Position'
MODE = 'Mode'
SHUTDOWN = 'Shutdown'
ACTIONS_PRIMARY = [MODE]
ACTIONS_SEGONDARY = [MOVE, MODE, SHUTDOWN]
TOP = 'Above'
BOTTOM = 'Below'
LEFT = 'Left of'
RIGHT = 'Right of'
SAME = 'Same as'
DIRECTIONS = [SAME, TOP, BOTTOM, LEFT, RIGHT]

XRANDR_OPTIONS_MOVE = {
    TOP: '--above',
    BOTTOM: '--below',
    LEFT: '--left-of',
    RIGHT: '--right-of',
    SAME: '--same-as',
}


def run_move(outputs, selected_output, is_auto=False):
    direction = prompt(DIRECTIONS, prompt=selected_output['name'])
    
    remaining_outputs = [outputName for outputName, output in outputs.items() if output != selected_output and output['isConnected'] and output['isMapped']]

    reference = prompt(remaining_outputs, prompt=(selected_output['name'] + ' ' + direction))

    set_position(selected_output['name'], XRANDR_OPTIONS_MOVE[direction], reference, auto_mode=is_auto)


def run_mode(selected_output):
    mode = prompt(selected_output['modes'], prompt=selected_output['name'])
    set_mode(selected_output['name'], mode)


def run_shutdown(selected_output):
    set_off(selected_output['name'])


def __main__():
    try:
        outputs = get_xrandr()

        connected_mapped_outputs = {outputName: output for outputName, output in outputs.items() if output['isConnected'] and output['isMapped']}
        connected_unmapped_outputs = {outputName: output for outputName, output in outputs.items() if output['isConnected'] and not output['isMapped']}
        outputs_to_cleanup = {('clean ' + outputName): output for outputName, output in outputs.items() if not output['isConnected'] and output['isMapped']}
        main_choices = sorted(chain.from_iterable([
            connected_unmapped_outputs,
            connected_mapped_outputs,
            outputs_to_cleanup,
        ]))

        selected_output_name = prompt(main_choices)

        if selected_output_name in connected_mapped_outputs:
            selected_output = connected_mapped_outputs[selected_output_name]

            if selected_output['isPrimary']:
                actions = ACTIONS_PRIMARY
            else:
                actions = ACTIONS_SEGONDARY
            action = prompt(actions, prompt=selected_output['name'])

            if action == MOVE:
                run_move(outputs, selected_output)
            elif action == MODE:
                run_mode(selected_output)
            elif action == SHUTDOWN:
                run_shutdown(selected_output)
        elif selected_output_name in connected_unmapped_outputs:
            selected_output = connected_unmapped_outputs[selected_output_name]

            run_move(outputs, selected_output, is_auto=True)
        elif selected_output_name in outputs_to_cleanup:
            selected_output = outputs_to_cleanup[selected_output_name]
            run_shutdown(selected_output)

    except InvalidValue:
        pass


__main__()
