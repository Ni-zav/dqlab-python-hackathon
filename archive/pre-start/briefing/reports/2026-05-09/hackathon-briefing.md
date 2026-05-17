# DQLab Hackathon Python Briefing Report

Last updated: 2026-05-09

## Purpose

This document captures the briefing information for the DQLab x UjiKompetensi Hackathon Python event, based on the PowerPoint briefing deck, the meeting transcript, and the live leaderboard page.

## Sources

- Briefing deck: [Hackathon Python Retail Recovery - Briefing.pptx](../../Hackathon%20Python%20Retail%20Recovery%20-%20Briefing.pptx)
- Meeting transcript: [meeting-briefing-transcribe.txt](../../meeting-briefing-transcribe.txt)

## Executive Summary

The event is a 24-hour Python hackathon run through an email-driven platform. Participants must already be registered as DQLab members. The system supports registration checks, nickname updates, task requests, complaints, score checks, and task submissions. Scoring focuses on correctness, execution speed, originality, and early submission.

## Confirmed Briefing Facts

### Event and platform

- The event is branded as DQLab x UjiKompetensi Hackathon Python.
- The live leaderboard page currently shows the competition name as Hackathon Python Retail Crisis & Recovery - May 2026.
- The platform is a backend system for hosting, managing, and scoring Python solutions in a limited time window.
- The hackathon is designed for individuals or teams.
- Only already-registered DQLab members can participate.

### Schedule

- The system is live on 9 May 2026 from 7:00 AM to 10:00 AM for testing.
- The hackathon starts on 9 May 2026 at 10:00 AM.
- The competition duration is 24 hours.
- Official announcement happens after fraud checking, no later than 7 days after the submission period ends.

### Submission and interaction model

- All interaction is done by email.
- The submission / interaction address shown in the deck is tugastest@ujikompetensi.com.
- You cannot send more than one email within 5 minutes.
- If you send another email earlier than that, it will not be processed.
- The deck indicates that score can be checked through DQLab’s leaderboard.
- The leaderboard gives immediate result visibility, but the official announcement is delayed.
- The visible leaderboard site is the DQLab Academy leaderboard page, consistent with the existing hackathon workspace link.

### Live system confirmation

- The registration-check email has been answered by the DQLab system.
- The reply explicitly states that the participant is registered in the system.
- The reply also shows the assigned hackathon nickname format: HACK-2026-PYTHON-02-1005.
- This confirms that the email command workflow is active and responding as described in the briefing.

### Live leaderboard confirmation

- The leaderboard UI is live and accessible.
- The competition card on the leaderboard page shows the title Hackathon Python Retail Crisis & Recovery - May 2026.
- This title should be treated as the current public-facing event name unless an organizer update says otherwise.

### Scoring criteria

The deck explicitly says scoring focuses on:

- Correctness: whether the Python script produces the expected output.
- Speed of execution: how fast the code runs.
- Originality: no plagiarism; similarity against earlier submissions is checked.
- Early submission: earlier submissions are preferred.

### Email commands documented in the deck

#### 1. Check registration

- Subject: `Check If I am Registered`
- Email body: empty
- Notes:
  - Subject is case-insensitive.
  - Spaces are flexible.
  - If registered, the system replies that you are already registered.
  - If not registered, there may be no reply.
  - The deck warns to check spam.

#### 2. Change nickname

- Subject: `Change Nickname to 'YOURNICKNAME'`
- Email body: empty
- Notes:
  - Subject is case-insensitive.
  - Spaces are flexible.
  - Nicknames may contain only alphanumeric characters, underscore, and dash.
  - If successful, the system confirms the nickname change.
  - If failed, the system sends a failure message.
  - The deck warns to check spam.

#### 3. Check score

- The deck tells participants to use DQLab’s leaderboard.
- Immediate results can be checked there.
- Official results come later after review.

#### 4. Request task

- Subject: `Request Task`
- Email body: empty
- Response:
  - The task detail and description are sent back.
  - One or several Excel files may be included.

#### 5. File complaint

- Subject: `File Complaint`
- Email body: complaint or critique message
- Attachments: allowed, including screenshots or files
- Response:
  - The system confirms the complaint has been received.

#### 6. Submit task

- The deck says submission will be instructed in the task.
- The response shown on the slide is: `Score`.

## What the transcript adds

The meeting transcript mostly reinforces the deck and adds operational context.

### Transcript-backed interpretation with medium confidence

- The 7 AM to 10 AM window on 9 May 2026 is for system checking, not the 24-hour competition itself.
- The 24-hour clock starts at 10:00 AM on 9 May 2026 and ends at 10:00 AM on 10 May 2026.
- Around 3,000 participants were mentioned in chat.
- The session included a shared presentation link and follow-up operational notes.

### Transcript-only questions that were raised but not clearly answered in the deck

These topics came up in chat, but the deck does not definitively resolve them:

- Required file format: `.py`, `.ipynb`, or both.
- Whether Google Colab is allowed.
- Whether submissions should be zipped.
- Whether any text insights should be included inside the code file.
- Whether only one file should be submitted or multiple files are allowed.
- Whether AI tools are allowed and how originality is evaluated in practice.
- Whether visual output must match an expected template exactly or can be improved creatively.
- Whether the task will be notebook-based or script-based.

## Confidence Map

### High confidence

These items are directly stated in the slide text.

- Event branding and purpose.
- Participation limited to already-registered DQLab members.
- 9 May 2026 schedule and 24-hour duration.
- Email-driven interaction model.
- Submission address.
- 5-minute email cooldown.
- The six documented email commands.
- The four scoring criteria.
- The registration-check command works in the live system and returns a confirmation reply for a registered participant.

### Medium confidence

These items are strongly supported by the transcript, but not as explicit in the slide text.

- The 7 AM to 10 AM window is for system testing.
- The hackathon starts at 10:00 AM and ends at 10:00 AM the next day.
- The event had roughly 3,000 participants.

### Low confidence

These items remain unconfirmed in the deck.

- Exact submission file format.
- Notebook versus script requirement.
- Colab support.
- Zip packaging requirement.
- Whether insights should be embedded as text.
- Whether AI use is permitted.
- Detailed weighting of the scoring rubric.
- Whether additional post-hackathon presentation or mentorship steps exist.

## Practical Takeaways

- Treat the event as an email-automated Python scoring system, not a general file-upload challenge.
- Optimize for a correct, fast, original solution first.
- Keep submissions simple; the deck emphasizes execution speed and originality, so avoid unnecessary complexity.
- Respect the 5-minute email rate limit during testing and submission.
- Use the leaderboard for rapid feedback, but do not assume it is the final official result.
- Use the leaderboard title as the current public label: Hackathon Python Retail Crisis & Recovery - May 2026.

## Open Questions To Confirm Before Building

Before implementation, the following should be confirmed from the organizers or task release:

- Final submission format.
- Allowed libraries and tooling.
- Whether a notebook or plain Python script is expected.
- Whether a single file, multiple files, or a zip archive is required.
- Whether explanatory text inside code files affects scoring.
- Whether the leaderboard score is final or only provisional.

## Suggested Repo Usage

This document is suitable as the main reference for planning the hackathon solution. If more official task instructions arrive later, they should be appended here or linked from a follow-up report under the same date-stamped folder.
