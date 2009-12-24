# This file is necessary to make this directory a package.

def cleanupHTML(html):
    lines = []
    for line in html.split("\n"):
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)
