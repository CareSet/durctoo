#!/usr/bin/env python3
"""
test_form_json_loading.py - Test the JSON loading capabilities of HTML5FormData

This script tests:
1. Loading example JSON files
2. Creating HTML5FormData objects from them
3. Converting back to JSON
4. Case-insensitive method handling
5. Uppercase method output in templates
6. Schema validation for JSON input
"""

import os
import json
import sys
from pathlib import Path
from typing import Any, Dict
from pprint import pprint
from jsonschema import ValidationError

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.insert(0, src_path)

from durctoo.forms import HTML5FormData, FormMethod

def test_schema_validation():
    """Test JSON schema validation in create_from_json."""
    print("\nTesting schema validation:")
    
    # Test 1: Missing required field
    invalid_json = {
        "form": {
            "form_header": {
                # Missing form_id
                "method": "POST",
                "action": "/test"
            },
            "form_element_list": []
        }
    }
    try:
        HTML5FormData.create_from_json(invalid_json)
        print("✗ Failed to catch missing required field")
        return False
    except ValidationError as e:
        if "form_id" in str(e):
            print("✓ Correctly caught missing required field")
        else:
            print(f"✗ Unexpected validation error: {e}")
            return False

    # Test 2: Invalid method value
    invalid_json = {
        "form": {
            "form_header": {
                "form_id": "test_form",
                "method": "INVALID",  # Invalid method
                "action": "/test"
            },
            "form_element_list": []
        }
    }
    try:
        HTML5FormData.create_from_json(invalid_json)
        print("✗ Failed to catch invalid method value")
        return False
    except ValidationError as e:
        if "method" in str(e):
            print("✓ Correctly caught invalid method value")
        else:
            print(f"✗ Unexpected validation error: {e}")
            return False

    # Test 3: Invalid input type
    invalid_json = {
        "form": {
            "form_header": {
                "form_id": "test_form",
                "method": "POST",
                "action": "/test"
            },
            "form_element_list": [{
                "type": "input",
                "input_type": "invalid_type",  # Invalid input type
                "name": "test"
            }]
        }
    }
    try:
        HTML5FormData.create_from_json(invalid_json)
        print("✗ Failed to catch invalid input type")
        return False
    except ValidationError as e:
        if "input_type" in str(e):
            print("✓ Correctly caught invalid input type")
        else:
            print(f"✗ Unexpected validation error: {e}")
            return False

    # Test 4: Valid JSON
    valid_json = {
        "form": {
            "form_header": {
                "form_id": "test_form",
                "method": "POST",
                "action": "/test"
            },
            "form_element_list": [{
                "type": "input",
                "input_type": "text",
                "name": "test_input",
                "required": True,
                "label": "Test Input"
            }]
        }
    }
    try:
        form = HTML5FormData.create_from_json(valid_json)
        if form.form_header["form_id"] == "test_form":
            print("✓ Successfully processed valid JSON")
        else:
            print("✗ Failed to process valid JSON correctly")
            return False
    except Exception as e:
        print(f"✗ Unexpected error with valid JSON: {e}")
        return False

    return True

def find_dict_differences(dict1: Dict[str, Any], dict2: Dict[str, Any], path: str = "") -> list:
    """
    Find all differences between two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        path: Current path in the dictionary (for nested diffs)
        
    Returns:
        list: List of differences found
    """
    differences = []
    
    # Check for keys in dict1 that aren't in dict2
    for key in dict1:
        current_path = f"{path}.{key}" if path else key
        if key not in dict2:
            differences.append(f"Key '{current_path}' missing in second dict")
            continue
            
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            differences.extend(find_dict_differences(dict1[key], dict2[key], current_path))
        elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
            if len(dict1[key]) != len(dict2[key]):
                differences.append(f"List length mismatch at '{current_path}': {len(dict1[key])} != {len(dict2[key])}")
            for i, (item1, item2) in enumerate(zip(dict1[key], dict2[key])):
                if isinstance(item1, dict) and isinstance(item2, dict):
                    differences.extend(find_dict_differences(item1, item2, f"{current_path}[{i}]"))
                elif item1 != item2:
                    differences.append(f"Value mismatch at '{current_path}[{i}]': {item1} != {item2}")
        elif dict1[key] != dict2[key]:
            differences.append(f"Value mismatch at '{current_path}': {dict1[key]} != {dict2[key]}")
    
    # Check for keys in dict2 that aren't in dict1
    for key in dict2:
        current_path = f"{path}.{key}" if path else key
        if key not in dict1:
            differences.append(f"Key '{current_path}' missing in first dict")
    
    return differences

