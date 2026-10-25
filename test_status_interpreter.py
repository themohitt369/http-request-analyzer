
from modules.status_interpreter import StatusCodeInterpreter


interpreter = StatusCodeInterpreter()

test_cases = [
    (200, "Success"),
    (301, "Redirection"),
    (404, "Client Error"),
    (429, "Client Error"),
    (500, "Server Error"),
    (503, "Server Error"),
    (418, "Client Error"),  # Valid but not in our built-in dictionary.
]

for code, expected_category in test_cases:
    result = interpreter.interpret(code)

    print(f"\nStatus: {result['status_code']}")
    print(f"Phrase: {result['phrase']}")
    print(f"Category: {result['category']}")
    print(f"Meaning: {result['meaning']}")
    print(f"Guidance: {result['guidance']}")

    assert result["category"] == expected_category

    if code == 418:
        assert result["phrase"] == "Unknown or unlisted status"

# Invalid input checks
for invalid_code in [99, 600, "404", True]:
    try:
        interpreter.interpret(invalid_code)
    except ValueError:
        print(f"\nCorrectly rejected invalid input: {invalid_code!r}")
    else:
        raise AssertionError(
            f"Expected ValueError for {invalid_code!r}"
        )

print("\nAll status interpreter tests passed.")
