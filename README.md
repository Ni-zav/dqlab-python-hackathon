# DQLab Python Hackathon: Retail Recovery

Python solution archive for my DQLab Retail Recovery hackathon run.

Repository:

```text
https://github.com/Ni-zav/dqlab-python-hackathon
```

The final accepted submission is:

```text
answers/29/solusi-retail.py
```

Final result:

```text
Excel correctness: 18 / 18
Image output: 100%
Actual image output: 100%
```

## What Is Included

This public repo keeps the final submission history compact, but it now also
includes the competition prompt, preview dataset, selected preparation notes,
and final chart outputs that are allowed to be shared publicly.

```text
answers/
  1/ ... 31/        Numbered Python submission attempts.
  29/               Final accepted variant.

archive/
  hackathon_playbook.md
  pre-start/
    analysis/       Dataset analysis notes and reproduction script.
    briefing/       Briefing summary used to plan the run.
    dataset/        Preview dataset released before the task.
  root-run-output/  Final published chart outputs.
  submission-prep/  Submission planning summary.

tasks/
  snippet_code_matplotlib.py
  rising_star_*_incomplete.png
  data_penjualan.xlsx
  retail_insight_example.xlsx

SOAL-HACKATHON.md   Public markdown copy of the official task statement.
requirements.txt    Local Python package versions used for the run.
README.md           This project note.
```

The answer folders still keep only the Python scripts. The newly published
supporting files are the minimum set that makes the repo readable as both a
competition record and a technical post.

## Publication Status

Redistribution of the materials listed above is now confirmed, so they are
tracked in this repository.

I still leave raw attachment bundles, duplicate source formats, screenshots,
meeting transcript files, generated workbooks, loose drafts, caches, and local
virtual environments out of git. That keeps the public repo focused on the
task, data, code, analysis process, and final result artifacts.

## Final Submission

The accepted script is:

```text
answers/29/solusi-retail.py
```

It is a single-file solution that:

- discovers the transaction input file from the working directory or local task
  layout,
- builds the required Excel workbook,
- generates the required chart images,
- handles the association-rule formatting needed by the grader.

The last point was the final scoring bottleneck. The calculations were already
right before the final score; the remaining issue was the exact display order of
two multi-item association rules in the workbook output.

## Scoring Trail

The later submissions were treated as controlled experiments. Each variant tried
to change one hypothesis at a time.

| Variant | Score | Note |
| --- | ---: | --- |
| 3 / 4 | 12/18 | Full pipeline existed, but workbook output was not exact yet. |
| 5 | 14/18 | Item ordering changes improved the workbook. |
| 8 / 12 | 16/18 | Most rows were correct; only a small mismatch remained. |
| 19 / 20 / 21 | 15/18 | Changing the trend-growth rows was the wrong direction. |
| 26 | 14/18 | Replacing a confirmed-good packaging pair broke the score. |
| 28 | 16/18 | A near-threshold rule replacement was not the missing answer. |
| 29 | 18/18 | Final accepted formatting for the remaining packaging pair. |

The main lesson was to stop broad rewrites once the score was close. From
16/18 onward, the useful strategy was preserving known-good behavior and making
small, testable changes.

## Local Environment

The run used Python with the package versions listed in `requirements.txt`.

Core packages:

```text
matplotlib
pandas
mlxtend
openpyxl
```

The original working environment used a local `venv/`, which is ignored in git.

## Running

The repo now includes the preview dataset at
`archive/pre-start/dataset/Transaksi.csv`. The accepted script still expects a
competition-style input file to be available in a location it can discover.

If the required dataset is available in the expected location:

```powershell
cd answers\29
..\..\venv\Scripts\python.exe solusi-retail.py
```

The script writes its outputs to the current working directory. Output files are
ignored by git so rerunning the solution does not dirty the repository with
generated artifacts.

## Notes

This repository is now a compact public record of the competition run: the
submission trail, the final accepted answer, the public task statement, the
published input datasets, and the selected notes that explain how the solution
was developed.
