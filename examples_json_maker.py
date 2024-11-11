#!/usr/bin/env python3
"""
examples_json_maker.py - Generate example JSON files for the durctoo package

This script creates various example forms using the HTML5FormData class and saves
their JSON representations to files in the example_output directory.

The script generates three types of forms:
1. A simple login form with username and password fields
2. A comprehensive registration form with various input types
3. A survey form demonstrating different question formats

Each form is saved as a JSON file in the example_output directory, which can be
used as reference or for testing purposes with the durctoo package.
"""

import os
import json
from durctoo.forms import HTML5FormData, FormMethod, InputType


def ensure_output_directory():
    """
    Create the example_output directory if it doesn't exist.
    
    This function ensures that there's a valid directory to store the generated
    JSON files. If the directory already exists, it will be used as-is.
    
    Returns:
        str: The path to the output directory ('example_output')
    """
    output_dir = "example_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def save_json_file(data: dict, filename: str, output_dir: str):
    """
    Save form data as a pretty-printed JSON file.
    
    Args:
        data (dict): The form data to be saved as JSON
        filename (str): The name of the output file (should end with .json)
        output_dir (str): The directory where the file will be saved
        
    The JSON output is formatted with an indent of 2 spaces for readability.
    The function prints a confirmation message after successfully creating the file.
    """
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Created {filepath}")


def create_login_form():
    """
    Create a simple login form and return its dictionary representation.
    
    Creates a basic authentication form with:
    - Username field (text input, required)
    - Password field (password input, required)
    
    The form uses POST method and submits to '/login'.
    
    Returns:
        dict: A dictionary representation of the login form structure
    """
    form = HTML5FormData(
        form_id="login_form",
        method=FormMethod.POST,
        action="/login"
    )
    
    form.add_input(
        name="username",
        input_type=InputType.TEXT,
        required=True,
        label="Username",
        placeholder="Enter your username"
    )
    
    form.add_input(
        name="password",
        input_type=InputType.PASSWORD,
        required=True,
        label="Password",
        placeholder="Enter your password"
    )
    
    return form.to_dict()


def create_registration_form():
    """
    Create a comprehensive registration form and return its dictionary representation.
    
    Creates a detailed registration form with multiple sections:
    - Basic Information:
        * Username (3-30 characters)
        * Email address
        * Password (min 8 characters)
    - Personal Details:
        * Full name
        * Date of birth
    - Contact Information:
        * Phone number (optional, with pattern validation)
        * Country (with predefined options)
    - Interests:
        * Multiple checkbox selection (1-3 choices)
    - Preferences:
        * Newsletter subscription option
    
    The form uses POST method, submits to '/register', and includes file upload capability.
    
    Returns:
        dict: A dictionary representation of the registration form structure
    """
    form = HTML5FormData(
        form_id="registration_form",
        method=FormMethod.POST,
        action="/register",
        enctype="multipart/form-data"
    )
    
    # Basic Information
    form.add_input(
        name="username",
        input_type=InputType.TEXT,
        required=True,
        label="Username",
        min_length=3,
        max_length=30
    )
    
    form.add_email_input(
        name="email",
        required=True,
        label="Email Address",
        placeholder="you@example.com"
    )
    
    form.add_input(
        name="password",
        input_type=InputType.PASSWORD,
        required=True,
        label="Password",
        min_length=8
    )
    
    # Personal Details
    form.add_input(
        name="full_name",
        input_type=InputType.TEXT,
        required=True,
        label="Full Name"
    )
    
    form.add_input(
        name="birth_date",
        input_type=InputType.DATE,
        required=True,
        label="Date of Birth"
    )
    
    # Contact Information
    form.add_input(
        name="phone",
        input_type=InputType.TEL,
        required=False,
        label="Phone Number",
        pattern=r"[0-9]{3}-[0-9]{3}-[0-9]{4}"
    )
    
    # Address with datalist for country
    countries = [
        "United States", "Canada", "United Kingdom", 
        "Australia", "Germany", "France", "Japan"
    ]
    form.add_datalist(
        name="country",
        options=countries,
        required=True,
        label="Country"
    )
    
    # Interests (checkbox group)
    interest_options = [
        {"value": "tech", "label": "Technology"},
        {"value": "sports", "label": "Sports"},
        {"value": "music", "label": "Music"},
        {"value": "travel", "label": "Travel"},
        {"value": "food", "label": "Food & Cooking"}
    ]
    form.add_checkbox_group(
        name="interests",
        options=interest_options,
        required=True,
        min_select=1,
        max_select=3
    )
    
    # Newsletter Subscription
    form.add_checkbox(
        name="newsletter",
        label="Subscribe to our newsletter",
        required=False
    )
    
    return form.to_dict()


