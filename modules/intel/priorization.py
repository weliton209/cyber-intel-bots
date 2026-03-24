def is_target_related(text, targets):

    if not text:
        return False

    text = text.lower()

    for t in targets:
        if t.lower() in text:
            return True

    return False
