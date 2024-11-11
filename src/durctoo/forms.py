from enum import Enum, auto
from typing import List, Dict, Any, Optional, Union
import json

class FormMethod(Enum):
    GET = "get"
    POST = "post"

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
    def __init__(self, form_id: str, method: FormMethod = FormMethod.POST, action: str = "", enctype: str = ""):
        """Initialize a new HTML5 form data structure.
        
        Args:
            form_id: Unique identifier for the form
            method: HTTP method (GET or POST)
            action: Form submission URL
            enctype: Form encoding type
        """
        self.form_header = {
            "form_id": form_id,
            "method": method.value,
            "action": action,
            "enctype": enctype
        }
        self.form_elements: List[Dict[str, Any]] = []

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
