import re
from pathlib import Path

log_path = Path(__file__).resolve().parents[1] / "logs" / "app.log"

patterns = {
    "Contains OR-based always-true condition": re.compile(
        r"or\s+['\"]?1['\"]?\s*=\s*['\"]?1",
        re.IGNORECASE
    ),
    "Contains SQL comment sequence": re.compile(
        r"--"
    ),
    "Contains UNION SELECT pattern": re.compile(
        r"union\s+select",
        re.IGNORECASE
    ),
}

if not log_path.exists():
    print("No log file found. Run the application and perform login attempts first.")
    raise SystemExit(1)

findings = []

with open(log_path, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        for reason, pattern in patterns.items():
            if pattern.search(line):
                findings.append((line_number, reason, line.strip()))

if not findings:
    print("No SQL Injection patterns detected.")
else:
    print("Potential SQL Injection payloads detected:\n")
    for line_number, reason, line in findings:
        print(f"Line: {line_number}")
        print(f"Reason: {reason}")
        print(f"Evidence: {line}")
        print()