# Detecting and Remediating SQL Injection Attacks in a Python Web Application

## Overview

This lab simulates a SQL Injection attack against the Globomantics employee portal.

Learners investigate suspicious authentication activity, exploit a vulnerable login endpoint, analyze logs for attack indicators, remediate the vulnerability using parameterized queries, and verify successful mitigation.

Estimated duration:

10–15 minutes

---

# Scenario

The Dark Kittens group has launched attacks against the Globomantics employee portal.

Security analysts suspect attackers may be exploiting SQL Injection vulnerabilities to gain unauthorized access.

You have been tasked with:

- Investigating suspicious login activity
- Confirming whether SQL Injection is possible
- Reviewing attack evidence from logs
- Applying secure remediation
- Verifying mitigation

---

# Environment Architecture

See:

```text
architecture.md
```

Environment contains:

- Vulnerable Flask API
- SQLite database
- SQL Injection detection script
- Application logs
- Bash setup automation

---

# Prerequisites

Required:

- Linux or macOS terminal
- Python 3.10+

Recommended:

- Ubuntu 22.04

---

# Environment Setup

Run:

```bash
bash setup.sh
```

Activate:

```bash
source .venv/bin/activate
```

Seed database:

```bash
python3 scripts/seed_db.py
```

---

# Start Vulnerable Application

Run:

```bash
cd app

python3 app.py
```

Expected:

```text
Running on:
http://127.0.0.1:5000
```

---

# Lab Exercise

Follow:

```text
Lab Instructions.md
```

---

# Reset Environment

Reset database and logs:

```bash
bash reset-lab.sh
```

---

# Troubleshooting

### Flask app not starting

Verify:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r app/requirements.txt
```

---

### Port 5000 already in use

Find process:

```bash
lsof -i :5000
```

Terminate:

```bash
kill -9 <pid>
```

---

### Database missing

Regenerate:

```bash
python3 scripts/seed_db.py
```

---

# Expected Learning Outcomes

By completing this lab, learners should be able to:

✓ Exploit SQL Injection vulnerabilities

✓ Detect attack indicators from logs

✓ Understand unsafe SQL construction

✓ Implement parameterized queries

✓ Verify mitigation effectiveness