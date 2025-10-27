#!/usr/bin/env python3
"""
AI-Powered Project Builder for 100 Days of Code
Automatically generates complete projects based on specifications
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Optional


class AIProjectBuilder:
    def __init__(self, specs_file: str = ".github/data/project-specs.json"):
        self.specs_file = Path(specs_file)
        self.specs = {}
        self.load_specs()

    def load_specs(self):
        """Load project specifications from JSON file"""
        if not self.specs_file.exists():
            raise FileNotFoundError(f"Specs file not found: {self.specs_file}")

        with open(self.specs_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.specs = {proj['id']: proj for proj in data['projects']}

    def get_project_spec(self, project_id: int) -> Optional[Dict]:
        """Get specification for a specific project"""
        return self.specs.get(project_id)

    def generate_project_prompt(self, spec: Dict) -> str:
        """Generate a detailed prompt for AI to build the project"""

        prompt = f"""# Project Build Request: {spec['name']}

## Project Overview
**Type:** {spec['type']}
**Difficulty:** {spec['difficulty']}
**Directory:** {spec['directory']}

{spec['description']}

## Requirements
"""
        for i, req in enumerate(spec['requirements'], 1):
            prompt += f"{i}. {req}\n"

        prompt += f"\n## Additional Features\n"
        for feature in spec['features']:
            prompt += f"- {feature}\n"

        prompt += f"\n## Tech Stack\n"
        for tech in spec['tech_stack']:
            prompt += f"- {tech}\n"

        prompt += f"""
## Test Cases to Implement
"""
        for test in spec['test_cases']:
            prompt += f"- {test}\n"

        prompt += f"""
## Implementation Instructions

Please create a COMPLETE, PRODUCTION-READY implementation with:

### File Structure
Create in directory: `{spec['directory']}/`
- `main.py` - Main application entry point
- `README.md` - Project documentation with usage instructions
- `requirements.txt` - All dependencies
- `tests/test_main.py` - Unit tests using pytest
- `.gitignore` - Python gitignore
"""

        if spec['type'] == 'GUI' or spec['type'] == 'CLI + GUI':
            prompt += "- `gui.py` - GUI implementation (if applicable)\n"

        prompt += """
### Code Quality Requirements
1. **Clean Code**: Follow PEP 8 style guide
2. **Documentation**: Add docstrings to all functions and classes
3. **Error Handling**: Proper try-except blocks for user input and file operations
4. **Type Hints**: Use type hints for function parameters and returns
5. **Comments**: Explain complex logic
6. **Modular**: Separate concerns into different functions/classes

### Testing Requirements
1. Write pytest unit tests covering all major functionality
2. Test edge cases and error conditions
3. Aim for >80% code coverage

### README Requirements
Include:
- Project description
- Features list
- Installation instructions
- Usage examples with screenshots/examples
- Requirements
- How to run tests

### Additional Notes
- Make the code beginner-friendly but professional
- Include example usage in main.py (if __name__ == "__main__")
- Add helpful comments for learning purposes
- Ensure all features from requirements are implemented

Please implement this project completely and professionally. Create all files with working code.
"""
        return prompt

    def create_project_structure(self, spec: Dict) -> Path:
        """Create basic project directory structure"""
        project_dir = Path(spec['directory'])
        project_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (project_dir / 'tests').mkdir(exist_ok=True)

        return project_dir

    def generate_basic_files(self, spec: Dict, project_dir: Path):
        """Generate basic boilerplate files"""

        # .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Tests
.pytest_cache/
.coverage
htmlcov/
"""
        (project_dir / '.gitignore').write_text(gitignore_content)

        # requirements.txt placeholder
        requirements = """# Project dependencies
# Add your dependencies here
"""
        if 'tkinter' in str(spec.get('tech_stack', [])):
            requirements += "# tkinter (usually comes with Python)\n"
        if 'matplotlib' in str(spec.get('tech_stack', [])):
            requirements += "matplotlib>=3.5.0\n"
        if 'pandas' in str(spec.get('tech_stack', [])):
            requirements += "pandas>=1.3.0\n"

        requirements += "\n# Testing\npytest>=7.0.0\npytest-cov>=3.0.0\n"

        (project_dir / 'requirements.txt').write_text(requirements)

        print(f"✅ Created basic project structure in {project_dir}")

    def build_project_with_ai(self, project_id: int):
        """Main method to build a project using AI assistance"""

        spec = self.get_project_spec(project_id)
        if not spec:
            print(f"❌ No specification found for project {project_id}")
            print(f"📋 Available projects: {list(self.specs.keys())}")
            return False

        print(f"\n🤖 Building Project {project_id}: {spec['name']}")
        print(f"📂 Directory: {spec['directory']}")
        print(f"📊 Difficulty: {spec['difficulty']}")

        # Create project structure
        project_dir = self.create_project_structure(spec)
        self.generate_basic_files(spec, project_dir)

        # Generate AI prompt
        ai_prompt = self.generate_project_prompt(spec)

        # Save prompt to file for reference
        prompt_file = project_dir / '_build_prompt.md'
        prompt_file.write_text(ai_prompt)
        print(f"📝 Build prompt saved to: {prompt_file}")

        # Save spec to project directory for reference
        spec_file = project_dir / '_project_spec.json'
        with open(spec_file, 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2)

        print(f"\n✅ Project structure created!")
        print(f"\n{'='*60}")
        print(f"🎯 NEXT STEP: AI Implementation Required")
        print(f"{'='*60}")
        print(f"\nThe AI prompt has been generated at:")
        print(f"  {prompt_file}")
        print(f"\nTo complete this project, run the AI builder workflow")
        print(f"or manually implement using the prompt as a guide.")
        print(f"{'='*60}\n")

        return True

    def run_tests(self, project_dir: Path) -> bool:
        """Run tests for the project"""
        test_dir = project_dir / 'tests'
        if not test_dir.exists():
            print(f"⚠️  No tests directory found in {project_dir}")
            return False

        print(f"\n🧪 Running tests for {project_dir.name}...")

        try:
            result = subprocess.run(
                ['pytest', str(test_dir), '-v', '--cov=' + str(project_dir)],
                capture_output=True,
                text=True,
                cwd=project_dir.parent
            )

            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            if result.returncode == 0:
                print(f"✅ All tests passed!")
                return True
            else:
                print(f"❌ Some tests failed")
                return False

        except FileNotFoundError:
            print("⚠️  pytest not installed. Install with: pip install pytest pytest-cov")
            return False


def main():
    if len(sys.argv) < 3:
        print("""
Usage: python ai_project_builder.py <command> <project_id>

Commands:
  build <id>    - Build project structure and generate AI prompt
  test <id>     - Run tests for project

Examples:
  python ai_project_builder.py build 5
  python ai_project_builder.py test 5
""")
        sys.exit(1)

    command = sys.argv[1]
    project_id = int(sys.argv[2])

    builder = AIProjectBuilder()

    if command == 'build':
        success = builder.build_project_with_ai(project_id)
        sys.exit(0 if success else 1)

    elif command == 'test':
        spec = builder.get_project_spec(project_id)
        if spec:
            project_dir = Path(spec['directory'])
            success = builder.run_tests(project_dir)
            sys.exit(0 if success else 1)
        else:
            print(f"❌ Project {project_id} not found")
            sys.exit(1)

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
