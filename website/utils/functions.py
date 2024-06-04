from flask import flash

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')


def is_truthy(string: str) -> bool:
    return string.lower() in ["tak", "t", "yes", "y", "1"]

def comments(self, userid):
        return Comment.query.filter_by(to=userid)