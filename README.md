# BSc Midwifery Mock Exit Exam (Python)

A timed, terminal-based practice exam based on the 2017 E.C. Mid-Year Exit Exam (free sample, 20 questions, 30 minutes).

## Run

Requires Python 3.8+ and no external packages.

```bash
python exam.py
```

## Commands

| Key | Action |
| --- | --- |
| `a` `b` `c` `d` | Answer the current question |
| `n` / `p` | Next / previous question |
| `g <num>` | Go to a question number |
| `l` | Show progress overview |
| `s` | Submit (type twice if questions are unanswered) |
| `q` | Save and quit |
| `h` | Help |

Progress is saved to `.exam_progress.json`, so an unfinished exam resumes on the next run. The exam auto-submits when time runs out. Results include a score, rationales, and references for every question.

## Files

- `exam.py` - the exam app
- `questions.json` - question data (topic, question, options, answer index, rationale, reference)

## Disclaimer

Practice questions from the 2017 E.C. Mid-Year Exit Exam. Not an official publication of the Ministry of Health or any examination body. Confirm clinical doses and protocols against the latest national guideline.

© 2026 Abdurezak Aliyi Hamid · Exit Exam Academy. Full edition (150 questions): Telegram [@abdur66](https://t.me/abdur66)
