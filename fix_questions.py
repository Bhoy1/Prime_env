"""
Script to make Q&A questions more specific by adding dates and context.

Adds dates to questions that are too vague or missing temporal context.
"""
import json
from pathlib import Path

# Load Q&A pairs
with open('output/qa_pairs.json', 'r') as f:
    qa_pairs = json.load(f)

# Load all records to get dates
records_dates = {}
for txt_file in Path('data').glob('*.txt'):
    with open(txt_file, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        records_dates[txt_file.name] = first_line

print(f"Loaded {len(records_dates)} record dates")
print(f"Processing {len(qa_pairs)} Q&A pairs...\n")

# Update questions
updated_count = 0
for qa in qa_pairs:
    source_file = qa['source_file']
    question = qa['question']

    if source_file not in records_dates:
        continue

    date = records_dates[source_file]
    original_question = question

    # Replace vague references with specific dates
    if "on this date" in question.lower():
        question = question.replace("on this date", f"on {date}")
        question = question.replace("On this date", f"On {date}")

    if "today" in question.lower() and "today's date" not in question.lower():
        question = question.replace("today", f"on {date}")
        question = question.replace("Today", f"On {date}")

    if "this record" in question.lower():
        question = question.replace("this record", f"the congressional record from {date}")
        question = question.replace("This record", f"The congressional record from {date}")

    # Add date to questions that need temporal context
    # These patterns indicate questions that need a date
    needs_date_patterns = [
        "when did the house adjourn",
        "when did the senate adjourn",
        "which representative resigned",
        "which senator resigned",
        "what measures were reported",
        "what reports were filed",
        "how many votes did",
        "what was the vote",
        "what bills were introduced",
        "what resolutions were introduced",
    ]

    question_lower = question.lower()

    # Check if question needs a date but doesn't have one
    needs_date = any(pattern in question_lower for pattern in needs_date_patterns)
    has_date = any(month in question for month in ['January', 'February', 'March', 'April', 'May', 'June',
                                                     'July', 'August', 'September', 'October', 'November', 'December'])

    if needs_date and not has_date:
        # Add date context to the question
        if question.endswith("?"):
            question = question[:-1] + f" (from the congressional record dated {date})?"
        else:
            question = question + f" (from the congressional record dated {date})"

    # Update if changed
    if question != original_question:
        qa['question'] = question
        updated_count += 1
        print(f"✓ Updated: {source_file}")
        print(f"  Old: {original_question}")
        print(f"  New: {question}\n")

# Save updated Q&A pairs
with open('output/qa_pairs.json', 'w') as f:
    json.dump(qa_pairs, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print(f"Updated {updated_count} questions")
print(f"Saved to output/qa_pairs.json")
print('='*70)
