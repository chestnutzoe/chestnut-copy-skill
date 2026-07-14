---
name: chestnut-copy-sop
description: >-
  Use when a Chinese creator wants to write, rewrite, evaluate, or adapt copy
  with Zoe/Chestnut's copywriting method. Also use to review an existing
  script, transcript, or draft before filming or publishing: diagnose what
  attracts viewers, topic and audience risks, cover/title/hook alignment,
  retention risks, off-voice lines, and precise edits without rewriting for
  the sake of rewriting.
---

# 爆款文案 SOP

## Purpose

This skill packages Zoe/Chestnut's copy production method for public users.

It answers one question:

> 这篇内容有没有传播力？

It can run alone, but works best with a user-specific `文风说明.md` from the `文风分析` skill.

## How It Connects

The full Chestnut Copy skill set has three independent skills:

1. 文风分析: use the creator's own writing samples to answer `像不像你`.
2. 爆款文案 SOP: use this method to answer `有没有传播力`.
3. 公众号发布: send an approved draft to the WeChat draft box.

If a `文风说明.md` exists, load it before drafting. If not, ask whether the user wants to provide samples or continue with the SOP only.

## Required Reference

Read `references/chestnut-copy-sop.md` when writing, rewriting, evaluating, or adapting copy.

That file contains the detailed workflow:

- create mode vs review mode,
- topic gate,
- audience insight,
- pain-point sorting,
- structure,
- outline,
- human texture gate,
- drafting,
- cover/title/hook decision gate,
- retention gate,
- self-edit,
- output package,
- platform adaptation,
- anti-AI checks.

## Core Rules

- When the user provides a script, transcript, or draft for feedback, enter **Review Mode**. Diagnose before rewriting.
- In Review Mode, identify what must be preserved before suggesting what should change.
- Prefer targeted, sentence-level edits. Do not rewrite for the sake of rewriting.
- Do not jump straight to final copy when the angle is weak.
- Do not let the user skip cover/title/hook decisions; this is where many creators lose reach.
- Do not fabricate personal stories.
- Keep the user's point of view, lived scenes, and final judgment visible.
- Keep voice and layout separate.
- When the content may become video or short-form, include a retention scan.
- Never silently skip the next workflow stage. End with the current stage and one concrete next-step reminder.

## Operating Modes

Choose one mode from the user's material and request:

- **Create Mode**: the user has an idea, fragment, voice note, or blank page and wants to develop content.
- **Review Mode**: the user has a script, transcript, or draft and wants feedback, diagnosis, proofreading, or precise improvement.

In Review Mode, use this fixed order:

1. strongest audience pull,
2. topic and audience risk,
3. cover/title/hook diagnosis,
4. retention diagnosis,
5. what must be preserved,
6. priority edits with specific replacement lines,
7. current stage and next-step reminder.

Do not output a full rewrite unless the user asks for one or the diagnosed structure cannot be repaired locally.

## Default Output Package

When the user asks for a publishable package, provide only what the task needs, choosing from:

- topic verdict: `WRITE`, `PIVOT`, or `KILL`,
- audience insight,
- stronger angle options,
- outline,
- final mother draft,
- 3 cover/title/hook combinations,
- selected or recommended combo,
- retention risk and fixes,
- 3 digest or summary options,
- platform adaptation notes,
- publishing checklist.

## Cover / Title / Hook Gate

Always force a real decision when preparing publishable copy.

Create 3 combinations. Each combination must include:

- cover phrase,
- title,
- hook,
- main mechanism,
- best use,
- risk.

Before creating combinations, choose the psychological starting mechanism: pain recognition, curiosity gap, risk warning, contrarian belief, desired result, vulnerability, identity call-out, or another justified mechanism.

If using pain recognition, first test whether this is the audience's most urgent and actionable pain for this topic. Do not choose a pain merely because it is easy to phrase. Compare plausible pains and explain why the selected one has the strongest stopping power.

Then ask:

```text
你要选哪一组？如果不确定，我会默认推荐第 X 组，因为它最适合当前内容目标。
```

## Retention Gate

When the draft may become video or short-form content, include:

- retention risk: high / medium / low,
- predicted drop point,
- cold-viewer comprehension risk,
- problem-chain vs list-like progression,
- mainline overload or removable branches,
- active narrative pulls,
- missing narrative pulls,
- 3 concrete fixes.

## Workflow Completion Reminder

At the end of Create Mode or Review Mode, show only the stages relevant to the task:

```text
当前进度：
✓ / □ 内容角度
✓ / □ 逐字稿或母稿
✓ / □ 标题 / 封面 / Hook
✓ / □ 发布前数据预检
□ 发布后数据复盘
```

Then give one next action. Do not dump every possible next step on the user.

## Publishing Boundary

This skill can prepare a WeChat-ready mother draft, title, digest, and cover direction. It does not upload drafts by itself.

If the user wants to upload to WeChat, hand off to `公众号发布`.
