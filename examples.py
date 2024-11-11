#!/usr/bin/env python3
"""
examples.py - Example usage of the durctoo package

This script demonstrates various ways to use the HTML5FormData class to model
different types of forms commonly found in web applications.
"""

from durctoo.forms import HTML5FormData, FormMethod, InputType


def create_login_form():
    """Create a simple login form."""
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
    
    print("\n=== Login Form ===")
    print(form.to_json())


def create_registration_form():
    """Create a more complex registration form."""
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
    
    print("\n=== Registration Form ===")
    print(form.to_json())


def create_survey_form():
    """Create a survey form with various question types."""
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
    
    print("\n=== Survey Form ===")
    print(form.to_json())


def main():
    """Run all example form creations."""
    print("Durctoo HTML5 Form Examples\n")
    print("This script demonstrates various form configurations possible with durctoo.")
    print("Each example shows a different type of form and its JSON representation.\n")
    
    create_login_form()
    create_registration_form()
    create_survey_form()


if __name__ == "__main__":
    main()
