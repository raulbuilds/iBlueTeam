
# iBlueTeam — Detection Coverage & Threat Visibility Platform

**MITRE ATT&CK-Based Detection Engineering, Coverage Analysis & Security Monitoring Prototype**

iBlueTeam is a full-stack cybersecurity platform designed to evaluate, visualize, and improve security detection coverage across the MITRE ATT&CK Enterprise framework.

Instead of assigning detection coverage manually, the platform calculates coverage from detection rule status, the latest test results, and log-source availability.

The project combines detection engineering workflows, ATT&CK technique mapping, risk-prioritized gap analysis, Sigma rule management, live event visualization, honeypot integration, and role-based rule review.

> **Project Status:** Functional local prototype developed for cybersecurity research, technical demonstrations, education, and portfolio purposes. Not production-hardened.

---

## Key Features

| Module | Capabilities |
|---|---|
| **Landing Page** | Animated entry interface, cybersecurity-themed visuals, and navigation to the main platform |
| **Overview Dashboard** | Detection coverage summaries, tactic-level statistics, rule status, test results, and log-source metrics |
| **Coverage Matrix** | MITRE ATT&CK tactics, techniques, sub-techniques, coverage states, interactive heatmap, filters, and risk-weighted coverage |
| **Detection Rules** | Rule creation, editing, testing, log-source associations, Sigma YAML imports, and CSV imports |
| **Rule Review Workflow** | Draft submissions, reviewer approval or rejection, and controlled rule activation |
| **Log Sources** | Telemetry collection status, required data sources, and detection visibility analysis |
| **Gap Analysis** | Detection gaps, telemetry blind spots, risk-prioritized findings, and CSV exports |
| **Live Monitor** | Interactive map displaying simulated security events and supported honeypot activity |
| **Honeypot Integration** | External sensor, connection-event collection, event classification, and ATT&CK technique mapping |
| **GeoIP & ASN Enrichment** | Optional IP geolocation, network provider information, and configurable lab-network locations |
| **Access Control** | Admin, Analyst, and Reviewer roles with separate permissions |
| **Data Export** | Coverage Matrix JSON/CSV, gap analysis CSV, and MITRE ATT&CK Navigator layer exports |
| **Multilingual Interface** | Azerbaijani and English interface support |

### Interactive Technique Analysis

Selecting an ATT&CK technique opens a detailed information panel containing:

- Technique descriptions and identifiers
- Associated detection rules
- Latest detection test results
- Required log sources
- Related sub-techniques
- Coverage status and relevant notes

This enables analysts to investigate why a technique is considered covered, partially covered, or missing detection capability.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python, FastAPI |
| **Database** | SQLite |
| **ORM** | SQLAlchemy |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Security Framework** | MITRE ATT&CK Enterprise |
| **Threat Intelligence Format** | STIX |
| **Detection Rules** | Sigma YAML, CSV |
| **API Architecture** | REST API |
| **Authentication** | Token-based authentication |
| **Network Monitoring** | Python-based honeypot sensor |
| **Geolocation** | GeoIP and ASN MMDB databases |

The frontend uses native HTML, CSS, and JavaScript without requiring React or a frontend build system.

---

## System Architecture

```text
                    USER / ANALYST
                          |
                          v
              +-----------------------+
              |     Web Interface     |
              |   HTML / CSS / JS     |
              +-----------------------+
                          |
                          v
              +-----------------------+
              |      FastAPI API      |
              +-----------------------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
   +-------------+ +-------------+ +-------------+
   |  Detection  | | Security    | | Honeypot    |
   |  Coverage   | | Monitoring  | | Integration |
   +-------------+ +-------------+ +-------------+
          |               |               |
          +---------------+---------------+
                          |
                          v
              +-----------------------+
              |   SQLAlchemy ORM      |
              +-----------------------+
                          |
                          v
              +-----------------------+
              |    SQLite Database    |
              +-----------------------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
      ATT&CK Data    Detection Rules   Security Events
```

The optional honeypot sensor runs as a separate component and sends supported events to the backend.

See [Architecture and Security](docs/architecture.md) for additional implementation details.

---

## Detection Coverage Methodology

Detection coverage is calculated dynamically using:

1. Detection rule availability and status
2. Latest detection test results
3. Required log-source availability
4. Associations between rules and ATT&CK techniques

### Coverage States

| State | Interpretation |
|---|---|
| **Full Coverage** | At least one enabled rule has a successful latest test and all required log sources are collected |
| **Partial Coverage** | A rule exists but is in draft, untested, has a failed latest test, or lacks specified log sources |
| **Coverage Gap** | No effective rule exists, a rule is disabled, or required telemetry is unavailable |
| **Blind Spot** | A detection gap specifically associated with missing telemetry |

### Risk-Prioritized Gap Analysis

The platform provides risk-weighted coverage metrics and prioritizes detection gaps to support security monitoring assessments.

