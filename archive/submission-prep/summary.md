# Submission Prep Summary

This file is the reusable starting point for the final task solution. Replace the placeholders with the actual question logic when it arrives.

## Submission Format Status

- Verified from the briefing transcript: participants asked about `.py` versus `.ipynb`, whether multiple files are allowed, and whether Colab can be used.
- Not yet verified from an organizer-facing source: whether the final submission must be a single file, a notebook, a zip, or multiple files.
- Practical default until the official task arrives: keep a single self-contained `.py` solution ready, and be prepared to mirror it into `.ipynb` if the task asks for a notebook.

## Event Branding Update

- The live leaderboard page now shows the competition title as Hackathon Python Retail Crisis & Recovery - May 2026.
- Treat that as the current public-facing event name when referencing the competition in notes, filenames, or final outputs.
- The leaderboard context is active and should be used as the source of truth for the current naming, even though the original briefing deck used the shorter Retail Recovery wording.

## Library Handling

- The transcript shows the organizers were asked whether data libraries and tools would be fixed or flexible.
- We do not yet have an organizer-confirmed package list, so the safe approach is to avoid relying on non-standard libraries unless the task clearly requires them.
- Current prep assumption: use standard Python plus the already-working data stack in the local `venv` when producing the solution.
- If the official task allows extra dependencies, keep them minimal and add only what the final solution truly needs.
- If the submission must stay portable, prefer a self-contained `.py` with explicit imports and avoid notebook-only features.

## Snapshot

- Rows: 42,446
- Distinct invoices: 9,403
- Distinct products: 58
- Date range: 2025-02-01 to 2025-03-04
- Total units: 97,078
- Total revenue: Rp3.439.447.500

## Validation

- Missing rate: 0.00%
- Duplicate row rate: 0.00%
- Price consistency rate: 100.00%
- Variable price products: 0

## Suggested Task Angles

- Revenue ranking
- Daily or weekday trend
- Product contribution and ABC analysis
- Basket analysis at invoice level
- Top invoice outlier inspection

## Ready-Made Objects

- Daily rows: 32
- Product rows: 58
- Top invoices rows: 10

## Next Step Placeholder

Fill the section below once the real task arrives:

```text
TASK QUESTION:
SUBMISSION FORMAT:
APPROACH:
OUTPUT:
VALIDATION:
```

## Current Submission Plan

- If the prompt is script-based, submit one root-level `.py` file with the complete solution and a clear `main()` entry point.
- If the prompt is notebook-based, convert the same logic into a single `.ipynb` with cells in execution order.
- If the prompt allows multiple files, keep helper code minimal and still prefer one primary entry file unless the task explicitly benefits from modularization.
- If the prompt requires email submission, keep the final artifact naming simple and include only what the organizer asks for.

## Group Hackathon Note

- The line about “1 file .py and 2 output result” appears to be participant-reported group-hackathon commentary, not a confirmed organizer rule in the transcript or reports.
- Treat it as a hint, not a requirement, until the official prompt or organizer message says otherwise.
