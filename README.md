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

This public repo is intentionally small.

```text
answers/
  1/ ... 31/        Numbered Python submission attempts.
  29/               Final accepted variant.

requirements.txt    Local Python package versions used for the run.
README.md           This project note.
```

The answer folders keep only the Python scripts in version control. Generated
Excel files, generated images, task packages, datasets, local archives, and
virtual environments are ignored.

## What Is Not Included Yet

The official task package, datasets, briefing files, screenshots, generated
workbooks, and generated charts are not published here for now.

Those files are kept out of git until I am sure they are allowed to be
redistributed. The scripts remain useful as a record of the implementation and
debugging process, but they may need the original competition data to run
unchanged.

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

If the required competition dataset is available in the expected location:

```powershell
cd answers\29
..\..\venv\Scripts\python.exe solusi-retail.py
```

The script writes its outputs to the current working directory. Output files are
ignored by git so rerunning the solution does not dirty the repository with
generated artifacts.

## Notes

This repository is mainly a code and process record. I may add the task package,
sample data, or fuller write-up later if redistribution is confirmed.
