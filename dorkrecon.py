
#!/usr/bin/env python3

import os
import re
import html
import time
import webbrowser

from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode, urlsplit

# ==========================================
# TERMINAL COLORS
# ==========================================

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
WHITE = "\033[97m"
RESET = "\033[0m"

# ==========================================
# GOOGLE DORK DATABASE
# ==========================================

DORKS = {

    "Indexed Documents": [
        "filetype:pdf",
        "filetype:xls",
        "filetype:xlsx",
        "filetype:doc",
        "filetype:docx"
    ],

    "Configuration References": [
        "inurl:config",
        '"configuration guide"',
        '"application settings"'
    ],

    "Administration Interfaces": [
        "inurl:admin",
        "inurl:administrator",
        'intitle:"Admin Portal"'
    ],

    "API Discovery": [
        "inurl:api",
        "inurl:swagger",
        "inurl:graphql",
        "inurl:openapi",
        "inurl:api-docs",
        "filetype:wsdl"
    ],

    "Authentication Pages": [
        "inurl:login",
        "inurl:signin",
        "inurl:register",
        "inurl:sso",
        "inurl:oauth"
    ],

    "Directory Indexing": [
        'intitle:"Index of"',
        'intitle:"Directory Listing"'
    ],

    "Application Error Disclosure": [
        'intext:"SQL syntax"',
        'intext:"Stack Trace"',
        'intext:"Unhandled Exception"',
        'intext:"Fatal Error"',
        'intext:"Internal Server Error"',
        '(intext:"error" OR intext:"warning")'
    ],

    "Development and Testing References": [
        '"development environment"',
        '"staging environment"',
        '"test environment"',
        '"sandbox environment"'
    ],

    "JavaScript Discovery": [
        "filetype:js",
        "inurl:assets filetype:js"
    ],

    "Legacy Application Discovery": [
        "ext:php",
        "ext:asp",
        "ext:aspx",
        "ext:jsp"
    ]
}

# ==========================================
# BANNER
# ==========================================

def banner():

    os.system("clear")

    print(CYAN + r"""
 ____             _    ____
|  _ \  ___  _ __| | _|  _ \ ___  ___ ___  _ __
| | | |/ _ \| '__| |/ / |_) / _ \/ __/ _ \| '_ \
| |_| | (_) | |  |   <|  _ <  __/ (_| (_) | | |
|____/ \___/|_|  |_|\_\_| \_\___|\___\___/|_| |_|
    """ + RESET)

    print(CYAN + "=" * 65 + RESET)
    print("          GOOGLE DORKING FOR WEB PENTESTING")
    print("              Passive Reconnaissance")
    print(CYAN + "=" * 65 + RESET)

    print(
        f"{GREEN}[+] Loaded Categories : "
        f"{len(DORKS)}{RESET}"
    )

    print(
        f"{GREEN}[+] Loaded Dorks      : "
        f"{sum(len(x) for x in DORKS.values())}{RESET}"
    )

# ==========================================
# DOMAIN INPUT AND VALIDATION
# ==========================================

def get_domain():

    while True:

        value = input(
            f"\n{GREEN}[+] Enter target domain: {RESET}"
        ).strip().lower()

        if "://" not in value:
            value = "https://" + value

        try:
            domain = urlsplit(value).hostname or ""
        except ValueError:
            domain = ""

        pattern = (
            r"(?:[a-z0-9](?:[a-z0-9-]{0,61}"
            r"[a-z0-9])?\.)+[a-z]{2,63}"
        )

        if len(domain) <= 253 and re.fullmatch(pattern, domain):
            return domain

        print(f"{RED}[-] Invalid domain. Try again.{RESET}")

# ==========================================
# GENERATE GOOGLE DORKS
# ==========================================

def generate_dorks(domain):

    results = []
    seen = set()

    for category, queries in DORKS.items():

        for dork in queries:

            query = f"site:{domain} {dork}"

            if query in seen:
                continue

            seen.add(query)

            url = (
                "https://www.google.com/search?"
                + urlencode({"q": query})
            )

            results.append({
                "id": len(results) + 1,
                "category": category,
                "query": query,
                "url": url,
                "status": "Pending review"
            })

    return results

