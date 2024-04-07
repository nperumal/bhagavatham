import re

txt = "12-27     మృతియును జీవనంబు... (చంపకమాల)."
p = re.search(r"(\d+-\d+)\s+(.*)", txt)

print(p.group(2))
