# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 3.x     | ✅ Yes             |
| 2.x     | ⚠️ Security fixes only |
| 1.x     | ❌ No              |

## Reporting a Vulnerability

If you discover a security vulnerability, **do not open a public issue**.

### Preferred: GitHub Security Advisory

1. Go to the **Security** tab on GitHub: https://github.com/ZQM-Computing/volusia-portal/security/advisories
2. Click **New draft security advisory**
3. Fill in the details (title, description, severity, CVSS if known)
4. Submit as a draft — the maintainers will be notified

### Alternative: Email

- **Email**: zqmcomputing@gmail.com
- **Subject line**: `[SECURITY] volusia-portal: <brief description>`
- Include steps to reproduce, affected version, and any relevant logs

Please allow up to 14 days for a response. If you do not hear back, follow up.

### What NOT to do

- Do NOT open public issues for security vulnerabilities
- Do NOT disclose the vulnerability publicly before a fix is released
- Do NOT include exploit code in your report

## Encryption

In transit: all API traffic should be served over HTTPS in production.
At rest: SQLite database files should be stored on encrypted volumes (BitLocker / LUKS).

## Response Process

1. Report received and acknowledged (within 14 days)
2. Triage: severity assessment, affected versions identified
3. Fix developed and tested on a private branch
4. Patch released and advisory published
5. Public disclosure after fix is available

## Scope

This policy covers the Project Volusia repository only.
External dependencies (FastAPI, React, Leaflet, etc.) are covered by their own security policies.