# ==========================================
# EXECUTION MENU
# ==========================================

def select_mode():

    print(f"\n{CYAN}{'=' * 65}{RESET}")
    print(f"{YELLOW}SELECT EXECUTION MODE{RESET}")
    print(f"{CYAN}{'=' * 65}{RESET}")

    print("[1] Browser + HTML Report")
    print("[2] Terminal + HTML Report")

    while True:

        choice = input(
            f"\n{GREEN}DorkRecon >> {RESET}"
        ).strip()

        if choice in ("1", "2"):
            return choice

        print(f"{RED}[-] Select 1 or 2.{RESET}")

# ==========================================
# TERMINAL MODE
# ==========================================

def terminal_mode(results):

    current_category = None

    for item in results:

        if current_category != item["category"]:

            current_category = item["category"]

            print(f"\n{CYAN}{'=' * 65}{RESET}")
            print(f"{YELLOW}[*] {current_category}{RESET}")
            print(f"{CYAN}{'=' * 65}{RESET}")

        print(
            f"{GREEN}[{item['id']:03}] "
            f"{item['query']}{RESET}"
        )

        print(f"{BLUE}      {item['url']}{RESET}")

    print(
        f"\n{GREEN}[+] Generated queries: "
        f"{len(results)}{RESET}"
    )

# ==========================================
# BROWSER MODE
# ==========================================

def browser_mode(results):

    print(f"\n{YELLOW}[*] Browser mode selected.{RESET}")
    print("[*] Opening Google searches in batches of five.")

    opened = 0
    total = len(results)

    for index, item in enumerate(results, 1):

        print(
            f"{GREEN}[{index:02}/{total:02}] "
            f"{item['query']}{RESET}"
        )

        try:

            if webbrowser.open_new_tab(item["url"]):

                item["status"] = "Browser opened - review pending"
                opened += 1

            else:
                item["status"] = "Browser failed"

        except Exception:
            item["status"] = "Browser failed"

        if index < total:
            time.sleep(2)

        if index % 5 == 0 and index < total:

            choice = input(
                f"\n{YELLOW}Open next five searches? "
                f"[Y/n]: {RESET}"
            ).strip().lower()

            if choice == "n":
                break

    print(
        f"\n{GREEN}[+] Browser searches opened: "
        f"{opened}/{total}{RESET}"
    )

# ==========================================
# HTML REPORT GENERATOR
# ==========================================

def generate_report(domain, results, mode):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_directory = Path.home() / "DorkRecon-Reports"

    report_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = (
        report_directory
        / f"{domain}_{timestamp}.html"
    )

    rows = []

    for item in results:

        category = html.escape(item["category"])
        query = html.escape(item["query"])
        url = html.escape(item["url"], quote=True)
        status = html.escape(item["status"])

        rows.append(f"""
        <tr>
            <td>{item['id']:03}</td>
            <td>{category}</td>
            <td><code>{query}</code></td>
            <td>
                <a href="{url}"
                   target="_blank"
                   rel="noopener noreferrer">
                    Search Google
                </a>
            </td>
            <td>{status}</td>
        </tr>
        """)

    table_rows = "\n".join(rows)

    category_options = "\n".join(
        f'<option value="{html.escape(name)}">'
        f'{html.escape(name)}</option>'
        for name in DORKS
    )

    report = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>DorkRecon | {html.escape(domain)}</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    background: #0d1117;
    color: #e6edf3;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 30px;
}}

.container {{
    max-width: 1500px;
    margin: auto;
}}

h1 {{
    color: #58a6ff;
    margin-bottom: 5px;
}}

.subtitle {{
    color: #8b949e;
}}

.summary {{
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 25px 0;
}}

.card {{
    background: #161b22;
    border: 1px solid #30363d;
    padding: 20px;
    border-radius: 8px;
    flex: 1;
    min-width: 180px;
}}

.number {{
    font-size: 30px;
    color: #3fb950;
    font-weight: bold;
    margin-top: 10px;
}}

