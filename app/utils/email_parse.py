import re

def parse_branch_year(email: str) -> tuple[str, int]:
    """
    From an address like 'suryansh26it064@satiengg.in' we want:
      - year  = 2026   (i.e. prefix '20' to the two‑digit '26')
      - branch = 'IT'  (uppercase letters that follow the year)
    """
    local = email.split('@')[0]  
    # Look for:  two digits, then letters, then any digits
    m = re.match(r".*?(\d{2})([A-Za-z]+)\d*$", local)
    if m:
        yy     = m.group(1)        # "26"
        branch = m.group(2).upper()# "IT"
        year   = 2000 + int(yy)    # 2026
        return branch, year

    # Fallback if we can’t parse
    return "", 0
