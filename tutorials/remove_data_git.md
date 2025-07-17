---
title: "Removing Sensitive Data from Git"
---

## Removing sensitive data from git

**This doc is a WIP and needs to be cleaned up**

Every time I do this it’s kind of an ordeal (and there’s a few different tools). Here’s what I did last time — could maybe be added to Clinic docs or wherever this sort of thing belongs.

Ok, this is always a nightmare but here's how you use the [BFG repo cleaner](https://rtyley.github.io/bfg-repo-cleaner/):

- First, make sure that you have a copy of the current repo that you've pulled all changes to
- **Do all of the file cleaning from a fresh clone of the repo**

```jsx
git clone --mirror https://github.com/your/repo
```

- It's actually really helpful to delete all of the sensitive files **first** since it gets weird if you try to delete them after doing the repo cleaning
    - Do another fresh clone of the repo (not a mirror so you can actually manipulate the files)
    - The BFG repo cleaner leaves them in the HEAD (which kind of makes sense…prevents breaking changes) but things go awry when you try to push the cleaned history to GitHub then merge with other branches...and you end up doing a lot of back and forth, merge conflicts with ghost files, etc.
    - **Merge the deletion of the files into the main branch also**
- Now we're ready to clean the history. cd into the *mirrored directory* and run this (for example, to delete .csv files)

```jsx
java -jar ~/bfg-1.14.0.jar --delete-files '*.csv'
```

- Run the reflog command it tells you to run to clean the commit history
- Then do git push --force
    - If this fails with a "hung up unexpectedly" error, it's probably because you need to increase the buffer for the large amount of information you're pushing

```jsx
git config http.postBuffer 524288000
```

- If you have branch protections enabled, you will run into problems. You will need to disable branch protections in order to clean the history correctly.

```jsx
! [remote rejected] dev -> dev (protected branch hook declined)
```

- If successful, you should see something like this:

```jsx
+ 74bca8b...eff0c7b dev -> dev (forced update)
+ 74bca8b...307119b main -> main (forced update)
```

- Note: You can still find "orphaned" commits by clicking on pull requests and finding the commit id. These orphaned commits will have sensitive files in them. If it's really important that the data be removed, you can reach out to GitHub support or create a new repo and push the cleaned history there.
- Anyone else who was using the repo should re-clone from the cleaned repo history
    - If there are any branches in progress that branched off from the history with sensitive files, those branches should be **rebased** — merging will probably reintroduce the sensitive files