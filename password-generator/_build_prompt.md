# Project Build Request: Password generator

## Project Overview
**Type:** CLI
**Difficulty:** Easy
**Directory:** password-generator

Generate secure random passwords with customizable options

## Requirements
1. Generate passwords with specified length
2. Include uppercase, lowercase, numbers, and special characters
3. Allow users to choose character types to include
4. Display password strength indicator
5. Option to generate multiple passwords at once
6. Copy to clipboard functionality (optional)

## Additional Features
- Password strength meter
- Memorable password option (using words)
- Exclude ambiguous characters option
- Save to file

## Tech Stack
- Python 3.8+
- random module
- string module

## Test Cases to Implement
- Test password length validation
- Test character type inclusion
- Test password uniqueness
- Test strength calculation

## Implementation Instructions

Please create a COMPLETE, PRODUCTION-READY implementation with:

### File Structure
Create in directory: `password-generator/`
- `main.py` - Main application entry point
- `README.md` - Project documentation with usage instructions
- `requirements.txt` - All dependencies
- `tests/test_main.py` - Unit tests using pytest
- `.gitignore` - Python gitignore

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
