# User Manual

**Application:** Adjective Collector
**Last updated:** 2026-06-10

---

## 1. What Is Adjective Collector?

Adjective Collector is a web application where users can submit adjectives — descriptive words such as *happy*, *brave*, or *curious*. The app collects submissions from everyone who visits the page and displays a live dashboard showing all submitted adjectives ranked by how often they have been submitted.

---

## 2. Getting Started

No account or login is required. Simply open the application in your web browser to begin.

---

## 3. Submitting an Adjective

1. Locate the **text input field** on the main page.
2. Type a single adjective into the field (e.g. `brave`).
3. Click the **Submit** button (or press Enter).
4. A confirmation message will appear confirming your word was added.

**What happens behind the scenes:**
- Your input is trimmed of any extra spaces and converted to lowercase automatically.
- If the word has never been submitted before, it is added to the database with a count of 1.
- If the word already exists, its submission counter is incremented by 1.

---

## 4. Viewing the Dashboard

After submitting (or on page load), the dashboard displays all collected adjectives along with how many times each has been submitted. Words are listed in the order they are retrieved from the database.

---

## 5. Known Limitations

| Limitation | Details |
|---|---|
| Single words only | Phrases or sentences will be stored as-is but are not intended use |
| No editing | You cannot edit or delete a word you have submitted |
| No undo | Submissions cannot be reversed by the user |
| Case-insensitive | `Happy`, `HAPPY`, and `happy` are all treated as the same word |
| No duplicates | Each unique word has one entry; re-submitting it increments the counter |

---

## 6. Error Messages

| Message | Cause | Solution |
|---|---|---|
| "Empty input!" | You submitted the form with nothing typed | Type an adjective before submitting |

---

## 7. Frequently Asked Questions

**Can I submit the same word more than once?**
Yes. Each time you submit the same word, its counter increases by 1.

**Can I delete a word I submitted?**
No. Users cannot delete submissions. Contact the application operator if you need a word removed.

**Is my personal information stored?**
No. The application only stores the word itself and its submission count. See the [Privacy Policy](privacy_policy.md) for full details.

**What kind of words should I submit?**
Any single adjective in any language. Please keep submissions appropriate — see the [Terms of Use](terms_of_use.md) for guidelines.

---

## 8. Contact & Support

For questions, issues, or requests, contact the application operator at:

**Email:** [insert contact email]
