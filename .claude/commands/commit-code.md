---
name: commit-code
description: Safely commit and push code changes with build verification. Use when the user wants to commit code, push changes, save work to git, or says "commit", "push", "save to git", or "commit my changes". Runs frontend build first, fixes errors, then commits frontend and backend separately with descriptive messages. If prettier or ruff have formatted the code, simply add again and provide the same commit message.
---
# Commit Code Workflow

Execute these steps in order. Do not skip steps.

## Step 1: Build Frontend

Check current directory:

```bash
pwd
```

Check file changes:

```bash
git status
```

If there are no changes in frontend/, skip building.

Otherwise:

```bash
cd frontend && pnpm build
```

If build fails:

1. Read error messages carefully
2. Fix each error in the source files
3. Re-run build until it passes
4. Do not proceed until build succeeds

## Step 2: Check for Changes

```bash
git status
```

Identify changes in:

- `frontend/` directory → frontend changes
- Everything else → backend changes

If no changes exist, inform user and stop.

## Step 3: Commit Frontend Changes

Only if frontend changes exist:

```bash
git add frontend/
git commit -m "<type>(<scope>): <issue summary>

Issue: <detailed description of what was wrong>
Fix: <explanation of how it was resolved>"
```

## Step 4: Commit Backend Changes

Only if backend changes exist:

```bash
git add .
git commit -m "<type>(<scope>): <issue summary>

Issue: <detailed description of what was wrong>
Fix: <explanation of how it was resolved>"
```

## Commit Message Format

Each commit message MUST have two parts:

### Part 1: Header Line

`<type>(<scope>): <brief issue summary>`

- **type**: feat, fix, refactor, style, docs, test, chore
- **scope**: component or feature name
- **summary**: brief description of the issue, in imperative mood

### Part 2: Body (Required)

```
Issue: <describe what was broken, missing, or needed improvement>
Fix: <describe the solution and how it resolves the issue>
```

### Examples

**Example 1 - Bug fix:**

``` text
fix(auth): resolve login failure for SSO users

Issue: Users authenticating via SSO were receiving a 401 error because the token validation was checking for a password hash that doesn't exist for SSO accounts.
Fix: Added a conditional check to skip password hash validation when the user's auth_type is 'sso', and instead validate the OAuth token directly.
```

**Example 2 - Feature:**

``` text
feat(dashboard): add real-time notification counter

Issue: Users had no way to see new notifications without manually refreshing the page, leading to missed alerts.
Fix: Implemented a WebSocket connection that listens for notification events and updates a badge counter in the header component in real-time.
```

**Example 3 - Refactor:**

``` text
refactor(api): consolidate duplicate validation logic

Issue: Input validation was duplicated across 5 different endpoint handlers, making maintenance error-prone and inconsistent.
Fix: Extracted validation rules into a shared middleware function and applied it to all relevant routes.
```

## Step 5: Push to Remote

```bash
git push
```

If push fails due to remote changes:

```bash
git pull --rebase && git push
```

## Summary Template

After completion, report:

- Build status: ✓ passed
- Frontend commit: `<message>` (N files)
  - Issue: <brief issue description>
  - Fix: <brief fix description>
- Backend commit: `<message>` (N files)
  - Issue: <brief issue description>
  - Fix: <brief fix description>
- Push: ✓ successful
