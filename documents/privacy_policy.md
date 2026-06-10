# Privacy Policy

**Application:** Adjective Collector
**Last updated:** 2026-06-10

---

## 1. Introduction

Adjective Collector is a web application that crowdsources adjectives from its users and displays the most frequently submitted ones. This privacy policy explains what data the application collects, how it is used, and how it is protected.

---

## 2. Data We Collect

The only data collected by this application is:

- **Submitted words (adjectives)** — the text you enter into the submission form.
- **Submission frequency** — how many times a given word has been submitted in total.

All submitted words are automatically converted to lowercase and stripped of leading/trailing whitespace before being stored.

---

## 3. Data We Do NOT Collect

This application does **not** collect any personally identifiable information (PII). Specifically, we do not collect:

- Names, email addresses, or any contact information
- IP addresses or device identifiers
- Browser type, operating system, or user-agent data
- Cookies or session data
- Timestamps of submissions
- User accounts or authentication credentials

---

## 4. How Data Is Used

The collected words are used solely to:

- Store the adjective in the database if it has not been submitted before.
- Increment the submission counter if the adjective already exists.
- Display all collected adjectives and their counts on the dashboard.

The data is not used for profiling, advertising, or any purpose beyond the core functionality of the application.

---

## 5. Data Storage

All data is stored in a self-hosted MariaDB database. No data is sent to or stored by any third-party cloud service. Database credentials are stored in a `.env` configuration file and are never committed to version control.

---

## 6. Security Measures

The following measures are in place to protect the application and its data:

- **Input validation:** Empty submissions are rejected; all input is stripped and lowercased before use.
- **Parameterised queries:** All database queries use parameterised statements to prevent SQL injection.
- **No session state:** The application does not use cookies or server-side sessions, eliminating session-hijacking risks.
- **Credential isolation:** Database credentials are stored in a `.env` file outside of version control and never exposed to end users.
- **Minimal data surface:** Because no personal data is collected, there is no PII at risk in the event of a data breach.

---

## 7. Data Sharing

We do not sell, trade, or otherwise transfer collected data to third parties. No external analytics services, advertising networks, or data brokers are used.

---

## 8. Data Retention

Submitted adjectives and their counters are stored indefinitely in the database until manually removed by the application operator. There is no automated deletion process.

---

## 9. Your Rights

Because this application does not collect any personal data, there is no personal information to access, correct, or delete. If you have submitted a word you would like removed, you may contact the application operator using the details below.

---

## 10. Changes to This Policy

Any future changes to this privacy policy will be reflected in an updated version of this document with a revised "Last updated" date.

---

## 11. Contact

For any questions regarding this privacy policy, please contact the application operator at:

**Email:** mamoa112@osloskolen.no
