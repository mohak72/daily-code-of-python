# 100 Days of Code - Automation Guide

Automated workflow for managing your 100 Days of Python coding challenge with automatic branch creation, progress tracking, and PR generation.

## Features

✨ **Automated Daily Workflow**
- Auto-detects next project from your progress
- Creates feature branches automatically (e.g., `day-05-number-guessing-game`)
- Updates progress tracking in `100days_of_python.md`
- Commits and pushes code automatically
- Creates pull requests with formatted descriptions

🎯 **Two Ways to Use**
1. **Local CLI** - Run commands from your terminal
2. **GitHub Actions** - Trigger workflows from GitHub UI

---

## Quick Start

### Option 1: Local CLI (Recommended for Daily Use)

```bash
# Start a new day
python 100days.py start

# Code your project...

# Complete the day
python 100days.py complete

# Check your progress
python 100days.py status
```

### Option 2: GitHub Actions (Remote Automation)

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **100 Days of Code - Automation**
4. Click **Run workflow**
5. Choose action: `start-day` or `complete-day`

---

## Setup Instructions

### Prerequisites

1. **Git** installed and configured
2. **Python 3.8+** installed
3. **GitHub CLI** (optional, for local PR creation)
   ```bash
   # Install GitHub CLI
   # Windows (using winget)
   winget install GitHub.cli

   # Mac (using homebrew)
   brew install gh

   # Linux
   sudo apt install gh  # Debian/Ubuntu
   ```

4. **Git Authentication** configured
   ```bash
   # Configure git if not already done
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

### First Time Setup

1. **Make the scripts executable** (Mac/Linux):
   ```bash
   chmod +x 100days.py
   chmod +x .github/scripts/100days_helper.py
   ```

2. **Test the setup**:
   ```bash
   python 100days.py status
   ```

---

## Local CLI Usage

### Available Commands

```bash
# Show help
python 100days.py help

# Start next project (auto-detected)
python 100days.py start

# Start specific project by number
python 100days.py start 5

# Complete current day
python 100days.py complete

# Show progress
python 100days.py status

# List all projects
python 100days.py list
```

### Daily Workflow

**Morning: Start Your Day**
```bash
# 1. Start new day (creates branch, updates tracking)
python 100days.py start

# Output:
# 🚀 Starting Day 5: Number guessing game
# Created and checked out branch: day-05-number-guessing-game
# ✅ Ready to code! Work in branch: day-05-number-guessing-game
# 📁 Project directory: /number-guessing-game
```

**During the Day: Code Your Project**
- Build your project in the designated directory
- Commit your changes as you go (optional)
- Test your code

**Evening: Complete Your Day**
```bash
# 2. Complete the day (commits all changes, marks complete)
python 100days.py complete

# Output:
# 🎉 Completing Day 5: Number guessing game
# ✅ Day 5 completed!
# 🔀 Ready to create PR from branch: day-05-number-guessing-game
```

**Create Pull Request**
```bash
# Option A: Using GitHub CLI
gh pr create --fill

# Option B: Manually on GitHub
# Push your branch and create PR through GitHub UI