def test_method_case_handling():
    """Test case-insensitive method handling and uppercase output."""
    print("\nTesting HTTP method case handling:")
    
    # Test lowercase input
    form1 = HTML5FormData("test_form", method="post")
    if form1.form_header["method"] != "POST":
        print("✗ Failed to convert lowercase 'post' to uppercase")
        return False
    
    # Test uppercase input
    form2 = HTML5FormData("test_form", method="POST")
    if form2.form_header["method"] != "POST":
        print("✗ Failed to maintain uppercase 'POST'")
        return False
    
    # Test enum input
    form3 = HTML5FormData("test_form", method=FormMethod.POST)
    if form3.form_header["method"] != "POST":
        print("✗ Failed to handle FormMethod enum")
        return False
    
    # Test JSON loading with lowercase method
    json_data = {
        "form": {
            "form_header": {
                "form_id": "test_form",
                "method": "post",
                "action": "/test"
            },
            "form_element_list": []
        }
    }
    form4 = HTML5FormData.create_from_json(json_data)
    if form4.form_header["method"] != "POST":
        print("✗ Failed to convert lowercase method from JSON")
        return False
    
    print("✓ All method case handling tests passed")
    return True

def compare_forms(original_file: str) -> bool:
    """
    Compare a form loaded from JSON with its original file.
    
    Args:
        original_file: Path to the original JSON file
        
    Returns:
        bool: True if the forms match, False otherwise
    """
    print(f"\nTesting {os.path.basename(original_file)}:")
    
    # Load the original JSON
    with open(original_file, 'r') as f:
        original_data = json.load(f)
    
    try:
        # Create form from JSON
        form = HTML5FormData.create_from_json(original_file)
        
        # Convert back to dictionary
        recreated_data = form.to_dict()
        
        # Compare the structures
        differences = find_dict_differences(original_data, recreated_data)
        
        if not differences:
            print("✓ Form successfully recreated from JSON")
            print("✓ Recreated form matches original exactly")
            return True
        else:
            print("✗ Differences found between original and recreated form:")
            for diff in differences:
                print(f"  - {diff}")
            print("\nOriginal data:")
            pprint(original_data)
            print("\nRecreated data:")
            pprint(recreated_data)
            return False
            
    except Exception as e:
        print(f"✗ Error processing form: {str(e)}")
        return False

def main():
    """Test JSON loading with example forms."""
    print("Testing HTML5FormData JSON Loading")
    print("==================================")
    
    # Test schema validation
    if not test_schema_validation():
        sys.exit(1)
    
    # Test method case handling
    if not test_method_case_handling():
        sys.exit(1)
    
    # Get paths to example files
    example_dir = Path(__file__).parent.parent / 'example_output'
    example_files = [
        example_dir / 'login_form.json',
        example_dir / 'registration_form.json',
        example_dir / 'survey_form.json'
    ]
    
    # Test each example form
    success_count = 0
    for file_path in example_files:
        if compare_forms(str(file_path)):
            success_count += 1
    
    # Print summary
    print("\nSummary:")
    print(f"Passed: {success_count}/{len(example_files)} tests")
    
    # Return appropriate exit code
    sys.exit(0 if success_count == len(example_files) else 1)

if __name__ == "__main__":
    main()
