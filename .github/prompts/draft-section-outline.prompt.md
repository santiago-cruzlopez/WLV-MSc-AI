---
name: Draft dissertation section outline
description: Create a source-aware outline for a dissertation section.
---

Create a structured outline for the following dissertation section.

**Chapter/section:** ${input:section:Name the chapter or section}
**Research question or objective:** ${input:question:State the relevant question/objective}
**Available evidence and sources:** ${input:evidence:List source files, notes, or findings to use}
**Required length or rubric constraints:** ${input:constraints:Provide constraints or write "not specified"}

Use the repository's global and path-specific instructions. Return:

1. A proposed heading hierarchy with the purpose of each subsection.
2. The logical progression of claims and how each supports the section's purpose.
3. Evidence needed for each substantive claim, using only the supplied material.
4. Gaps, assumptions, and items to verify before drafting.

Do not invent findings, citations, or source details. Mark unsupported content as an explicit evidence need.
