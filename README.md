# nyc-311-sla-analysis

Analysis of NYC 311 service requests to identify SLA breach patterns across agencies, complaint types, and boroughs

## Where the City Falls Behind

854,000 complaints. One question: does NYC actually resolve them on time, or does that depend entirely on who you call?

### The short version

I pulled almost a year's worth of NYC 311 service requests, built a proper data pipeline for it (Python to MySQL star schema to Power BI), and went looking for patterns in who's slow, who's fast, and why. What I found surprised me. My first guess about why the city was slow turned out to be wrong, and the real answer was more interesting.

**39.4%** of complaints with a known resolution time missed my SLA threshold (24+ hours). That's the headline number. Everything below explains what's actually driving it.

### What I expected vs. what I found

Going in, I assumed location would matter most, that certain boroughs get worse service than others. It's the obvious hypothesis, and it's the one I'd have bet on.

It's wrong. Or at least, it's not the main story.

Agency handling the complaint: 3% breach rate (NYPD) up to 98% (Dept. of Housing Preservation and Development).

Borough: 35% (Queens) up to 48.5% (Staten Island).

A 95 point gap by agency. A 13.5 point gap by borough. Whatever's slowing complaints down is baked into which department picks up the ticket, not where you live. That's a very different story than the one I went in expecting to tell, and I think it's the more useful one. It points at process and staffing, not geography.

### What's actually slow

Housing related complaints dominate the worst offenders: rodent sightings, indoor air quality, unsanitary conditions, all sitting near or at 100% SLA breach among complaint types with real volume (I filtered out anything under 1,000 total complaints so a single slow ticket couldn't fake a 100% rate).

NYPD handled complaints, by contrast, close out fast almost across the board.

### How I built this

Extraction: NYC 311 public API, 854,221 raw records.

Cleaning (Python/pandas): dropped impossible values (negative resolution times), discovered the official due_date field was 99.6% empty and unusable, so I derived my own resolution_hours metric instead. 853,689 clean rows.

Warehousing (MySQL): built a star schema, one fact table (fact_service_requests) plus four dimension tables (agency, complaint type, location, date), and validated the load (zero broken foreign keys, NULL patterns matched expected open complaint counts).

Analysis (SQL): breach rate queries broken out by agency, complaint type, and borough, with volume thresholds so tiny sample sizes couldn't distort the ranking.

Dashboard (Power BI): connected live to MySQL, DAX measures built from scratch, four visuals that put the agency vs borough contrast side by side.

### Repo structure

python/ : extraction and cleaning scripts

00_problem_statement.md.txt : the question I set out to answer

recommendations.md.txt : what I'd suggest the city actually do about this

README.md

### A note on the data

Real government data is messy in ways clean tutorials never show you. About 11,000 complaints in this dataset have a "still open" status but somehow also carry a closed date timestamp, a source system quirk, not something I could or should paper over. I flagged it rather than quietly fixing it, because pretending your data is cleaner than it is helps no one.

Built as a self directed project to practice the full analyst pipeline end to end. Not just querying clean data, but owning it from raw API pull to a dashboard someone else could actually read.
