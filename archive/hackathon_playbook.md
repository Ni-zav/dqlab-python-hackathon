# Hackathon Playbook

Last updated: 2026-05-09

## Goal

This file is the fast operational prep guide for the hackathon. It is meant to help us move immediately when the task arrives.

## What We Know So Far

- The event is email-driven and score-based.
- The current dataset is clean, line-item retail transaction data.
- The preview dataset spans 32 transaction days from 2025-02-01 to 2025-03-04.
- The same product price appears fixed throughout the current dataset.
- Basket size appears capped at 10 line items per invoice.

## Good Default Analyses

1. Revenue ranking by product.
2. Daily and weekday sales trends.
3. Invoice-level basket analysis.
4. ABC / Pareto product contribution.
5. Top invoice outlier review.

## Likely Question Shapes

- "Which product contributes the most revenue?"
- "How does revenue change over time?"
- "What are the best-selling products by unit or revenue?"
- "Which invoices are outliers?"
- "Which products are low-velocity but still important?"

## Working Assumptions

- Use `dd-mm-yyyy` parsing for `tgl_transaksi`.
- Keep invoice-level aggregation helpers ready.
- Treat `jumlah_terjual * harga == total_nilai` as a mandatory integrity check.
- Prefer simple, fast, readable Python over complicated abstractions.

## When The Task Arrives

1. Copy the question into a new root analysis note.
2. Map it to the closest prepared helper.
3. Run the relevant aggregation on the dataset.
4. Add one validation check.
5. Produce the final answer with the smallest possible code path.

## Files To Use

- [hackathon_submission_template.py](hackathon_submission_template.py)
- [dataset_deep_dive.md](dataset_deep_dive.md)
- [reports/2026-05-09/hackathon-briefing.md](reports/2026-05-09/hackathon-briefing.md)
