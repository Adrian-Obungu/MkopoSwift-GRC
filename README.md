# MkopoSwift-GRC

<div align="center">
  <img src="./assets/banner.png" alt="MkopoSwift Banner">
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Compliance-KES%209.5M%20Risk%20Mitigated-brightgreen?style=for-the-badge&logo=checkmarx" alt="Risk Mitigated">
  <img src="https://img.shields.io/badge/ISO%2FIEC%2027701%3A2025-PIMS-blue?style=for-the-badge&logo=iso" alt="ISO 27701">
  <img src="https://img.shields.io/badge/Kenyan%20DPA%202019-Section%2043%20Ready-red?style=for-the-badge" alt="KDPA">
  <br>
  <img src="https://img.shields.io/github/languages/top/Adrian-Obungu/MkopoSwift-GRC" alt="Top Language">
  <img src="https://img.shields.io/github/license/Adrian-Obungu/MkopoSwift-GRC" alt="License">
  <img src="https://img.shields.io/github/last-commit/Adrian-Obungu/MkopoSwift-GRC" alt="Last Commit">
</div>

<br>

<h3 align="center">Stop guessing compliance. Engineer it.</h3>

---

## 💡 The Problem: Navigating Kenya's Data Protection Landscape

Kenya's Office of the Data Protection Commissioner (ODPC) is actively enforcing the Data Protection Act (2019), imposing significant fines and stringent compliance requirements on digital credit providers (fintechs). Recent cases underscore the severe financial and reputational risks:

*   **Mulla Pride Ltd:** Fined KES 2.97 Million for unauthorized contact scraping, highlighting the critical need for robust data minimization practices.
*   **Chizzy Taabu Orwa v Mast Jägermeister SE:** Fined KES 1.5 Million for generic consent practices, emphasizing the necessity of immutable, purpose-specific consent records.

Beyond fines, fintechs face mandatory 72-hour breach notification requirements under Section 43 of the Act and often endure lengthy, 90-day bank vendor security assessments. These challenges create a complex and costly compliance burden.

---

## ✨ The Solution: MkopoSwift-GRC Appliance

**MkopoSwift-GRC** is an offline-first, cryptographically verifiable Governance, Risk, and Compliance (GRC) platform engineered specifically for Kenyan digital credit providers. It directly addresses the regulatory challenges by mapping to **ISO/IEC 27701:2025** and the **Kenyan Data Protection Act 2019**. The entire appliance runs locally, ensuring no cloud dependencies and providing quantifiable risk mitigation and accelerated procurement.

### Key Modules:

*   **Data Minimization & Consent Engine:** An SQLite/PostgreSQL schema with strict `CHECK` constraints that prevent mass contact scraping (Mulla Pride case) and enforce immutable, purpose-specific consent (Mast Jägermeister case).
*   **72-Hour Breach Triage Automation:** A Python script that scans logs, detects bulk exports of National IDs, checks the ODPC notification window, and generates a Section 43 notification.
*   **Cryptographic Evidence Vault:** A `.grc_vault` directory containing hashed evidence assets and a `verify_vault_integrity.py` script that provides a one-click audit attestation report.
*   **Streamlit Dashboard:** A Dockerized visual interface displaying risk metrics (KES 9.5M fines avoided), live breach simulation, vault integrity status, and consent timelines. (Local demo only – see Quick Start)

---

## 🚀 Key Features

*   🔒 **Structural Data Minimisation:** Blocks contact scraping, preventing Mulla Pride-style fines.
*   ✍️ **Immutable Consent Ledger:** Ensures explicit, purpose-specific consent, avoiding Mast Jägermeister-style penalties.
*   ⏱️ **72-Hour Breach Auto-Notification:** Automates log analysis and Section 43 notification generation for timely compliance.
*   🔐 **One-Click Cryptographic Vault Verification:** Provides instant audit attestation, cutting bank vendor review times from 90 to 14 days.
*   🖥️ **Local Streamlit Dashboard:** Offers an offline visual interface for real-time risk metrics and compliance posture.

---

## ⚡ Quick Start / Local Demo

Experience the MkopoSwift-GRC appliance locally. Follow these steps using your command line (Windows PowerShell or Git Bash recommended):

```bash
# 1. Clone the repository
git clone https://github.com/Adrian-Obungu/MkopoSwift-GRC.git
cd MkopoSwift-GRC

# 2. Run the database schema (PostgreSQL example)
#    Ensure PostgreSQL is installed and running, then connect to your database
#    and execute the schema file.
# psql -U your_username -d your_database -f data_minimization/schema_postgresql.sql

# 3. Execute the breach simulation (example with sample log)
# python breach_response/breach_triage_automation.py --log sample_access.log.sha256

# 4. Verify the cryptographic vault integrity
python verify_vault_integrity.py

# Expected Output for Vault Verification:
# [PASS] data_minimization/schema_postgresql.sql - Hash matched.
# [PASS] breach_response/breach_triage_automation.py - Hash matched.
# ...
# VAULT INTEGRITY VERIFIED.
```

---

## 📸 Screenshots

*(Actual screenshots will be added here soon.)*

### Dashboard Overview
<img src="screenshots/dashboard_overview.png" alt="Streamlit metrics dashboard showing real-time compliance posture">

### Breach Simulation Output
<img src="screenshots/breach_simulation.png" alt="Terminal output and auto-generated ODPC notification">

### Vault Integrity Report
<img src="screenshots/vault_integrity.png" alt="All system hashes passing verification">

---

## 📂 Repository Structure

```
MkopoSwift-GRC/
├── assets/
│   ├── banner.png
│   └── logo.png
├── breach_response/
│   ├── breach_triage_automation.py
│   ├── odpc_notification_breach_1.md
│   └── sample_access.log.sha256
├── data_minimization/
│   ├── schema_postgresql.sql
│   └── schema_validation.sql
├── vendor_procurement/
│   └── iso27701_dpa_mapping.csv
├── verify_vault_integrity.py
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## 🗺️ Roadmap

Our vision for MkopoSwift-GRC includes:

*   **Multi-Regulation Mapping:** Expanding compliance mapping to additional data protection regulations globally.
*   **ML-Based Anomaly Detection:** Integrating machine learning for proactive identification of data breach indicators.
*   **Automated PDF Audit Reports:** Generating comprehensive, automated audit reports in PDF format for simplified regulatory submissions.
*   **Enhanced Streamlit Dashboard:** Adding more interactive features and visualizations for deeper insights into compliance posture.

---

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

For inquiries, support, or collaboration, please reach out to Adrian Obungu:

*   **Email:** dpo@mkoposwift.co.ke
*   **LinkedIn:** [Adrian Obungu](https://www.linkedin.com/in/adrian-o-9b4856260?utm_source=share_via&utm_content=profile&utm_medium=member_ios)
*   **GitHub:** [Adrian-Obungu](https://github.com/Adrian-Obungu)

---

<div align="center">
  Built with ❤️ in Nairobi, Kenya. Offline-first. GitOps-driven.
</div>
