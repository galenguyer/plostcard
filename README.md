# plostcard
a nightly cron job to summarize the last day of blaseball (or last week, on sundays), and send a letter to the specified recipient

plostcard will have three stages. the first will use python and jinja2 to get data from the blaseball api and fill out a latex template. stage two will compile the latex into a pdf. stage three will use clicksend to mail the pdf as a letter

## stage 1: data
endpoints:
 - [allTeams](https://www.blaseball.com/database/allTeams) for getting the most recent data for all teams including standings
 - [allDivisions](https://www.blaseball.com/database/allDivisions) for sorting teams into divisions
 - [feed/global](https://www.blaseball.com/database/feed/global?&limit=20&sort=3) to get the latest events from the feed
