import requests
import json
from string import Template

headers = {"User-Agent": "plostcards (chef#1911)"}
valid_divisions = [
    "d4cc18de-a136-4271-84f1-32516be91a80",  # Wild High
    "456089f0-f338-4620-a014-9540868789c9",  # Mild High
    "98c92da4-0ea7-43be-bd75-c6150e184326",  # Wild Low
    "fadc9684-45b3-47a6-b647-3be3f0735a84",  # Mild Low
]

print("GET https://blaseball.com/database/simulationData")
simData = requests.get(
    "https://blaseball.com/database/simulationData", headers=headers
).json()
# MOCK: simData = {"season": 22}

print("GET https://www.blaseball.com/database/season?number=" + str(simData["season"]))
seasonData = requests.get(
    "https://www.blaseball.com/database/season?number=" + str(simData["season"]),
    headers=headers,
).json()

print("GET https://www.blaseball.com/database/standings?id=" + seasonData["standings"])
standingsData = requests.get(
    "https://www.blaseball.com/database/standings?id=" + seasonData["standings"],
    headers=headers,
).json()

print("GET https://www.blaseball.com/database/allTeams")
allTeamsData = requests.get(
    "https://www.blaseball.com/database/allTeams", headers=headers
).json()

print("GET https://www.blaseball.com/database/allDivisions")
divisionsData = requests.get(
    "https://www.blaseball.com/database/allDivisions", headers=headers
).json()

print("GET https://www.blaseball.com/database/feed/global?&limit=20&sort=3")
feedData = requests.get(
    "https://www.blaseball.com/database/feed/global?&limit=20&sort=3", headers=headers
).json()

teams = []
for t in allTeamsData:
    team = {}
    team["id"] = t["id"]
    team["location"] = t["location"]
    team["nickname"] = t["nickname"]
    team["fullName"] = t["fullName"]
    team["losses"] = (
        standingsData["losses"][t["id"]] if t["id"] in standingsData["losses"] else 0
    )
    team["wins"] = (
        standingsData["wins"][t["id"]] if t["id"] in standingsData["wins"] else 0
    )
    team["gamesPlayed"] = (
        standingsData["gamesPlayed"][t["id"]]
        if t["id"] in standingsData["gamesPlayed"]
        else 0
    )
    team["emoji"] = t["emoji"]
    teams.append(team)

print(json.dumps(teams, indent=2))

divisions = []
for d_id in valid_divisions:
    d = [div for div in divisionsData if div["id"] == d_id][0]
    division = {}
    division["name"] = d["name"]
    division["id"] = d["id"]
    division["teams"] = [t for t in teams if t["id"] in d["teams"]]
    division["teams"].sort(key=lambda x: x["wins"], reverse=True)
    divisions.append(division)

print(json.dumps(divisions, indent=2))

latex_division = Template("        \\multicolumn{2}{ c }{\\large{$name}} \\\\\n")
latex_standing = Template("        $name & $wins ($games)\\\\\n")
standings = ""
for division in divisions:
    standings += "    \\begin{tabular}{ l c }\n"
    standings += latex_division.substitute(name=division["name"])
    for team in division["teams"]:
        standings += latex_standing.substitute(
            name=team["fullName"],
            wins=team["wins"],
            games=f"{team['gamesPlayed']-team['losses']}-{team['losses']}",
        )
    standings += "    \\end{tabular}\n"
    standings += "    \\vspace{8px}\n"

latex_feed = Template("    S$season-$day & $description\\\\")
feed = ""
for f in feedData:
    feed += latex_feed.substitute(season=f["season"]+1, day=f["day"]+1, description=f["description"]) + "\n"
    
with open("template.tex", "r") as fd:
    template = fd.read()
    with open("daily.tex", "w") as wd:
        wd.write(Template(template).substitute(standings=standings, feed=feed))
