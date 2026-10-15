#!/usr/bin/env python3
"""BSc Midwifery Mock Exit Exam (2017 E.C. Mid-Year, free sample).

A timed, terminal-based practice exam. Progress is saved automatically so an
unfinished exam can be resumed. Questions live in questions.json.
"""

import json
import sys
import textwrap
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "questions.json"
PROGRESS_FILE = BASE_DIR / ".exam_progress.json"
MINUTES = 30
LETTERS = "ABCD"
WIDTH = 78

HELP = (
    "Commands:  a/b/c/d = answer   n = next   p = previous   "
    "g <num> = go to question\n"
    "           l = list progress  s = submit  h = help  q = save & quit"
)


# ---------------------------------------------------------------- helpers
def wrap(text, indent=""):
    return textwrap.fill(text, WIDTH, initial_indent=indent, subsequent_indent=indent)


def load_questions():
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_progress(answers, current, end_at):
    try:
        PROGRESS_FILE.write_text(
            json.dumps({"answers": answers, "current": current, "end_at": end_at})
        )
    except OSError:
        pass


def load_progress(total):
    try:
        data = json.loads(PROGRESS_FILE.read_text())
        if (
            data["end_at"] > time.time()
            and len(data["answers"]) == total
            and 0 <= data["current"] < total
        ):
            return data
    except (OSError, ValueError, KeyError):
        pass
    clear_progress()
    return None


def clear_progress():
    try:
        PROGRESS_FILE.unlink()
    except OSError:
        pass