# Option C: Use GitHub Actions workflow
# Go to Actions tab and run "complete-day" workflow
```

---

## GitHub Actions Workflow

### Trigger from GitHub UI

1. Navigate to your repository
2. Click **Actions** tab
3. Select **100 Days of Code - Automation** workflow
4. Click **Run workflow** button
5. Select parameters:
   - **Action**: `start-day` or `complete-day`
   - **Project number**: (optional) Leave empty for auto-detect

### What the Workflow Does

**Start Day Workflow:**
- Checks out your repository
- Finds next uncompleted project
- Creates feature branch
- Updates `100days_of_python.md`
- Pushes branch to remote

**Complete Day Workflow:**
- Commits all your changes
- Marks project as completed
- Pushes changes
- **Auto-creates Pull Request** with:
  - Formatted title: "Day X: Project Name"
  - Template body for learnings and screenshots
  - `100-days-of-code` label

---

## File Structure

```
your-repo/
├── 100days_of_python.md           # Main tracking file
├── 100days.py                      # Local CLI tool
├── 100DAYS_AUTOMATION.md           # This documentation
├── .github/
│   ├── workflows/
│   │   └── 100days-automation.yml  # GitHub Actions workflow
│   └── scripts/
│       └── 100days_helper.py       # Core automation logic
└── [your-project-folders]/
```

---

## Branch Naming Convention

Branches are automatically created with this format:
```
day-{number}-{project-name}
```

Examples:
- `day-05-number-guessing-game`
- `day-12-tic-tac-toe-game`
- `day-21-portfolio-website-with-flask-django`

---

## Tracking File Updates

The automation automatically updates `100days_of_python.md`:

**Progress Section:**
```markdown
## Progress Tracking
- [x] Projects Completed: 5/100
- [x] Current Project: Number guessing game
- [x] Days Completed: 5/100
```

**Project Checkboxes:**
```markdown
5. [x] Number guessing game
   - Status: Completed
   ...
```

---

## Pull Request Template

Auto-generated PRs include:

```markdown
## 100 Days of Code - Day 5

### Project: Number guessing game

**Status:** ✅ Completed

### What I Built
[Project description]

### Key Learnings
- Add your learnings here

### Screenshots/Demo
- Add screenshots or demo links here

---
*Auto-generated PR for 100 Days of Code challenge*
```

---

## Troubleshooting

### Issue: Branch already exists

**Solution:**
```bash
# Delete local branch
git branch -D day-05-number-guessing-game

# Delete remote branch
git push origin --delete day-05-number-guessing-game

# Then try again
python 100days.py start 5
```

### Issue: Script can't find tracking file

**Solution:**
Make sure you're running commands from the repository root directory where `100days_of_python.md` exists.

### Issue: GitHub Actions fails with permission error

**Solution:**
1. Go to repository **Settings**
2. Click **Actions** → **General**
3. Under "Workflow permissions":
   - Select **Read and write permissions**
   - Check **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

### Issue: Git push fails (authentication)

**Solution:**
```bash
# Configure GitHub credentials
gh auth login

# Or use SSH keys
ssh-keygen -t ed25519 -C "your.email@example.com"
# Add the key to GitHub: Settings → SSH Keys
```

---

## Tips for Success

1. **Commit Early and Often** - Don't wait until the end of the day
2. **Write Good Commit Messages** - Describe what you built
3. **Test Before Completing** - Run your code to make sure it works
4. **Document Your Learnings** - Add notes to your PR descriptions
5. **Review Your PRs** - Look over your code before merging
6. **Merge Regularly** - Don't let PRs pile up

---

## Advanced Usage

### Skip to a Specific Project

```bash
# Start day 10 specifically
python 100days.py start 10
```

### Manual Branch Management

```bash
# If you want to manage branches manually
git checkout -b day-05-custom-name

# Use the helper just for tracking
python .github/scripts/100days_helper.py complete-day 5
```

### Customize PR Templates

Edit `.github/workflows/100days-automation.yml` around line 50 to customize the PR body template.

---

## FAQ

**Q: Do I have to create PRs for every project?**
A: No, but it's recommended for tracking progress and building your GitHub portfolio.

**Q: Can I work on multiple days at once?**
A: The automation expects one day at a time, but you can manually create multiple branches.

**Q: What if I want to skip a project?**
A: Manually mark it complete in `100days_of_python.md` by changing `[ ]` to `[x]`.

**Q: Can I use this for other challenge formats?**
A: Yes! Edit `100days_of_python.md` to match your challenge format.

---

## Contributing

Found a bug or want to improve the automation? Feel free to:
1. Fork the repository
2. Make your changes
3. Submit a PR

---

## License

This automation setup is provided as-is for personal use in your 100 Days of Code challenge.

---

**Happy Coding! 🚀**

Keep pushing, keep learning, and most importantly - keep coding every day!
