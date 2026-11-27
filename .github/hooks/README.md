# Optional academic quality-check hooks

These are opt-in examples, not active Git hooks or editor integrations. They flag an explicit unresolved-citation marker in Markdown/BibTeX; they do not prove that citations are valid or that a bibliography follows a particular style.

## Pre-commit example

Review `pre-commit.example.sh`, then install it as a local Git hook if desired:

```sh
cp .github/hooks/pre-commit.example.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Git does not track files under `.git/hooks`. Re-run the copy command after changing the example. For a team-wide hook manager, adopt one separately and configure it to invoke the same check.

## Post-edit example

Run `bash .github/hooks/post-edit.example.sh path/to/edited-file.md` from an editor task or local automation. Configure your editor's post-edit event to invoke it only after confirming the event's command and argument format.

Both checks intentionally fail on `[CITATION NEEDED]` or `[TODO: cite]`. They do not retrieve or validate references, and they make no network requests.
