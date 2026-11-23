
# iBlueTeam — Detection Coverage & Threat Visibility

**iBlueTeam** is a cybersecurity portfolio project for assessing detection coverage against the MITRE ATT&CK Enterprise framework. Rather than assigning coverage manually, it derives coverage states from detection-rule status, test results, and log-source availability.

The project combines a detection coverage matrix, risk-prioritized gap analysis, Sigma rule management, a simulated live monitor, and a separately deployable honeypot sensor. It is a **local prototype for demonstration and learning**, not a production-ready SIEM or intrusion-prevention system.

## Technology stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** HTML, CSS, vanilla JavaScript (no frontend build step)
- **Security data:** MITRE ATT&CK Enterprise STIX, sample detection rules and test records
- **Rule formats:** Sigma YAML and CSV

## Main features

| Module | Capabilities |
|---|---|
| Coverage Matrix | ATT&CK tactics, techniques and sub-techniques; coverage states; heatmap; filters; tactic-level and overall metrics; risk-weighted coverage |
| Overview | Coverage summaries and statistics for rules, tests and log sources |
| Detection Rules | Create, edit and remove rules; associate log sources; record tests; import Sigma YAML and CSV |
| Log Sources | Track telemetry availability and identify missing sources |
| Gap Analysis | Prioritize coverage gaps, review contributing factors and export CSV |
| Live Monitor | Visualize simulated security events and, when configured, honeypot events |
| Honeypot | Separate sensor for recording inbound connection activity and mapping events to ATT&CK techniques |
| Exports | Matrix JSON/CSV, gap CSV and ATT&CK Navigator layer |

## Quick start

**Requirements:** Python, pip, and an internet connection for downloading the full ATT&CK dataset on first run.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:IBT_ADMIN_PASSWORD = "replace-with-a-strong-password"
python run.py
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export IBT_ADMIN_PASSWORD='replace-with-a-strong-password'
python run.py
```

Open **http://127.0.0.1:8000** and sign in as `admin` with the password you configured. If `IBT_ADMIN_PASSWORD` is not set when the initial admin account is created, the application generates a password and prints it to the terminal once. Keep credentials private.

Interactive API documentation: **http://127.0.0.1:8000/docs**.

## MITRE ATT&CK dataset setup

The full `data/enterprise-attack.json` file is **not included** in this repository because it exceeds GitHub's 25 MB browser-upload limit.

On startup, iBlueTeam attempts to download the official ATT&CK Enterprise STIX dataset and import it into the local SQLite database. If the download fails, the application can use a limited built-in fallback dataset; the full matrix will not be available.

To install the full dataset manually:

1. Download [`enterprise-attack.json`](https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json) from the [official MITRE CTI repository](https://github.com/mitre/cti).
2. Save the file to `data/enterprise-attack.json` in the project directory.
3. Run:

```bash
python run.py --reimport-attack
```

The dataset is excluded by `.gitignore`; do not commit it to the repository. If the local file is absent, the application attempts to download it before using its fallback dataset.

## Coverage calculation

Coverage is derived from the relationship between a technique, its detection rules, the latest test results and the availability of associated log sources.

| State | Interpretation |
|---|---|
| Full | At least one enabled rule has a successful latest test and all associated log sources are collected |
| Partial | A rule exists, but is in draft, untested, has a failed latest test or lacks specified log sources |
| Gap | No suitable active rule exists, or required telemetry is unavailable |
| Blind | A gap specifically associated with missing telemetry |

For implementation details, see [docs/coverage.md](docs/coverage.md).

## Deployment and configuration

Useful startup options:

```bash
python run.py --port 9000
python run.py --no-sample
python run.py --reimport-attack
python run.py --reload
python run.py --lan
```

`--lan` binds the server to network interfaces so other devices on the same network can reach it. **Use this only on a trusted, controlled network.** Do not expose this prototype directly to the public internet.

Supported environment variables include `IBT_ADMIN_PASSWORD`, `IBT_SECRET`, `IBT_TARGET_NAME`, `IBT_TARGET_LAT` and `IBT_TARGET_LON`.

For optional lab-network mapping, edit the example configuration described in [data/LAB_LOCATIONS_SETUP.md](data/LAB_LOCATIONS_SETUP.md). Replace sample addresses and coordinates with values appropriate for your own lab. Never commit real credentials, private keys, secrets or sensitive infrastructure details.

## Project structure

```text
backend/       FastAPI endpoints, models, authentication, coverage logic, ATT&CK import
frontend/      HTML, CSS and JavaScript application
honeypot/      Sensor and traffic simulation utilities
data/          Sample rules and example configuration
docs/          Architecture, data model, coverage, honeypot and demo documentation
run.py         Application entry point
requirements.txt
README.md
```

## Documentation

- [Architecture and security](docs/architecture.md)
- [Data model and API overview](docs/data-model.md)
- [Coverage methodology](docs/coverage.md)
- [Honeypot setup and event handling](docs/honeypot.md)
- [Demo walkthrough](docs/demo.md)
- [Lab location configuration](data/LAB_LOCATIONS_SETUP.md)

## Security and limitations

- This is an educational and portfolio prototype; it has not been independently production-hardened.
- The live monitor includes **synthetic events**. These are demonstrations, not evidence of actual attacks.
- The honeypot sensor requires a separately configured environment. Incoming connections and scans are not automatically proof of malicious intent.
- There is no direct SIEM integration in this version. Rule and log-source information is entered through the application or imported from files.
- Coverage associations are technique-based and may not distinguish every platform-specific detection scenario.
- SQLite is intended for a small local deployment, not a large concurrent production workload.
- Google Fonts may require an internet connection; the interface can fall back to system fonts.

## Project purpose

Built to explore **blue-team workflows, detection engineering, ATT&CK mapping, telemetry visibility and practical cybersecurity application development**.
