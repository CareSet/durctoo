import pytest
from durctoo.forms import HTML5FormData, FormMethod, InputType

def test_form_initialization():
    form = HTML5FormData("test_form", method=FormMethod.POST)
    assert form.form_header["form_id"] == "test_form"
    assert form.form_header["method"] == "post"
    assert len(form.form_elements) == 0

def test_add_text_input():
    form = HTML5FormData("test_form")
    form.add_input(
        name="username",
        input_type=InputType.TEXT,
        required=True,
        label="Username"
    )
    
    assert len(form.form_elements) == 1
    element = form.form_elements[0]
    assert element["type"] == "input"
    assert element["input_type"] == "text"
    assert element["name"] == "username"
    assert element["required"] is True
    assert element["label"] == "Username"

def test_form_to_json():
    form = HTML5FormData("test_form")
    form.add_input("username", InputType.TEXT)
    
    json_str = form.to_json()
    assert isinstance(json_str, str)
    assert "form_header" in json_str
    assert "form_element_list" in json_str

def test_checkbox_group():
    form = HTML5FormData("test_form")
    options = [
        {"value": "1", "label": "Option 1"},
        {"value": "2", "label": "Option 2"}
    ]
    form.add_checkbox_group("choices", options, required=True, min_select=1)
    
    element = form.form_elements[0]
    assert element["type"] == "checkbox_group"
    assert element["required"] is True
    assert element["min_select"] == 1
    assert len(element["options"]) == 2

def test_radio_group():
    form = HTML5FormData("test_form")
    options = [
        {"value": "yes", "label": "Yes"},
        {"value": "no", "label": "No"}
    ]
    form.add_radio_group("choice", options, required=True)
    
    element = form.form_elements[0]
    assert element["type"] == "radio_group"
    assert element["required"] is True
    assert len(element["options"]) == 2

def test_select_element():
    form = HTML5FormData("test_form")
    options = [
        {"value": "1", "label": "One"},
        {"value": "2", "label": "Two"}
    ]
    form.add_select("numbers", options, required=True, multiple=True)
    
    element = form.form_elements[0]
    assert element["type"] == "select"
    assert element["multiple"] is True
    assert len(element["options"]) == 2
