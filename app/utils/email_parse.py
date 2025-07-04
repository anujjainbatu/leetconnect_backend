import re

def parse_branch_year(email: str) -> tuple[str, str]:
    """
    Extract branch and year from email prefix, e.g.
    'alice.cs22@satiengg.in' → ('cs', '22').
    """
    local = email.split("@")[0]
    match = re.match(r"([a-zA-Z]+)(\d+)", local)
    if match:
        return match.groups()  # (branch, year)
    return ("", "")
