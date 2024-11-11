from enum import Enum, auto
from typing import List, Dict, Any, Optional, Union
import json
import os
from pathlib import Path
from jsonschema import validate, ValidationError

class FormMethod(Enum):
    """Form HTTP methods.
    
    While the enum uses uppercase values as per industry standards,
    it supports case-insensitive matching when creating from strings.
    """
    GET = "GET"
    POST = "POST"

    @classmethod
    def from_string(cls, value: str) -> 'FormMethod':
        """Create a FormMethod from a string, case-insensitive."""
        try:
            return cls(value.upper())
        except ValueError:
            raise ValueError(f"Invalid form method: {value}. Must be either 'GET'/'get' or 'POST'/'post'")

class InputType(Enum):
    TEXT = "text"
    PASSWORD = "password"
    EMAIL = "email"
    URL = "url"
    NUMBER = "number"
    TEL = "tel"
    DATE = "date"
    TIME = "time"
    DATETIME_LOCAL = "datetime-local"
    MONTH = "month"
    WEEK = "week"
    COLOR = "color"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    HIDDEN = "hidden"
    SUBMIT = "submit"
    RESET = "reset"
    BUTTON = "button"
    FILE = "file"

class HTML5FormData:
    # Load the schema once when the module is imported
    _schema = None
    
    @classmethod
    def _get_schema(cls) -> dict:
        """Load and cache the JSON schema."""
        if cls._schema is None:
            schema_path = Path(__file__).parent / 'json_schemas' / 'html5_form.schema.json'
            with open(schema_path, 'r') as f:
                cls._schema = json.load(f)
        return cls._schema

    def __init__(self, form_id: str, method: Union[FormMethod, str] = FormMethod.POST, action: str = "", enctype: str = ""):
        """Initialize a new HTML5 form data structure.
        
        Args:
            form_id: Unique identifier for the form
            method: HTTP method (GET/get or POST/post), case-insensitive
            action: Form submission URL
            enctype: Form encoding type
        """
        if isinstance(method, str):
            method = FormMethod.from_string(method)
        
        self.form_header = {
            "form_id": form_id,
            "method": method.value,  # Always uppercase in output
            "action": action,
            "enctype": enctype
        }
        self.form_elements: List[Dict[str, Any]] = []

    @staticmethod
    def create_from_json(source: Union[str, dict]) -> 'HTML5FormData':
        """Create a new HTML5FormData instance from JSON data.
        
        Args:
            source: Either a file path to a JSON file, a JSON string, or a dictionary
                   containing the form data.
        
        Returns:
            HTML5FormData: A new instance populated with the form data
            
        Raises:
            ValueError: If the JSON data is invalid or missing required fields
            FileNotFoundError: If the specified JSON file doesn't exist
            json.JSONDecodeError: If the JSON string is invalid
            jsonschema.ValidationError: If the JSON data doesn't conform to the schema
        """
        # Load the JSON data
        if isinstance(source, dict):
            data = source
        elif isinstance(source, str):
            if os.path.isfile(source):
                with open(source, 'r') as f:
                    data = json.load(f)
            else:
                try:
                    data = json.loads(source)
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON string provided")
        else:
            raise TypeError("Source must be a file path, JSON string, or dictionary")

        # Validate against schema
        try:
            validate(instance=data, schema=HTML5FormData._get_schema())
        except ValidationError as e:
            raise ValidationError(f"JSON validation failed: {e.message} at path: {' -> '.join(str(p) for p in e.path)}")

        # Extract form data
        form_data = data['form']
        header = form_data['form_header']
        
        # Create new instance
        method = FormMethod.from_string(header['method'])
        instance = HTML5FormData(
            form_id=header['form_id'],
            method=method,
            action=header['action'],
            enctype=header.get('enctype', '')
        )

        # Add form elements
        for element in form_data['form_element_list']:
            element_type = element['type']
            
            if element_type == 'input':
                input_type = element['input_type']
                if input_type == 'email':
                    instance.add_email_input(
                        name=element['name'],
                        required=element.get('required', False),
                        label=element.get('label', ''),
                        placeholder=element.get('placeholder', ''),
                        multiple=element.get('multiple', False)
                    )
                elif input_type == 'url':
                    instance.add_url_input(
                        name=element['name'],
                        required=element.get('required', False),
                        label=element.get('label', ''),
                        placeholder=element.get('placeholder', '')
                    )
                elif input_type == 'checkbox' and 'checked' in element:
                    instance.add_checkbox(
                        name=element['name'],
                        required=element.get('required', False),
                        label=element.get('label', ''),
                        checked=element.get('checked', False)
                    )
                else:
                    instance.add_input(
                        name=element['name'],
                        input_type=InputType(input_type),
                        required=element.get('required', False),
                        label=element.get('label', ''),
                        placeholder=element.get('placeholder', ''),
                        value=element.get('value', ''),
                        min_length=element.get('min_length'),
                        max_length=element.get('max_length'),
                        pattern=element.get('pattern')
                    )
            
            elif element_type == 'textarea':
                instance.add_textarea(
                    name=element['name'],
                    required=element.get('required', False),
                    label=element.get('label', ''),
                    rows=element.get('rows', 3),
                    cols=element.get('cols', 40),
                    placeholder=element.get('placeholder', ''),
                    value=element.get('value', '')
                )
            
            elif element_type == 'checkbox_group':
                instance.add_checkbox_group(
                    name=element['name'],
                    options=element['options'],
                    required=element.get('required', False),
                    min_select=element.get('min_select', 0),
                    max_select=element.get('max_select')
                )
            
            elif element_type == 'radio_group':
                instance.add_radio_group(
                    name=element['name'],
                    options=element['options'],
                    required=element.get('required', False),
                    default_value=element.get('default_value')
                )
            
            elif element_type == 'select':
                instance.add_select(
                    name=element['name'],
                    options=element['options'],
                    required=element.get('required', False),
                    multiple=element.get('multiple', False),
                    size=element.get('size')
                )
            
            elif element_type == 'datalist':
                instance.add_datalist(
                    name=element['name'],
                    options=element['options'],
                    required=element.get('required', False),
                    label=element.get('label', '')
                )

        return instance

    def add_input(self, name: str, input_type: InputType, required: bool = False, 
                 label: str = "", placeholder: str = "", value: str = "",
                 min_length: Optional[int] = None, max_length: Optional[int] = None,
                 pattern: Optional[str] = None) -> None:
        """Add a basic input field to the form."""
        element = {
            "type": "input",
            "input_type": input_type.value,
            "name": name,
            "required": required,
            "label": label,
            "placeholder": placeholder,
            "value": value
        }
        
        if min_length is not None:
            element["min_length"] = min_length
        if max_length is not None:
            element["max_length"] = max_length
        if pattern is not None:
            element["pattern"] = pattern
            
        self.form_elements.append(element)

    def add_textarea(self, name: str, required: bool = False, label: str = "",
                    rows: int = 3, cols: int = 40, placeholder: str = "",
                    value: str = "") -> None:
        """Add a textarea field to the form."""
        self.form_elements.append({
            "type": "textarea",
            "name": name,
            "required": required,
            "label": label,
            "rows": rows,
            "cols": cols,
            "placeholder": placeholder,
            "value": value
        })

    def add_checkbox(self, name: str, required: bool = False, 
                    label: str = "", checked: bool = False) -> None:
        """Add a single checkbox to the form."""
        self.form_elements.append({
            "type": "input",
            "input_type": "checkbox",
            "name": name,
            "required": required,
            "label": label,
            "checked": checked
        })

    def add_checkbox_group(self, name: str, options: List[Dict[str, str]], 
                          required: bool = False, min_select: int = 0,
                          max_select: Optional[int] = None) -> None:
        """Add a group of checkboxes to the form.
        
        Args:
            name: Group name
            options: List of dictionaries with 'value' and 'label' keys
            required: Whether at least one option must be selected
            min_select: Minimum number of options that must be selected
            max_select: Maximum number of options that can be selected
        """
        self.form_elements.append({
            "type": "checkbox_group",
            "name": name,
            "required": required,
            "min_select": min_select,
            "max_select": max_select,
            "options": options
        })

    def add_radio_group(self, name: str, options: List[Dict[str, str]], 
                       required: bool = False, default_value: Optional[str] = None) -> None:
        """Add a group of radio buttons to the form.
        
        Args:
            name: Group name
            options: List of dictionaries with 'value' and 'label' keys
            required: Whether an option must be selected
            default_value: Value to be selected by default
        """
        self.form_elements.append({
            "type": "radio_group",
            "name": name,
            "required": required,
            "default_value": default_value,
            "options": options
        })

    def add_select(self, name: str, options: List[Dict[str, str]], 
                  required: bool = False, multiple: bool = False,
                  size: Optional[int] = None) -> None:
        """Add a select element to the form.
        
        Args:
            name: Select element name
            options: List of dictionaries with 'value' and 'label' keys
            required: Whether a selection is required
            multiple: Whether multiple options can be selected
            size: Number of visible options
        """
        self.form_elements.append({
            "type": "select",
            "name": name,
            "required": required,
            "multiple": multiple,
            "size": size,
            "options": options
        })

    def add_datalist(self, name: str, options: List[str], 
                    required: bool = False, label: str = "") -> None:
        """Add a datalist input element to the form."""
        self.form_elements.append({
            "type": "datalist",
            "name": name,
            "required": required,
            "label": label,
            "options": options
        })

    def add_email_input(self, name: str, required: bool = False, 
                       label: str = "", placeholder: str = "",
                       multiple: bool = False) -> None:
        """Add an email input field with HTML5 validation."""
        self.form_elements.append({
            "type": "input",
            "input_type": "email",
            "name": name,
            "required": required,
            "label": label,
            "placeholder": placeholder,
            "multiple": multiple
        })

    def add_url_input(self, name: str, required: bool = False,
                     label: str = "", placeholder: str = "") -> None:
        """Add a URL input field with HTML5 validation."""
        self.form_elements.append({
            "type": "input",
            "input_type": "url",
            "name": name,
            "required": required,
            "label": label,
            "placeholder": placeholder
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert the form data to a dictionary."""
        return {
            "form": {
                "form_header": self.form_header,
                "form_element_list": self.form_elements
            }
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert the form data to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def __str__(self) -> str:
        """Return a pretty-printed JSON representation of the form."""
        return self.to_json()

    def __repr__(self) -> str:
        """Return a string representation of the form object."""
        return f"HTML5FormData(id='{self.form_header['form_id']}', elements={len(self.form_elements)})"
