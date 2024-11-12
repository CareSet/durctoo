#!/usr/bin/env python3
"""
test_bulma_template.py - Test the Bulma CSS template for HTML5 forms

This script creates a test form with various input types and generates
a complete HTML page using the Bulma template.
"""

import os
import sys
from pathlib import Path
from pprint import pprint

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.insert(0, src_path)

from durctoo.forms import HTML5FormData, FormMethod, InputType
from durctoo.templates.bulma import BulmaFormTemplate

def create_test_form() -> HTML5FormData:
    """Create a test form with various input types."""
    form = HTML5FormData(
        form_id="test_form",
        method=FormMethod.POST,
        action="/submit",
        enctype="multipart/form-data"
    )
    
    # Text input with validation
    form.add_input(
        name="username",
        input_type=InputType.TEXT,
        required=True,
        label="Username",
        placeholder="Enter your username",
        min_length=3,
        max_length=20
    )
    
    # Password input
    form.add_input(
        name="password",
        input_type=InputType.PASSWORD,
        required=True,
        label="Password",
        placeholder="Enter your password",
        min_length=8
    )
    
    # Email input
    form.add_email_input(
        name="email",
        required=True,
        label="Email Address",
        placeholder="you@example.com"
    )
    
    # Textarea
    form.add_textarea(
        name="bio",
        required=False,
        label="Biography",
        placeholder="Tell us about yourself...",
        rows=4
    )
    
    # Select dropdown
    form.add_select(
        name="country",
        options=[
            {"value": "us", "label": "United States"},
            {"value": "ca", "label": "Canada"},
            {"value": "uk", "label": "United Kingdom"},
            {"value": "au", "label": "Australia"}
        ],
        required=True,
        label="Country"
    )
    
    # Radio group
    form.add_radio_group(
        name="subscription",
        options=[
            {"value": "free", "label": "Free Plan"},
            {"value": "pro", "label": "Pro Plan"},
            {"value": "enterprise", "label": "Enterprise Plan"}
        ],
        required=True,
        default_value="free"
    )
    
    # Checkbox group
    form.add_checkbox_group(
        name="interests",
        options=[
            {"value": "tech", "label": "Technology"},
            {"value": "sports", "label": "Sports"},
            {"value": "music", "label": "Music"},
            {"value": "travel", "label": "Travel"}
        ],
        required=True,
        min_select=1,
        max_select=3
    )
    
    # Single checkbox
    form.add_checkbox(
        name="newsletter",
        label="Subscribe to newsletter",
        required=False
    )
    
    # File input
    form.add_input(
        name="avatar",
        input_type=InputType.FILE,
        required=False,
        label="Profile Picture"
    )
    
    return form

def generate_complete_html(css: str, html: str, js: str) -> str:
    """Generate a complete HTML page."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bulma Form Test</title>
        <!-- Bulma CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            body {{
                background-color: #f5f5f5;
                min-height: 100vh;
            }}
            .section {{
                padding: 3rem 1.5rem;
            }}
            .box {{
                margin-top: 1rem;
                box-shadow: 0 2px 3px rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.1);
            }}
            .title {{
                color: #363636;
            }}
            .subtitle {{
                color: #7a7a7a;
                margin-bottom: 2rem;
            }}
        </style>
        {css}
    </head>
    <body>
        <section class="section">
            <div class="container">
                <div class="columns is-centered">
                    <div class="column is-half">
                        <div class="box">
                            <h1 class="title has-text-centered">Registration Form</h1>
                            <p class="subtitle has-text-centered">Please fill out the form below</p>
                            {html}
                        </div>
                    </div>
                </div>
            </div>
        </section>
        {js}
    </body>
    </html>
    """

def main():
    """Create test form and generate HTML with Bulma template."""
    # Create test form
    form = create_test_form()
    
    # Debug output
    print("\nForm Elements:")
    pprint(form.form_elements)
    
    # Generate form HTML using Bulma template
    css, html, js = BulmaFormTemplate.buildForm(form)
    
    print("\nGenerated HTML:")
    print(html)
    
    # Create complete HTML page
    complete_html = generate_complete_html(css, html, js)
    
    # Save to file
    output_dir = Path(__file__).parent.parent / 'example_output'
    output_file = output_dir / 'bulma_form_test.html'
    
    with open(output_file, 'w') as f:
        f.write(complete_html)
    
    print(f"\nTest form has been generated at: {output_file}")
    print("Open this file in a web browser to view the styled form.")

if __name__ == "__main__":
    main()