.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 20px 0;
}}

input, select {{
    background: #161b22;
    border: 1px solid #30363d;
    color: #e6edf3;
    padding: 12px;
    border-radius: 6px;
    flex: 1;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    border: 1px solid #30363d;
    padding: 13px;
    text-align: left;
}}

th {{
    background: #161b22;
    color: #58a6ff;
}}

tr:hover {{
    background: #21262d;
}}

code {{
    color: #7ee787;
    overflow-wrap: anywhere;
}}

a {{
    color: #58a6ff;
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

.notice {{
    color: #d29922;
    padding: 15px 0;
}}

footer {{
    color: #8b949e;
    margin-top: 30px;
    text-align: center;
}}

</style>

</head>

<body>

<div class="container">

<h1>DorkRecon Security Report</h1>

<p class="subtitle">
    Passive Web Application Reconnaissance
</p>

<div class="summary">

    <div class="card">
        Target Domain
        <h3>{html.escape(domain)}</h3>
    </div>

    <div class="card">
        Total Google Dorks
        <div class="number">{len(results)}</div>
    </div>

    <div class="card">
        Categories
        <div class="number">{len(DORKS)}</div>
    </div>

    <div class="card">
        Execution Mode
        <h3>{html.escape(mode)}</h3>
    </div>

</div>

<p>Generated: {timestamp}</p>

<p class="notice">
    Search results require manual review.
    No vulnerabilities have been verified.
</p>

<div class="controls">

    <input type="text"
           id="searchBox"
           placeholder="Search Google Dorks..."
           oninput="filterTable()">

    <select id="categoryFilter"
            onchange="filterTable()">

        <option value="">All Categories</option>

        {category_options}

    </select>

</div>

<table id="dorkTable">

<thead>

<tr>
    <th>ID</th>
    <th>Category</th>
    <th>Google Dork</th>
    <th>Search</th>
    <th>Status</th>
</tr>

</thead>

<tbody>

{table_rows}

</tbody>

</table>

<footer>
    DorkRecon | Web Application Security Assessment
</footer>

</div>

<script>

function filterTable() {{

    const search = document.getElementById(
        "searchBox"
    ).value.toLowerCase();

    const category = document.getElementById(
        "categoryFilter"
    ).value;

    const rows = document.querySelectorAll(
        "#dorkTable tbody tr"
    );

    rows.forEach(row => {{

        const matchesSearch =
            row.textContent.toLowerCase().includes(search);

        const matchesCategory =
            !category ||
            row.cells[1].textContent.trim() === category;

        row.style.display =
            matchesSearch && matchesCategory ? "" : "none";

    }});

}}

</script>

</body>
</html>
"""

    report_file.write_text(
        report,
        encoding="utf-8"
    )

    return report_file

# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    banner()

    domain = get_domain()
    results = generate_dorks(domain)

    print(f"\n{GREEN}[+] Target  : {domain}{RESET}")
    print(f"{GREEN}[+] Queries : {len(results)}{RESET}")

    mode = select_mode()

    if mode == "1":

        mode_name = "Browser"

        try:
            browser_mode(results)
        except KeyboardInterrupt:
            print("\n[!] Browser execution stopped.")

    else:

        mode_name = "Terminal"
        terminal_mode(results)

    report = generate_report(
        domain,
        results,
        mode_name
    )

    print(f"\n{CYAN}{'=' * 65}{RESET}")
    print(f"{GREEN}[+] RECONNAISSANCE COMPLETED{RESET}")
    print(f"{CYAN}{'=' * 65}{RESET}")

    print(f"[+] Target     : {domain}")
    print(f"[+] Categories : {len(DORKS)}")
    print(f"[+] Queries    : {len(results)}")
    print(f"[+] Mode       : {mode_name}")
    print(f"[+] Report     : {report}")

    webbrowser.open_new_tab(report.resolve().as_uri())

    print(f"{CYAN}{'=' * 65}{RESET}")


if __name__ == "__main__":

    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print("\n[!] DorkRecon stopped.")
