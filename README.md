# DorkRecon

**Google Dorking Tool for Web Application Penetration Testing**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

## Overview

DorkRecon is a lightweight Python-based passive reconnaissance tool designed for web application penetration testing, VAPT, and authorized security assessments.

It eliminates the repetitive process of manually writing Google Dork queries by automatically generating categorized search queries for a specified target domain.

The tool focuses exclusively on Google Dorking, keeping reconnaissance simple, efficient, and organized.

## Features

- Clean and interactive command-line interface.
- Automatic domain validation.
- 40 curated Google Dorks across 10 categories.
- Automatic query generation and duplicate removal.
- Browser and terminal execution modes.
- Automated HTML report generation.
- Automatic HTML report opening after execution.
- Searchable reports with category filters.
- Clickable Google search URLs.
- No external Python dependencies.
- No API key required.
- No root privileges required.

## Reconnaissance Coverage

| Category | Queries |
|---|---:|
| Indexed Documents | 5 |
| Configuration References | 3 |
| Administration Interfaces | 3 |
| API Discovery | 6 |
| Authentication Pages | 5 |
| Directory Indexing | 2 |
| Application Error Disclosure | 6 |
| Development and Testing References | 4 |
| JavaScript Discovery | 2 |
| Legacy Application Discovery | 4 |
| **Total** | **40** |

## Requirements

- Python 3.x
- Linux or Kali Linux
- Internet connection
- Web browser

No additional Python packages are required.

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/DorkRecon.git
cd DorkRecon
chmod +x dorkrecon.py
```

## Usage

```bash
python3 dorkrecon.py
```

Enter the authorized target domain and select an execution mode.

```text
=================================================
                  DORKRECON
       Google Dorking for Web Pentesting
            Passive Reconnaissance
=================================================

[+] Loaded Categories : 10
[+] Loaded Dorks      : 40

[+] Enter target domain: example.com

=================================================
SELECT EXECUTION MODE
=================================================

[1] Browser + HTML Report
[2] Terminal + HTML Report

DorkRecon >>
```

## Execution Modes

### 1. Browser Mode

- Opens Google searches in the default browser.
- Executes searches in controlled batches.
- Generates an HTML reconnaissance report.
- Automatically opens the generated report.

### 2. Terminal Mode

- Displays categorized Google Dorks in the terminal.
- Displays corresponding Google search URLs.
- Generates an HTML reconnaissance report.
- Automatically opens the generated report.

## HTML Report

DorkRecon generates an interactive, self-contained HTML report containing:

- Target domain
- Assessment timestamp
- Total generated queries
- Reconnaissance categories
- Google Dork queries
- Clickable search links
- Execution status
- Search and category filters

Reports are automatically saved in:

```text
~/DorkRecon-Reports/
```

## Project Structure

```text
DorkRecon/
├── dorkrecon.py
└── README.md
```

## Limitations

- Search results depend on Google's indexing.
- The tool currently generates search queries rather than automatically extracting search results.
- HTML reports contain generated queries and execution status, not verified vulnerabilities.
- Identified resources require manual security validation.


## Disclaimer

DorkRecon is developed for educational purposes, authorized penetration testing, passive reconnaissance, and defensive security assessments.

Use this tool only against domains you own or have explicit permission to assess.

Users are responsible for complying with applicable laws and search engine terms of service. The developer is not responsible for unauthorized or illegal use of this tool.

## Contributions

Contributions, feature suggestions, bug reports, and improvements are welcome through GitHub Issues and Pull Requests.

## Project Status

Actively under development.

---

**DorkRecon — Automate the queries. Simplify reconnaissance.**