def create_survey_form():
    """
    Create a survey form with various question types and return its dictionary representation.
    
    Creates a survey form with different types of questions:
    - Satisfaction Rating:
        * Single choice radio buttons (1-5 scale)
        * Default value set to neutral (3)
    - Areas for Improvement:
        * Multiple checkbox selection
        * Minimum one selection required
    - Usage Frequency:
        * Dropdown selection menu
    - Additional Feedback:
        * Large text area for open-ended responses
    
    The form uses POST method and submits to '/submit-survey'.
    
    Returns:
        dict: A dictionary representation of the survey form structure
    """
    form = HTML5FormData(
        form_id="survey_form",
        method=FormMethod.POST,
        action="/submit-survey"
    )
    
    # Single choice question
    satisfaction_options = [
        {"value": "5", "label": "Very Satisfied"},
        {"value": "4", "label": "Satisfied"},
        {"value": "3", "label": "Neutral"},
        {"value": "2", "label": "Dissatisfied"},
        {"value": "1", "label": "Very Dissatisfied"}
    ]
    form.add_radio_group(
        name="satisfaction",
        options=satisfaction_options,
        required=True,
        default_value="3"
    )
    
    # Multiple choice question
    improvement_options = [
        {"value": "speed", "label": "Speed"},
        {"value": "ui", "label": "User Interface"},
        {"value": "features", "label": "Features"},
        {"value": "support", "label": "Customer Support"},
        {"value": "price", "label": "Pricing"}
    ]
    form.add_checkbox_group(
        name="improvements",
        options=improvement_options,
        required=True,
        min_select=1
    )
    
    # Dropdown selection
    frequency_options = [
        {"value": "daily", "label": "Daily"},
        {"value": "weekly", "label": "Weekly"},
        {"value": "monthly", "label": "Monthly"},
        {"value": "rarely", "label": "Rarely"}
    ]
    form.add_select(
        name="usage_frequency",
        options=frequency_options,
        required=True
    )
    
    # Long text feedback
    form.add_textarea(
        name="feedback",
        required=False,
        label="Additional Feedback",
        rows=5,
        cols=50,
        placeholder="Please share any additional thoughts..."
    )
    
    return form.to_dict()


def main():
    """
    Generate all example forms and save them as JSON files.
    
    This is the main entry point of the script. It:
    1. Ensures the output directory exists
    2. Creates three different types of forms
    3. Saves each form as a JSON file
    4. Prints progress messages to the console
    
    The generated files can be found in the 'example_output' directory:
    - login_form.json
    - registration_form.json
    - survey_form.json
    """
    print("Durctoo Form Examples - JSON Generator")
    print("Generating example form JSON files...\n")
    
    output_dir = ensure_output_directory()
    
    # Create and save login form
    login_form = create_login_form()
    save_json_file(login_form, "login_form.json", output_dir)
    
    # Create and save registration form
    registration_form = create_registration_form()
    save_json_file(registration_form, "registration_form.json", output_dir)
    
    # Create and save survey form
    survey_form = create_survey_form()
    save_json_file(survey_form, "survey_form.json", output_dir)
    
    print("\nAll example JSON files have been created in the 'example_output' directory.")


if __name__ == "__main__":
    main()
