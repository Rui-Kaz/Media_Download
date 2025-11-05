# Quick Git Commands Guide

## Initial Setup (First Time Only)

### Configure Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Initialize and Push (Use git_push.bat or manually):
```bash
# Initialize repository
git init

# Add remote
git remote add origin https://github.com/Rui-Kaz/Media_Download.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: Media Download application"

# Push to main branch
git branch -M main
git push -u origin main
```

## Daily Workflow

### Check Status
```bash
git status
```

### Add Changes
```bash
# Add all changes
git add .

# Add specific file
git add saca_videos.py
```

### Commit Changes
```bash
git commit -m "Description of changes"
```

### Push to GitHub
```bash
git push origin main
```

### Pull Latest Changes
```bash
git pull origin main
```

## Branch Management

### Create New Branch
```bash
git checkout -b feature/new-feature
```

### Switch Branch
```bash
git checkout main
```

### Merge Branch
```bash
git checkout main
git merge feature/new-feature
```

### Delete Branch
```bash
git branch -d feature/new-feature
```

## Common Tasks

### View Commit History
```bash
git log
git log --oneline
```

### Undo Changes
```bash
# Undo uncommitted changes
git checkout -- filename

# Undo last commit (keep changes)
git reset HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Create Tag/Release
```bash
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

## Quick Reference

```bash
# Clone repository
git clone https://github.com/Rui-Kaz/Media_Download.git

# Update repository
git pull

# See differences
git diff

# Discard all local changes
git reset --hard origin/main

# Remove file from Git (keep local)
git rm --cached filename
```

## GitHub Workflow

1. Make changes locally
2. `git add .`
3. `git commit -m "message"`
4. `git push origin main`
5. Check GitHub repository

## Tips

- Commit often with clear messages
- Pull before push to avoid conflicts
- Use branches for new features
- Don't commit sensitive data
- Check .gitignore is working