This helps identify which techniques require additional rules, testing, or telemetry improvements.

Detailed methodology:
[Coverage Calculations](docs/coverage.md)

---

## Role-Based Access Control

iBlueTeam implements a three-role workflow for managing detection rules.

| Role | Responsibilities |
|---|---|
| **Admin** | Manage users and rules; approve or reject eligible pending rule reviews |
| **Analyst** | Create and edit draft rules; submit rules for review |
| **Reviewer** | Review submitted rules and approve or reject pending submissions |

### Detection Rule Review Workflow

```text
     Analyst Creates Rule
              |
              v
         Draft Status
              |
              v
       Submit for Review
              |
              v
        Pending Review
              |
       +------+------+
       |             |
       v             v
    Approved       Rejected
       |             |
       v             v
   Active Rule   Return to Draft
```

Rule submissions remain pending until an authorized reviewer makes a decision.

A user cannot approve their own submission.

See [Three-Role Review Workflow](docs/THREE_ROLE_REVIEW.md).

---

## Live Security Monitor

The Live Monitor provides a visual representation of security events through an interactive world map.

### Capabilities

- Simulated security event streams
- Event classification and visualization
- ATT&CK technique associations
- Detection coverage indicators
- Map-based event monitoring
- Honeypot event display when a sensor is configured

**Important:** Simulated events are demonstration data and must not be interpreted as actual detected attacks.

---

## Honeypot Sensor Integration

iBlueTeam includes an optional Python-based honeypot sensor that can be deployed separately in a controlled environment.

### Capabilities

- Inbound connection-event collection
- Sensor-to-backend event reporting
- API-key authenticated ingestion
- Event categorization
- Heuristic MITRE ATT&CK mapping
- Event visualization in the platform
- Test traffic simulation

The honeypot can provide real network observations when correctly deployed and connected.

A connection or scan does not automatically prove malicious intent.

**Security Notice:** Deploy the sensor only in an isolated or appropriately controlled lab environment. Protect API keys and restrict network access.

Setup documentation:
[Honeypot Setup](docs/honeypot.md)

---

## GeoIP & ASN Enrichment

Supported honeypot events can be enriched using optional local geolocation databases.

Available enrichment fields include:

- Country and city
- Geographic coordinates
- Autonomous System Number (ASN)
- Network organization
- Location data source

### Optional Setup

Obtain compatible City and ASN MMDB databases from an authorized provider.

Place supported database files in the project's `data/` directory according to the setup guide.

These databases are not included in the repository.

Private laboratory networks can use locally configured display locations.

For configuration instructions, see:

- [GeoIP and ASN Setup](docs/geoip-asn-setup.md)
- [Lab Network Configuration](data/LAB_LOCATIONS_SETUP.md)

IP geolocation is approximate and does not establish the physical location or identity of an attacker.

---

## Getting Started

### Requirements

- Python 3
- pip
- Git
- Internet access for the initial full ATT&CK dataset download

### 1. Clone the Repository

```bash
git clone https://github.com/r4ul70/iBlueTeam.git
cd iBlueTeam
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -m venv .venv
```

**Linux / macOS:**

```bash
python3 -m venv .venv
```

### 3. Install Dependencies

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Linux / macOS:**

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 4. Configure the Administrator Password

For security, use your own strong password.

**Windows PowerShell:**

```powershell
$env:IBT_ADMIN_PASSWORD = "replace-with-your-strong-password"
```

**Linux / macOS:**

```bash
export IBT_ADMIN_PASSWORD="replace-with-your-strong-password"
```

Do not reuse this example value as an actual password.

