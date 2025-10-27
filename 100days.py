#!/usr/bin/env python3
"""
100 Days of Code - Local CLI Tool
Quick commands to manage your daily coding workflow
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

# Load the helper module dynamically
script_path = Path(__file__).parent / '.github' / 'scripts' / '100days_helper.py'
spec = importlib.util.spec_from_file_location("days_helper", script_path)
days_helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(days_helper)
HundredDaysHelper = days_helper.HundredDaysHelper


def print_banner():
    """Print welcome banner"""
    print("""
╔══════════════════════════════════════════════╗
║     100 DAYS OF PYTHON - Workflow Manager    ║
╚══════════════════════════════════════════════╝
""")


def show_help():
    """Show help message"""
    print_banner()
    print("""
Usage: python 100days.py <command> [options]

Commands:
  start          Start a new day (auto-detects next project)
  start N        Start day N (specific project number)
  build          Build current project with AI (auto-implements code)
  build N        Build specific project N with AI
  test           Run tests for current project
  test N         Run tests for specific project N
  complete       Complete current day and prepare PR
  status         Show current progress
  list           List all projects
  help           Show this help message

Examples:
  python 100days.py start          # Start next project
  python 100days.py start 5        # Start project #5
  python 100days.py build          # Auto-build current project
  python 100days.py test           # Run tests
  python 100days.py complete       # Mark current project as done
  python 100days.py status         # See your progress

Workflow (Manual):
  1. Run 'start' to begin a new day
  2. Code your project manually
  3. Run 'test' to verify
  4. Run 'complete' when done

Workflow (Automated):
  1. Run 'start' to begin a new day
  2. Run 'build' to auto-generate code with AI
  3. Run 'test' to verify
  4. Run 'complete' when done
""")


def show_status():
    """Show current progress"""
    helper = HundredDaysHelper()
    helper.parse_tracking_file()

    print_banner()
    print(f"📊 Progress: {helper.completed_count}/100 projects completed\n")

    # Show last 3 completed
    completed = [p for p in helper.projects if p.is_completed()]
    if completed:
        print("✅ Recently Completed:")
        for project in completed[-3:]:
            print(f"   Day {project.number}: {project.name}")
        print()

    # Show next 5 upcoming
    upcoming = [p for p in helper.projects if not p.is_completed()][:5]
    if upcoming:
        print("📋 Next Up:")
        for project in upcoming:
            print(f"   Day {project.number}: {project.name}")
        print()

    # Show current branch
    try:
        result = subprocess.run(['git', 'branch', '--show-current'],
                                capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        if current_branch and current_branch != 'main':
            print(f"🌿 Current branch: {current_branch}")
    except:
        pass


def list_projects():
    """List all projects"""
    helper = HundredDaysHelper()
    helper.parse_tracking_file()

    print_banner()
    print("All Projects:\n")

    current_level = None
    for project in helper.projects:
        # Determine difficulty level
        if project.number <= 10:
            level = "Beginner"
        elif project.number <= 20:
            level = "Intermediate"
        else:
            level = "Advanced"

        if level != current_level:
            current_level = level
            print(f"\n{level} Level:")
            print("-" * 50)

        status_icon = "✅" if project.is_completed() else "⬜"
        print(f"{status_icon} Day {project.number:2d}: {project.name}")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    helper = HundredDaysHelper()

    try:
        if command in ['help', '-h', '--help']:
            show_help()

        elif command == 'status':
            show_status()

        elif command == 'list':
            list_projects()

        elif command == 'start':
            project_num = int(sys.argv[2]) if len(sys.argv) > 2 else None
            print_banner()
            project, branch = helper.start_day(project_num)
            print(f"\n💡 Tip: Run 'python 100days.py complete' when you're done!")

        elif command == 'build':
            project_num = int(sys.argv[2]) if len(sys.argv) > 2 else None
            print_banner()

            # Run AI project builder
            if not project_num:
                # Get current project from branch
                result = subprocess.run(['git', 'branch', '--show-current'],
                                      capture_output=True, text=True)
                branch = result.stdout.strip()
                import re
                match = re.match(r'day-(\d+)-', branch)
                if match:
                    project_num = int(match.group(1))
                else:
                    print("❌ Could not detect project number. Please specify: python 100days.py build N")
                    sys.exit(1)

            print(f"🤖 Building project {project_num} with AI...")

            # Build project structure
            result = subprocess.run(['python', '.github/scripts/ai_project_builder.py', 'build', str(project_num)])
            if result.returncode != 0:
                print("❌ Failed to build project structure")
                sys.exit(1)

            # Auto-implement with AI
            import json
            with open('.github/data/project-specs.json', 'r') as f:
                data = json.load(f)
                project_dir = None
                for proj in data['projects']:
                    if proj['id'] == project_num:
                        project_dir = proj['directory']
                        break

            if project_dir:
                result = subprocess.run(['python', '.github/scripts/claude_builder.py', project_dir])
                if result.returncode == 0:
                    print(f"\n✅ Project built successfully!")
                    print(f"💡 Next: Run 'python 100days.py test' to verify")
                else:
                    print("⚠️  Build completed with issues. Check the output above.")

        elif command == 'test':
            project_num = int(sys.argv[2]) if len(sys.argv) > 2 else None
            print_banner()

            if not project_num:
                # Get current project from branch
                result = subprocess.run(['git', 'branch', '--show-current'],
                                      capture_output=True, text=True)
                branch = result.stdout.strip()
                import re
                match = re.match(r'day-(\d+)-', branch)
                if match:
                    project_num = int(match.group(1))

            if not project_num:
                print("❌ Could not detect project number. Please specify: python 100days.py test N")
                sys.exit(1)

            print(f"🧪 Running tests for project {project_num}...")
            result = subprocess.run(['python', '.github/scripts/ai_project_builder.py', 'test', str(project_num)])

            if result.returncode == 0:
                print(f"\n✅ All tests passed!")
                print(f"💡 Next: Run 'python 100days.py complete' to finish")
            else:
                print(f"\n❌ Tests failed. Fix issues and try again.")
                sys.exit(1)

        elif command == 'complete':
            project_num = int(sys.argv[2]) if len(sys.argv) > 2 else None
            print_banner()
            project, branch = helper.complete_day(project_num)
            print(f"\n💡 Next steps:")
            print(f"   1. Review your changes")
            print(f"   2. Create PR: gh pr create --fill")
            print(f"   3. Or use GitHub Actions workflow")

        else:
            print(f"❌ Unknown command: {command}")
            print("Run 'python 100days.py help' for usage information")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
