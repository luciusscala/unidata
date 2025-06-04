# NCAA School Athletics Website Scraper & Verifier

## Project Overview

This project’s purpose is to create a comprehensive, structured database of every NCAA school in the United States, paired with its official athletics website. This is a nuanced, nontrivial challenge because athletics websites are frequently hosted on different domains than the schools' main `.edu` domains and are not predictably structured.

The final deliverables enable:
- **Programmatic verification** of student identities against official athletics rosters.
- Simple integration into registration flows (see FastAPI and Supabase demo).
- Reproducible data scraping and a strategy for keeping datasets up-to-date.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Workflow & Data Flow](#workflow--data-flow)
3. [File & Directory Descriptions](#file--directory-descriptions)
4. [API & Demo Frontend](#api--demo-frontend)
5. [Notes & Future Improvements](#notes--future-improvements)

---

## Project Structure

```
unidata/
├── scripts/
│   ├── athletics.py
│   ├── directory.py
│   ├── path.py
│   ├── schools.py
│   └── test.py
├── schools.json
├── output.sql
├── database.db
├── check.py
├── package.json
├── package-lock.json
├── index.html
├── plan.txt
├── .gitignore
└── README.md
```

---

## Workflow & Data Flow

The process of building the NCAA school and athletics website database is as follows:

1. **Initial Data Ingestion**
   - Begin with `schools.json` (a JSON list of raw school data, likely from an external dump/API).
   - Use `scripts/schools.py` to import this data into an SQLite table named `universities`.

2. **Enrich with NCAA Directory Routes**
   - Run `scripts/path.py` to scrape each school's NCAA.com listing, extracting a "route" (a partial URL to the school's NCAA details or athletics info), and update this value in `universities`.

3. **(Optionally) Gather Further Details**
   - `scripts/athletics.py` can be used next (after fixing DB table alignment; see notes) to visit each NCAA.com listing, extract the official athletics website, and persist this info.

4. **Alternative Brute-Force Scraping**
   - `scripts/directory.py` implements a wide, ID-based scrape of the NCAA's institutional directory. It gathers pairs of general and athletics websites for thousands of schools, saved into a separate table `new`.

5. **Validation, API, and Demo**
   - The data—most importantly, pairs of school domains and athletics website URLs—is now ready for external consumption:
     - Via SQLite DB (`database.db` or export as `output.sql`)
     - With a FastAPI endpoint in `check.py`
     - Using a minimal, live demo frontend (`index.html`)

---

## File & Directory Descriptions

### scripts/
- **athletics.py**  
  Scrapes each school's NCAA listing (from the `route` in `universities` or `schools`), finds the official athletics website URL, and updates the DB. _Note: Expects a table `schools`—rename or adjust for production._
  
- **directory.py**  
  Iteratively scrapes thousands of potential NCAA institution pages, finds general and athletics domains, and stores paired results in a `new` table. Includes helpers for cleaning domains/URLs.

- **path.py**  
  Scrapes NCAA.com schools indices to retrieve the URL path (`route`) for each school. Adds the route to the correct school row in the `universities` table.

- **schools.py**  
  Loads data from `schools.json` and adds it to the `universities` table in the SQLite DB.

- **test.py**  
  A sandbox script to try scraping individual roster pages. Not part of the production flow.

---

### Root Files

- **schools.json**  
  The input JSON for initial school data (name, domains). This is the foundational dataset used by `schools.py`.

- **database.db**  
  The active SQLite database, aggregating the scraped/processed results as the scripts run.

- **output.sql**  
  The SQL-dump (CREATE and INSERT statements) for easy export/import of the core dataset. Table `school_data` generally follows (website TEXT, domain TEXT).

- **check.py**  
  A FastAPI app providing a `/verify` endpoint for external systems to:
    - Submit an email (domain) and full name.
    - Locate the corresponding athletics website.
    - Scrape the men’s soccer roster page for the provided name.
    - Return JSON verification status.

- **index.html**  
  A demonstration frontend:
    - Sign up with email/password using Supabase Auth.
    - Verify a name against the school’s roster using the FastAPI `/verify` endpoint.
    - Results shown in the browser.

- **plan.txt**  
  A basic note on directions for API + Auth0 integration for future registration—_not currently implemented_.

- **package.json / package-lock.json**  
  Present from NPM ecosystem, possibly for package tracking or future extensions.

---

## API & Demo Frontend

### FastAPI Service (`check.py`)
- POST `/verify`
  - Input: JSON with `email` and `name`.
  - Action: Finds the school by email domain, appends `/sports/mens-soccer/roster` to its site, pulls the page and checks for name match.
  - Output: `{ "status": "valid" }` or `{ "status": "invalid" }`

### Frontend (`index.html`)
- Users sign up (Supabase Auth).
- Prompted to input a full name—calls the verify API.
- Result (verified / failed) is shown in the page.

---

## Notes & Future Improvements

- **Database Structure**: For full productionization, harmonize the different scripts to use a single table/schema for all scraped data. Multiple tables (`universities`, `new`, `schools`) and outputs (`database.db`, `output.sql`) reflect incremental dev and experimentation.
- **Extensibility**: Easily add further sports, expand roster formats, or extend to other divisions by modifying API/search logic.
- **Authentication**: See `plan.txt`—future roadmap includes robust Auth0/API integration for registration validation.
- **Organization**: For clarity, consider moving all scraped data (`*.db`, `*.sql`, `schools.json`) to a `/data` or `/output` folder in future refactors.

---

## Attribution & Disclaimer

This project is for educational and research purposes, demonstrating end-to-end data gathering and validation workflows relevant to the NCAA. Site scraping respects target site TOS and should be done responsibly and sparingly to avoid undue load.

---

## Contact

For inquiries or improvements, open an issue or reach out to the maintainer.