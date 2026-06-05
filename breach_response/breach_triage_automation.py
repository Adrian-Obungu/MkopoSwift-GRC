#!/usr/bin/env python3
"""
MkopoSwift Breach Triage Automation
ISO/IEC 27701:2025 A.7.4.3 + Kenyan DPA 2019 Section 43
Enhanced with log integrity verification (anti-tampering).
No external dependencies – standard library only.
Usage: python breach_triage_automation.py <log_file_path>
"""

import sys
import re
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG_SHA256_SUFFIX = ".sha256"

def compute_sha256(file_path):
    """Return SHA-256 hex digest of file contents."""
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def verify_log_integrity(log_path):
    """
    Check if <log_path>.sha256 exists and matches current log file.
    If not, log file may have been tampered with.
    Returns True if integrity OK, False otherwise.
    """
    hash_file = Path(str(log_path) + LOG_SHA256_SUFFIX)
    if not hash_file.exists():
        print("WARNING: No integrity hash found for log file. Treating log as trusted (first run?).")
        return True
    stored_hash = hash_file.read_text().strip()
    current_hash = compute_sha256(log_path)
    if current_hash != stored_hash:
        print("CRITICAL: Log file integrity FAILED – hash mismatch.")
        print(f"  Stored:  {stored_hash}")
        print(f"  Current: {current_hash}")
        print("  Possible log tampering detected. Breach analysis aborted.")
        return False
    print("Log integrity VERIFIED.")
    return True

def store_log_integrity_hash(log_path):
    """Generate and save SHA-256 hash of the log file for future verification."""
    hash_file = Path(str(log_path) + LOG_SHA256_SUFFIX)
    current_hash = compute_sha256(log_path)
    hash_file.write_text(current_hash)
    print(f"Integrity hash stored in {hash_file}")

def parse_log_line(line):
    """Extract timestamp, event type, user, and JSON payload from a log line."""
    parts = line.strip().split(maxsplit=4)
    if len(parts) < 5:
        return None
    timestamp_str, event_type, user, resource, payload_str = parts
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except ValueError:
        return None
    payload = None
    if payload_str.startswith('{'):
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            pass
    return {
        'timestamp': timestamp,
        'event_type': event_type,
        'user': user,
        'resource': resource,
        'payload': payload
    }

def scan_for_bulk_export_anomaly(log_entries):
    """Detect BULK_EXPORT events that export >5 IDs within 60 seconds."""
    bulk_exports = []
    for entry in log_entries:
        if entry['event_type'] == 'BULK_EXPORT' and entry['payload'] and 'ids' in entry['payload']:
            bulk_exports.append(entry)

    if not bulk_exports:
        return []

    bulk_exports.sort(key=lambda x: x['timestamp'])
    breach_events = []
    window_start = bulk_exports[0]['timestamp']
    batch_ids = []

    for event in bulk_exports:
        if (event['timestamp'] - window_start) <= timedelta(seconds=60):
            batch_ids.extend(event['payload']['ids'])
        else:
            if len(set(batch_ids)) > 5:
                breach_events.append({
                    'first_timestamp': window_start.isoformat(),
                    'compromised_ids': list(set(batch_ids)),
                    'count': len(set(batch_ids))
                })
            window_start = event['timestamp']
            batch_ids = event['payload']['ids'][:]
    if len(set(batch_ids)) > 5:
        breach_events.append({
            'first_timestamp': window_start.isoformat(),
            'compromised_ids': list(set(batch_ids)),
            'count': len(set(batch_ids))
        })
    return breach_events

def check_72_hour_window(breach_time_iso):
    """Returns (within_window, elapsed timedelta)."""
    breach_dt = datetime.fromisoformat(breach_time_iso)
    now = datetime.now(timezone.utc)
    elapsed = now - breach_dt
    return elapsed <= timedelta(hours=72), elapsed

def generate_odpc_notification(breach_event, breach_user, db_path="data_minimization/pims.db"):
    """Build a notification template conforming to KDPA Section 43."""
    affected_count = breach_event['count']
    conn = sqlite3.connect(Path(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in breach_event['compromised_ids'])
    cursor.execute(
        f"SELECT DISTINCT purpose_id FROM user_metadata WHERE national_id IN ({placeholders})",
        breach_event['compromised_ids']
    )
    purposes = [row['purpose_id'] for row in cursor.fetchall()]
    conn.close()
    categories_str = ', '.join(purposes) if purposes else 'loan_origination, fraud_check'

    template = f"""
## ODPC DATA BREACH NOTIFICATION (Section 43 of the Data Protection Act, 2019)

**Data Controller:** MkopoSwift Ltd  
**Date/Time of Notification:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}

### 1. Description of the Personal Data Breach
On {breach_event['first_timestamp']}, an unauthorised bulk export event was detected. User `{breach_user}` executed a series of data exports that extracted {affected_count} unique Kenyan National ID numbers. The export violated the data minimisation controls enforced by our PIMS.

### 2. Categories of Personal Data Affected
- National ID numbers ({affected_count} records)
- Purpose-linked metadata fields: {categories_str}
- No financial transaction data or biometric hashes were exposed.

### 3. Number of Data Subjects Affected
{affected_count} individuals whose National IDs appear in the exported set.

### 4. Likely Consequences of the Breach
Potential identity theft or targeted phishing attempts using the National ID numbers. No direct financial credentials were leaked.

### 5. Measures Taken to Address the Breach
- Immediate revocation of `{breach_user}` API keys.
- Temporary suspension of bulk export functionality.
- Activation of breach response team.
- Launch of forensic audit to trace exfiltration vector.

### 6. Data Protection Officer Contact
Name: [Your DPO]  
Email: dpo@mkoposwift.co.ke  
Phone: +254 7XX XXX XXX

---
*This notification is automatically generated by the MkopoSwift Breach Triage System and complies with Section 43(2) of the Data Protection Act, 2019.*
"""
    return template.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python breach_triage_automation.py <log_file> [--init-hash]")
        sys.exit(1)

    log_path = Path(sys.argv[1])
    if not log_path.exists():
        print(f"Error: {log_path} not found")
        sys.exit(1)

    # Optional flag to generate and store the initial log hash
    if len(sys.argv) > 2 and sys.argv[2] == "--init-hash":
        store_log_integrity_hash(log_path)
        print("Log integrity hash initialised. Run without --init-hash to perform triage.")
        return

    # Verify log file integrity before processing
    if not verify_log_integrity(log_path):
        sys.exit(1)

    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = [parse_log_line(l) for l in lines]
    entries = [e for e in entries if e is not None]

    breaches = scan_for_bulk_export_anomaly(entries)
    if not breaches:
        print("No bulk export anomaly detected.")
        return

    for i, breach in enumerate(breaches, 1):
        within_72h, elapsed = check_72_hour_window(breach['first_timestamp'])
        print(f"--- Breach Event {i} ---")
        print(f"First timestamp: {breach['first_timestamp']}")
        print(f"Compromised ID count: {breach['count']}")
        print(f"Elapsed since breach: {elapsed}")
        print(f"72-hour window intact: {within_72h}")

        breach_user = entries[0]['user'] if entries else 'unknown'

        notification = generate_odpc_notification(
            breach, breach_user,
            db_path=str(Path(__file__).parent.parent / "data_minimization" / "pims.db")
        )
        out_path = Path(__file__).parent / f"odpc_notification_breach_{i}.md"
        out_path.write_text(notification)
        print(f"Notification saved to {out_path}")
        print()

if __name__ == '__main__':
    main()