# Durctoo

Durctoo is a Python package that provides clean abstractions for modeling HTML5 form data. It allows you to create, manipulate, and serialize form definitions independently of any specific web framework or rendering engine.

DURC stands for "reversed CRUD", and this project takes ideas from the [original PHP version of DURC](https://github.com/CareSet/DURC).

## Features

- Framework-agnostic HTML5 form modeling
- Support for all common HTML5 form elements
- Clean JSON serialization
- Type hints for better development experience
- No external dependencies

## Installation

```bash
pip install durctoo
```

## Quick Start

```python
from durctoo.forms import HTML5FormData, FormMethod, InputType

# Create a new form
form_model = HTML5FormData("registration_form", method=FormMethod.POST)

# Add form elements
form_model.add_input("username", InputType.TEXT, required=True, label="Username")
form_model.add_input("password", InputType.PASSWORD, required=True, label="Password")
form_model.add_email_input("email", required=True, label="Email Address")

# Get JSON representation
print(form_model.to_json())
```

## Documentation
Soon...

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
