---
title: 'Text Diff'
description: 'Compare two blocks of text and see additions, removals, and unchanged lines in your browser. No upload, no tracking.'
pubDate: 2025-12-10
category: 'text'
tags: ['diff', 'text', 'productivity']
icon: '🧩'
component: 'TextDiff'
translationKey: 'text-diff'
tldr: 'A privacy-friendly, browser-only text diff tool that highlights added, removed, and unchanged lines instantly.'
faq:
  - q: 'Is my text uploaded anywhere?'
    a: 'No. The comparison runs entirely in your browser using a JavaScript implementation. Closing the tab discards the data.'
  - q: 'How large a text can I compare?'
    a: 'Up to a few hundred thousand characters work smoothly. For larger inputs, split the documents into sections.'
---

## How to use

1. Paste the original text into the left box.
2. Paste the modified text into the right box.
3. The diff appears below in real time. Lines are color-coded.

## Privacy

The tool runs fully client-side. Nothing is uploaded, logged, or shared. Refresh the page and your inputs are gone.

## Tips

- For best results, normalize line endings first (`\n`).
- The diff is line-based, not word-based — keep that in mind when comparing prose.
