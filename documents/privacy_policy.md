# Privacy Policy

**Application:** Adjective Collector
**Last updated:** 2026-06-12

---

## 1. Introduction

Adjective Collector is a web application that crowdsources adjectives from its users and displays the most frequently submitted ones. This privacy policy explains what data the application collects, how it is used, and how it is protected.

---

## 2. Data We Collect

This application collects the following data:

- **Submitted words (adjectives)** — the text you enter into the submission form.
- **Submission frequency** — how many times a given word has been submitted in total.
- **Username** — the name you choose when creating an account.
- **Password hash** — your password is stored as a one-way bcrypt hash; the plaintext password is never retained.
- **Role** — whether your account has standard user or administrator access.
- **Submission authorship** — when a new adjective is first submitted, it is linked to the submitter's user ID.
- **Session data** — a server-side session cookie is used to keep you logged in; it stores your user ID, username, and role for the duration of your session.

All submitted words are automatically converted to lowercase and stripped of leading/trailing whitespace before being stored.

---

## 3. Data We Do NOT Collect

This application does **not** collect the following:

- Real names, email addresses, or other contact information
- IP addresses or device identifiers
- Browser type, operating system, or user-agent data
- Timestamps of submissions

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
- **Password hashing:** Passwords are never stored in plaintext. They are hashed using bcrypt before being written to the database.
- **Session management:** Server-side sessions are used to authenticate logged-in users. Sessions are cleared in full when you log out.
- **Credential isolation:** Database credentials are stored in a `.env` file outside of version control and never exposed to end users.

---

## 7. Data Sharing

We do not sell, trade, or otherwise transfer collected data to third parties. No external analytics services, advertising networks, or data brokers are used.

---

## 8. Data Retention

Submitted adjectives and their counters are stored indefinitely in the database until manually removed by the application operator. There is no automated deletion process.

---

## 9. Your Rights

If you have created an account, you may contact the application operator to request the deletion of your account and any associated data. If you have submitted a word you would like removed, you may also contact the operator using the details below.

---

## 10. Changes to This Policy

Any future changes to this privacy policy will be reflected in an updated version of this document with a revised "Last updated" date.

---

## 11. Contact

For any questions regarding this privacy policy, please contact the application operator at:

**Email:** mamoa112@osloskolen.no
