#!/usr/bin/env python3
"""
100 Days of Code Helper Script
Automates branch creation, tracking updates, and PR management
"""

import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


class Project:
    def __init__(self, number: int, name: str, status: str, directory: str = None):
        self.number = number
        self.name = name
        self.status = status
        self.directory = directory or f"/{self.name.lower().replace(' ', '-')}"

    def is_completed(self) -> bool:
        return self.status.lower() == "completed" or "[x]" in self.status

    def to_branch_name(self) -> str:
        """Convert project name to git branch format"""
        clean_name = re.sub(r'[^\w\s-]', '', self.name)
        clean_name = clean_name.lower().replace(' ', '-')
        return f"day-{self.number:02d}-{clean_name}"


class HundredDaysHelper:
    def __init__(self, tracking_file: str = "100days_of_python.md"):
        self.tracking_file = Path(tracking_file)
        self.projects = []
        self.completed_count = 0
        self.current_day = 0

    def parse_tracking_file(self) -> None:
        """Parse the 100 days markdown file to extract projects"""
        if not self.tracking_file.exists():
            raise FileNotFoundError(f"Tracking file not found: {self.tracking_file}")

        content = self.tracking_file.read_text(encoding='utf-8')

        # Parse progress tracking
        progress_match = re.search(r'Projects Completed:\s*(\d+)/100', content)
        if progress_match:
            self.completed_count = int(progress_match.group(1))

        # Parse projects - matches numbered list items
        project_pattern = r'^(\d+)\.\s+\[(.)\]\s+(.+?)(?:\n|$)'
        matches = re.finditer(project_pattern, content, re.MULTILINE)

        for match in matches:
            number = int(match.group(1))
            checkbox = match.group(2)
            name = match.group(3).strip()

            # Clean up the project name
            name = name.split('(')[0].strip()  # Remove parenthetical info

            status = "Completed" if checkbox.lower() == 'x' else "Not Started"

            # Try to find directory info
            directory = None
            project_section_start = match.end()
            project_section = content[project_section_start:project_section_start + 500]
            dir_match = re.search(r'Directory:\s*`?([^`\n]+)`?', project_section)
            if dir_match:
                directory = dir_match.group(1)

            self.projects.append(Project(number, name, status, directory))

    def get_next_project(self, project_number: Optional[int] = None) -> Optional[Project]:
        """Get the next uncompleted project or a specific project by number"""
        if project_number:
            for project in self.projects:
                if project.number == project_number:
                    return project
            return None

        # Find first uncompleted project
        for project in self.projects:
            if not project.is_completed():
                return project
        return None

    def update_progress(self, project: Project, mark_complete: bool = False) -> None:
        """Update the tracking file with new progress"""
        content = self.tracking_file.read_text(encoding='utf-8')

        # Update project status
        if mark_complete:
            # Find the project line and mark it as complete
            pattern = f"^{project.number}\\. \\[ \\] {re.escape(project.name)}"
            replacement = f"{project.number}. [x] {project.name}"
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            # Update completed count
            new_completed = self.completed_count + 1
            content = re.sub(
                r'Projects Completed:\s*\d+/100',
                f'Projects Completed: {new_completed}/100',
                content
            )

            # Update days completed
            content = re.sub(
                r'Days Completed:\s*\d+/100',
                f'Days Completed: {new_completed}/100',
                content
            )

        # Update current project
        content = re.sub(
            r'Current Project:.*',
            f'Current Project: {project.name}',
            content
        )

        self.tracking_file.write_text(content, encoding='utf-8')

    def create_branch(self, project: Project) -> str:
        """Create and checkout a new branch for the project"""
        branch_name = project.to_branch_name()

        try:
            # Create and checkout new branch
            subprocess.run(['git', 'checkout', '-b', branch_name], check=True, capture_output=True)
            print(f"Created and checked out branch: {branch_name}")
            return branch_name
        except subprocess.CalledProcessError as e:
            # Branch might already exist, try to checkout
            try:
                subprocess.run(['git', 'checkout', branch_name], check=True, capture_output=True)
                print(f"Checked out existing branch: {branch_name}")
                return branch_name
            except subprocess.CalledProcessError:
                raise Exception(f"Failed to create or checkout branch: {e}")

    def commit_and_push(self, project: Project, branch_name: str) -> None:
        """Commit changes and push to remote"""
        try:
            # Add all changes
            subprocess.run(['git', 'add', '.'], check=True)

            # Commit with message
            commit_msg = f"feat: complete day {project.number} - {project.name}\n\n✅ Completed {project.name} project"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)

            # Push to remote
            subprocess.run(['git', 'push', '-u', 'origin', branch_name], check=True)

            print(f"Committed and pushed changes to {branch_name}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to commit and push: {e}")

    def start_day(self, project_number: Optional[int] = None) -> Tuple[Project, str]:
        """Start a new day - create branch and update tracking"""
        self.parse_tracking_file()
        project = self.get_next_project(project_number)

        if not project:
            raise Exception("No uncompleted projects found!")

        print(f"\n🚀 Starting Day {project.number}: {project.name}")

        # Create branch
        branch_name = self.create_branch(project)

        # Update tracking file
        self.update_progress(project, mark_complete=False)

        # Commit the tracking update
        try:
            subprocess.run(['git', 'add', str(self.tracking_file)], check=True)
            subprocess.run(['git', 'commit', '-m', f'chore: start day {project.number} - {project.name}'], check=True)
            subprocess.run(['git', 'push', '-u', 'origin', branch_name], check=True)
        except subprocess.CalledProcessError:
            print("Note: No changes to commit for tracking file")

        print(f"✅ Ready to code! Work in branch: {branch_name}")
        print(f"📁 Project directory: {project.directory}")

        return project, branch_name

    def complete_day(self, project_number: Optional[int] = None) -> Tuple[Project, str]:
        """Complete the day - mark project as done, commit, and push"""
        self.parse_tracking_file()

        # Get current branch
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()

        # Parse project number from branch name if not provided
        if not project_number:
            match = re.match(r'day-(\d+)-', current_branch)
            if match:
                project_number = int(match.group(1))

        if not project_number:
            raise Exception("Could not determine project number from branch name")

        project = self.get_next_project(project_number)
        if not project:
            raise Exception(f"Project {project_number} not found!")

        print(f"\n🎉 Completing Day {project.number}: {project.name}")

        # Update tracking file to mark as complete
        self.update_progress(project, mark_complete=True)

        # Commit and push all changes
        self.commit_and_push(project, current_branch)

        print(f"✅ Day {project.number} completed!")
        print(f"🔀 Ready to create PR from branch: {current_branch}")

        # Set GitHub Actions outputs
        print(f"::set-output name=day_number::{project.number}")
        print(f"::set-output name=project_name::{project.name}")
        print(f"::set-output name=branch_name::{current_branch}")
        print(f"::set-output name=project_description::{project.name} - Day {project.number} of 100 Days of Code")

        return project, current_branch


def main():
    if len(sys.argv) < 2:
        print("Usage: python 100days_helper.py <start-day|complete-day> [project_number]")
        sys.exit(1)

    action = sys.argv[1]
    project_number = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else None

    helper = HundredDaysHelper()

    try:
        if action == "start-day":
            helper.start_day(project_number)
        elif action == "complete-day":
            helper.complete_day(project_number)
        else:
            print(f"Unknown action: {action}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
