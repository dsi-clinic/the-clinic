---
title: "WSL Tutorial"
---

### Where are my files?

You should be able to find it from `\\wsl$\`

Never use `%LOCALAPPDATA%` to access wsl files - [[source](https://devblogs.microsoft.com/commandline/do-not-change-linux-files-using-windows-apps-and-tools/)]


### VS Code is acting strange

Check that you are accessing your repository with the Remote - WSL extension. Look for the green box in the bottom left. If it doesn't say WSL, click it and select to reopen in WSL. 

Make sure you cloned your repository inside WSL, not Windows.