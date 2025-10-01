
"""Small example: print several variables with types and formatting.

This file is a sample daily snippet. Use `generate_daily.py` to create
date-stamped daily snippets in the `daily/` folder automatically.
"""

from datetime import datetime


def demo_print_variables():
	name = "Alice"
	age = 30
	balance = 1234.5678
	tags = ["python", "daily", "snippet"]

	print(f"Name: {name} (type: {type(name).__name__})")
	print(f"Age: {age} (type: {type(age).__name__})")
	print(f"Balance: ${balance:,.2f} (type: {type(balance).__name__})")
	print(f"Tags: {', '.join(tags)} (type: {type(tags).__name__})")


if __name__ == "__main__":
	print(f"Running sample snippet at {datetime.now().isoformat()}")
	demo_print_variables()