### 5. Start the Application

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe run.py
```

**Linux / macOS:**

```bash
python run.py
```

Open the application:

http://127.0.0.1:8000

**Initial administrator username:** `admin`

Use the administrator password configured above.

If no administrator password is provided during initial account creation, the application generates a random password and prints it once in the terminal.

**Interactive API Documentation:**

http://127.0.0.1:8000/docs

---

## MITRE ATT&CK Dataset Setup

The full `enterprise-attack.json` dataset is intentionally excluded from this repository because of its size.

### Automatic Download

On startup, iBlueTeam attempts to download the official MITRE ATT&CK Enterprise STIX dataset and import the data into the local SQLite database.

An internet connection is required for the automatic download.

If the download fails, the application can use a limited built-in fallback dataset.

### Manual Installation

1. Download the official Enterprise ATT&CK dataset:

[MITRE ATT&CK Enterprise STIX JSON](https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json)

2. Save the downloaded file to:

```text
data/enterprise-attack.json
```

3. Reimport the dataset:

```bash
python run.py --reimport-attack
```

The dataset is excluded through `.gitignore` and should not be committed to this repository.

Official source:
[MITRE CTI GitHub Repository](https://github.com/mitre/cti)

---

## Runtime Configuration

The application supports several command-line options.

| Option | Description |
|---|---|
| `--port 9000` | Run the application on a custom port |
| `--lan` | Allow access from other devices on a local network |
| `--no-sample` | Start without loading sample detection rules |
| `--reimport-attack` | Reimport the ATT&CK dataset |
| `--reload` | Enable development auto-reload |

Example:

```bash
python run.py --port 9000
```

### Environment Variables

| Variable | Purpose |
|---|---|
| `IBT_ADMIN_PASSWORD` | Initial administrator password |
| `IBT_SECRET` | Authentication token signing secret |
| `IBT_TARGET_NAME` | Protected network display name |
| `IBT_TARGET_LAT` | Protected network display latitude |
| `IBT_TARGET_LON` | Protected network display longitude |

Do not store real passwords or token secrets directly in source code.

The `--lan` option should only be used on trusted networks.

---

## Repository Structure

```text
iBlueTeam/
|
+-- backend/
|   +-- main.py
|   +-- models.py
|   +-- auth.py
|   +-- coverage.py
|   +-- attack_import.py
|   +-- monitor.py
|   +-- honeypot.py
|   +-- geo.py
|   +-- sigma.py
|   +-- database.py
|   +-- ...
|
+-- frontend/
|   +-- index.html
|   +-- dashboard.html
|   +-- css/
|   +-- js/
|
+-- honeypot/
|   +-- honeypot.py
|   +-- sim_client.py
|
+-- data/
|   +-- sample_rules/
|   +-- lab-locations.example.json
|   +-- LAB_LOCATIONS_SETUP.md
|
+-- docs/
|   +-- architecture.md
|   +-- coverage.md
|   +-- data-model.md
|   +-- honeypot.md
|   +-- geoip-asn-setup.md
|   +-- THREE_ROLE_REVIEW.md
|   +-- demo.md
|
+-- run.py
+-- requirements.txt
+-- .gitignore
+-- README.md
```

Runtime databases, private configuration, and other sensitive local files should remain outside version control.

---

## Data Export

iBlueTeam supports exporting security assessment results for further analysis.

Available formats include:

- Coverage Matrix JSON
- Coverage Matrix CSV
- Detection Gap CSV
- MITRE ATT&CK Navigator layer

These exports can support reporting, visualization, and additional security assessment workflows.

---

## Documentation

Additional technical documentation is available in the repository:

- [Architecture and Security](docs/architecture.md)
- [Data Model and API](docs/data-model.md)
- [Coverage Methodology](docs/coverage.md)
- [Honeypot Setup](docs/honeypot.md)
- [GeoIP & ASN Configuration](docs/geoip-asn-setup.md)
- [Rule Review and RBAC](docs/THREE_ROLE_REVIEW.md)
- [Lab Network Configuration](data/LAB_LOCATIONS_SETUP.md)
- [Demo Scenarios](docs/demo.md)

---

## Security Considerations

This project is intended for controlled environments, education, research, and technical demonstrations.

Important considerations:

- Do not expose administrator credentials or API keys.
- Do not commit runtime databases or secret files.
- Use an isolated environment for honeypot deployment.
- Restrict network access when enabling LAN mode.
- Treat geolocation information as approximate.
- Do not assume every observed connection represents an attack.
- Review authentication, authorization, and deployment security before any public-facing use.

The project has not undergone an independent production security audit.

---

## Current Limitations

- No direct SIEM integration is included in this version.
- The default Live Monitor uses synthetic events.
- Real honeypot observations require a separately deployed sensor.
- Detection rules are managed and evaluated through stored metadata and test records; they are not automatically executed against live SIEM telemetry.
- Technique-level coverage may not fully distinguish platform-specific detection scenarios.
- SQLite is intended for lightweight local deployments rather than large-scale concurrent workloads.
- GeoIP and ASN enrichment require optional external database files.
- The application is a functional prototype, not a production-ready security monitoring service.

---

## Future Development

Potential improvements include:

- SIEM integration with platforms such as Wazuh
- Automated log-source and telemetry ingestion
- Expanded detection rule validation
- Platform-specific coverage evaluation
- Additional security analytics
- Broader testing and deployment hardening
- Production-oriented infrastructure improvements

These items represent possible future work and are not claimed as completed functionality.

---

## Project Scope

iBlueTeam demonstrates practical experience in:

- Cybersecurity and blue-team workflows
- Detection engineering concepts
- MITRE ATT&CK mapping
- Python backend development
- FastAPI REST API design
- SQLAlchemy database modeling
- Frontend web development
- Rule-based security analysis
- Network event collection and simulation
- Security data visualization
- Role-based authorization workflows
- Technical documentation and system architecture

The project was developed as an independent technical portfolio initiative to explore how detection engineering, telemetry availability, and security monitoring concepts can be combined within a unified web platform.

---

## Disclaimer

This repository is intended for educational, research, and portfolio use.

MITRE ATT&CK is maintained by The MITRE Corporation. This independent project is not affiliated with or endorsed by MITRE.
