def input_val(unvalidated):
    validated = ''.join(e for e in unvalidated if e.isalnum())
    return validated