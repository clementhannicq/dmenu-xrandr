import dmenu


class InvalidValue(Exception):
    pass


def prompt(entries, unless_stupid=True, allow_unknown_values=False, **kwargs):
    """
    Prompts the end user to make a choice
    @param entries: Iterable of choices to select from
    @param unless_stupid: If True and allow_unknown_values is False, do not prompt the user if there is only one choice
    @param allow_unknown_values: If False, it will raise InvalidValue if the user inputs a value not in the entities iterable
    @param kwargs: Other named arguments to be forwarded to dmenu
    @return: The selected value
    @raise InvalidValue: If allow_unknown_values is False and a value not in the entities was entered
    """
    if unless_stupid and not allow_unknown_values and len(entries) == 1:
        return entries[0]
    value = dmenu.show(entries, bottom=True, fast=True, case_insensitive=True, **kwargs)
    if not allow_unknown_values and value not in entries:
        raise InvalidValue(value)
    return value
