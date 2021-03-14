import subprocess

### Update README

helptext = subprocess.run(["ih", "--help"], capture_output=True)

readme = "README.md"
with open(readme) as f:
    lines = f.read().split("\n")

newfile = []
copy = True
for line in lines: 
    if "END_USAGE" in line:
        copy = True
        newfile += helptext.stdout.decode('utf-8').split("\n")
        newfile.append("```")
    if copy:
        newfile.append(line)
    if "START_USAGE" in line:
        copy = False
        newfile.append("```")

with open(readme, 'w') as f:
    f.write("\n".join(newfile))

