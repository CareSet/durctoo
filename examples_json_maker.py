import json
from src.durctoo.forms import FormGenerator
from src.durctoo.templates import MaterializeFormTemplate

example_form_json = {
    "form": {
        "form_header": {
            "form_id": "example_form",
            "method": "POST",
            "action": "/submit",
            "enctype": ""
        },
        "form_element_list": [
            {
                "type": "input",
                "input_type": "text",
                "name": "name",
                "label": "Name",
                "required": True,
                "placeholder": "Enter your name"
            },
            {
                "type": "select",
                "name": "color",
                "label": "Favorite Color",
                "required": True,
                "options": [
                    {
                        "value": "red",
                        "label": "Red"
                    },
                    {
                        "value": "green",
                        "label": "Green"
                    },
                    {
                        "value": "blue",
                        "label": "Blue"
                    }
                ]
            }
        ]
    }
}

form_generator = FormGenerator(example_form_json, MaterializeFormTemplate)
generated_form = form_generator.generate_form()

print("Generated Materialize Form:")
print(generated_form)

with open("example_output/materialize_form.html", "w") as f:
    f.write(generated_form)
