
from modules.json_parser import JSONParser


parser = JSONParser()

# Test 1: Valid JSON object
result = parser.parse_text('{"name": "Test", "quantity": 3}')
assert result["success"] is True
assert result["data_type"] == "object"
assert result["item_count"] == 2
print("Test 1 passed: Valid JSON object")

# Test 2: Valid JSON array
result = parser.parse_text('[1, 2, 3]')
assert result["success"] is True
assert result["data_type"] == "array"
assert result["item_count"] == 3
print("Test 2 passed: Valid JSON array")

# Test 3: Invalid JSON
result = parser.parse_text('{"name": }')
assert result["success"] is False
assert result["error_type"] == "JSONDecodeError"
assert result["data"] is None
print("Test 3 passed: Invalid JSON handled")

# Test 4: Empty input
result = parser.parse_text("   ")
assert result["success"] is False
assert result["error_type"] == "EmptyInput"
print("Test 4 passed: Empty input handled")

# Test 5: JSON null
result = parser.parse_text("null")
assert result["success"] is True
assert result["data"] is None
assert result["data_type"] == "null"
print("Test 5 passed: JSON null handled")

# Test 6: Non-string input
result = parser.parse_text({"name": "Test"})
assert result["success"] is False
assert result["error_type"] == "InputTypeError"
print("Test 6 passed: Non-string input handled")

print("\nAll JSON parser tests passed.")
