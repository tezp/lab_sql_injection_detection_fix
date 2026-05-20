# Lab Instructions

## Scenario

The Dark Kittens group has launched attacks against the Globomantics employee portal.

Security analysts suspect attackers may be exploiting SQL Injection vulnerabilities to gain unauthorized access.

As a security engineer at Globomantics, your objective is to:

1. Start the vulnerable application
2. Verify normal login behavior
3. Exploit SQL Injection
4. Detect suspicious SQL Injection indicators from logs
5. Investigate vulnerable code
6. Apply a secure remediation
7. Verify mitigation

Estimated completion time:

10–15 minutes

---

# Task 1: Start the vulnerable application

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start Flask:

```bash
cd app

python3 app.py
```

Expected output:

```text
Running on:
http://127.0.0.1:5000
```

Keep this terminal running.

Open another terminal for remaining tasks.

---

# Task 2: Verify normal authentication behavior

Run:

```bash
curl \
-X POST \
http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{
"username":"alice",
"password":"password123"
}'
```

Expected response:

```json
{
 "status":"success",
 "user":"alice",
 "role":"employee"
}
```

This confirms legitimate authentication succeeds.

---

# Task 3: Exploit SQL Injection

Attack the login endpoint:

```bash
curl \
-X POST \
http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{
"username":"'\'' OR '\''1'\''='\''1'\'' --",
"password":"anything"
}'
```

Expected response:

```json
{
 "status":"success",
 "user":"alice",
 "role":"employee"
}
```

Observe:

The payload:

```text
' OR '1'='1' --
```

contains:

- `'` → closes the original username string
- `OR '1'='1'` → adds a condition that is always true
- `--` → comments out the remainder of the SQL query

The resulting query may become:

```sql
SELECT *
FROM users
WHERE username=''
OR '1'='1'
--'
AND password='anything'
```

Because:

```sql
'1'='1'
```

always evaluates to true, the application grants access without validating legitimate credentials.

---

# Task 4: Detect suspicious SQL Injection indicators from logs

Analyze logs:

```bash
python3 scripts/detect_sqli.py
```

Expected output:

```text
Potential SQL Injection payloads detected

Reason:
Contains OR-based always true condition

Reason:
Contains SQL comment sequence

Evidence:
LOGIN_FAILED username=' OR '1'='1' --

```

Observe:

The detection script identifies patterns commonly associated with SQL Injection attempts, including:

- Always-true conditions such as:

```text
OR '1'='1'
```

- SQL comment sequences:

```text
--
```

These patterns appeared in the payload submitted to the login endpoint.

Security teams often review similar indicators in application logs when investigating suspicious authentication activity.

---

# Task 5: Review vulnerable code

Open:

```bash
nano app/app.py
```

Locate:

```python
query = f"""
SELECT *
FROM users
WHERE username='{username}'
AND password='{password}'
"""

cursor.execute(query)
```

Observe:

User input is inserted directly into SQL.

This allows attackers to manipulate query behavior.

---

# Task 6: Apply secure remediation

Replace:

## Vulnerable code

```python
query = f"""
SELECT *
FROM users
WHERE username='{username}'
AND password='{password}'
"""

cursor.execute(query)
```

Replace with:

## Secure implementation

```python
query = """
SELECT *
FROM users
WHERE username=?
AND password=?
"""

cursor.execute(
    query,
    (
        username,
        password
    )
)
```

Parameterized queries separate SQL commands from user-controlled input.

Save:

```text
CTRL + O
```

Exit:

```text
CTRL + X
```

---

# Task 7: Restart application

Stop Flask:

```text
CTRL + C
```

Restart:

```bash
cd app

python3 app.py
```

---

# Task 8: Verify mitigation

Repeat the SQL Injection attack:

```bash
curl \
-X POST \
http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{
"username":"'\'' OR '\''1'\''='\''1'\'' --",
"password":"anything"
}'
```

Expected:

```json
{
 "status":"failed"
}
```

or:

```text
401 Unauthorized
```

Observe:

The SQL Injection payload no longer bypasses authentication.

Compare this result with Task 3:

- Before remediation → authentication succeeded
- After remediation → authentication fails

The application now requires valid credentials to authenticate successfully.

---

# Summary

In this lab you:

- Investigated suspicious login activity
- Exploited SQL Injection
- Detected attack indicators from logs
- Applied secure coding practices
- Verified successful mitigation

The Globomantics employee portal is now protected against this SQL Injection technique.