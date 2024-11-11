#!/usr/bin/env python3
"""
validate_schema.py - Test the HTML5 form JSON schema against example forms

This script validates the example form JSON files against our schema to ensure
they conform to the expected structure.
"""

import json
import os
import sys
try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("Installing jsonschema package...")
    os.system(f"{sys.executable} -m pip install jsonschema")
    from jsonschema import validate, ValidationError

def load_schema():
    """Load the HTML5 form JSON schema."""
    schema_path = os.path.join(os.path.dirname(__file__), 'html5_form.schema.json')
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_form(form_data, schema):
    """
    Validate a form against the schema.
    
    Args:
        form_data (dict): The form data to validate
        schema (dict): The JSON schema to validate against
        
    Returns:
        bool: True if validation succeeds
        
    Raises:
        ValidationError: If the form data doesn't match the schema
    """
    validate(instance=form_data, schema=schema)
    return True

def main():
    """Test schema validation against example forms."""
    # Load the schema
    schema = load_schema()
    
    # Get the path to example forms
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    example_dir = os.path.join(project_root, 'example_output')
    
    # First generate the example forms
    examples_script = os.path.join(project_root, 'examples_json_maker.py')
    if os.path.exists(examples_script):
        print("Generating example forms...")
        os.system(f"{sys.executable} {examples_script}")
        print("\nValidating forms against schema...")
    else:
        print("Warning: examples_json_maker.py not found")
    
    # Test each example form
    example_files = [
        'login_form.json',
        'registration_form.json',
        'survey_form.json'
    ]
    
    for filename in example_files:
        filepath = os.path.join(example_dir, filename)
        try:
            with open(filepath, 'r') as f:
                form_data = json.load(f)
            
            validate_form(form_data, schema)
            print(f"✓ {filename} - Valid")
            
        except FileNotFoundError:
            print(f"✗ {filename} - File not found")
        except ValidationError as e:
            print(f"✗ {filename} - Validation failed:")
            print(f"  Error: {e.message}")
            print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        except json.JSONDecodeError:
            print(f"✗ {filename} - Invalid JSON format")

if __name__ == "__main__":
    main()