def fmt_time(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


# ---------------------------------------------------------------- display
def show_question(questions, answers, current, end_at):
    q = questions[current]
    remaining = end_at - time.time()
    print("\n" + "=" * WIDTH)
    print(f"Question {current + 1} of {len(questions)}"
          f"   |   Time left: {fmt_time(remaining)}"
          + ("  (hurry!)" if remaining <= 300 else ""))
    print("=" * WIDTH)
    print(f"[{q['topic']}]\n")
    print(wrap(q["question"]) + "\n")
    for i, opt in enumerate(q["options"]):
        mark = "*" if answers[current] == i else " "
        print(textwrap.fill(f"{mark} {LETTERS[i]}. {opt}", WIDTH,
                            subsequent_indent="     "))
    print()


def show_overview(answers, current):
    print("\nProgress (✔ answered, · unanswered, > current):")
    cells = []
    for i, a in enumerate(answers):
        sym = "✔" if a is not None else "·"
        prefix = ">" if i == current else " "
        cells.append(f"{prefix}{i + 1:>2}{sym}")
    for i in range(0, len(cells), 10):
        print("  " + "  ".join(cells[i:i + 10]))
    print(f"  Unanswered: {answers.count(None)}")


def show_results(questions, answers):
    total = len(questions)
    correct = sum(1 for q, a in zip(questions, answers) if a == q["answer"])
    pct = round(correct / total * 100)

    if correct >= 17:
        msg = "Excellent work!"
    elif correct >= 13:
        msg = "Good, review the questions you missed."
    else:
        msg = "Keep going: revise the weak topics and retry."

    print("\n" + "#" * WIDTH)
    print(f"  YOUR SCORE: {correct} / {total}   ({pct}% correct)")
    print(f"  {msg}")
    print("#" * WIDTH)

    print("\nREVIEW YOUR ANSWERS")
    for i, (q, a) in enumerate(zip(questions, answers), start=1):
        if a is None:
            verdict = "Not answered"
        elif a == q["answer"]:
            verdict = "Correct"
        else:
            verdict = "Wrong"
        print("\n" + "-" * WIDTH)
        print(f"Q{i} · {q['topic']} · {verdict}")
        print(wrap(q["question"]))
        for j, opt in enumerate(q["options"]):
            tag = ""
            if j == q["answer"]:
                tag = "  ✓ correct"
            elif j == a:
                tag = "  ✗ your answer"
            print(textwrap.fill(f"  {LETTERS[j]}. {opt}{tag}", WIDTH,
                                subsequent_indent="     "))
        print(wrap("Rationale: " + q["rationale"], ""))
        print(wrap("Source: 2017 E.C. Mid-Year Exit Exam · Reference: "
                   + q["reference"]))

    print("\n" + "=" * WIDTH)
    print("Want more practice? The full edition has 150 questions from")
    print("2016 E.C. to 2018 E.C. with detailed rationales.")
    print("Order on Telegram: @abdur66  (https://t.me/abdur66)")
    print("=" * WIDTH)
    print(wrap(
        "© 2026 Abdurezak Aliyi Hamid · Exit Exam Academy. Practice questions "
        "from the 2017 E.C. Mid-Year Exit Exam. Not an official publication of "
        "the Ministry of Health or any examination body. Confirm clinical "
        "doses and protocols against the latest national guideline."
    ))


# ---------------------------------------------------------------- main flow
def run_exam(questions):
    total = len(questions)
    resume = load_progress(total)

    if resume:
        answers, current, end_at = resume["answers"], resume["current"], resume["end_at"]
        print(f"Resuming your unfinished exam ({fmt_time(end_at - time.time())} left).")
    else:
        answers = [None] * total
        current = 0
        end_at = time.time() + MINUTES * 60

    save_progress(answers, current, end_at)
    print(HELP)
    warned = False

    while True:
        if time.time() >= end_at:
            print("\nTime is up! Submitting your exam automatically.")
            break

        show_question(questions, answers, current, end_at)
        try:
            raw = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nProgress saved. Run the script again to resume.")
            save_progress(answers, current, end_at)
            return None

        if time.time() >= end_at:
            print("\nTime is up! Submitting your exam automatically.")
            break

        cmd, _, arg = raw.partition(" ")
        if cmd in ("a", "b", "c", "d"):
            answers[current] = "abcd".index(cmd)
            warned = False
        elif cmd == "n":
            if current < total - 1:
                current += 1
            else:
                print("That was the last question. Type 's' to submit.")
        elif cmd == "p":
            current = max(0, current - 1)
        elif cmd == "g" and arg.isdigit() and 1 <= int(arg) <= total:
            current = int(arg) - 1
        elif cmd == "l":
            show_overview(answers, current)
        elif cmd == "h":
            print(HELP)
        elif cmd == "q":
            save_progress(answers, current, end_at)
            print("Progress saved. Run the script again to resume.")
            return None
        elif cmd == "s":
            left = answers.count(None)
            if left and not warned:
                print(f"\n{left} unanswered. Type 's' again to submit anyway.")
                warned = True
                continue
            break
        else:
            print("Unknown command. Type 'h' for help.")

        save_progress(answers, current, end_at)

    clear_progress()
    return answers


def main():
    questions = load_questions()
    total = len(questions)

    print("=" * WIDTH)
    print("BSc Midwifery Mock Exit Exam  (Free sample · Previous exam questions)")
    print("=" * WIDTH)
    print(wrap(
        "These questions are provided for your practice and preparation for the "
        "National Exit Exam. Use them as a timed self-assessment to review "
        "important concepts, test your knowledge, and strengthen your exam "
        "readiness."
    ))
    print(f"\n  {total} questions  |  {MINUTES} min time limit  |  Instant results")
    print("  Answers are saved as you go. The exam submits automatically when "
          "time runs out.\n")

    while True:
        if not load_progress(total):
            try:
                input("Press Enter to start the exam (Ctrl+C to exit)... ")
            except (EOFError, KeyboardInterrupt):
                print()
                return 0

        answers = run_exam(questions)
        if answers is None:
            return 0

        show_results(questions, answers)
        try:
            again = input("\nRetake the exam? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if again != "y":
            return 0


if __name__ == "__main__":
    sys.exit(main())
