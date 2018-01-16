class Form(object):
    text = ""

    def __init__(self, model):
        self.prepare_form(model)

    def prepare_form_footer(self):
        self.text += "#            Div(Div(Submit('save', _('Save Changes'), css_class='btn btn-success btn-block'),css_class=\"col-md-6 col-md-offset-3\"),\n" \
                     "#               css_class=\"row\")\n" \
                     "#        )\n" \
                     "#    )\n"

    def prepare_form_header(self, name):
        self.text += "#@parsleyfy\n" \
                     "#class " + name + "Form(ModelForm):\n" \
                                        "#    class Meta:\n" \
                                        "#        model = " + name + "\n" \
                                                                     "#        exclude = []\n" \
                                                                     "#    def __init__(self, *args, **kwargs):\n" \
                                                                     "#        super(" + name + "Form, self).__init__(*args, **kwargs)\n" \
                                                                                                "#        self.helper = FormHelper()\n" \
                                                                                                "#        self.helper.attrs = {\"data-parsley-validate\": \"data-parsley-validate\"}\n" \
                                                                                                "#        self.helper.layout = Layout(\n" \
                                                                                                "#            Div(\n"

    def add_field(self, name):
        self.text += "#                    Div('" + name + "', css_class=\"col-md-6\"),\n"

    def prepare_form(self, model):
        forms = ""
        self.prepare_form_header(model.__name__)
        counter = 1
        for field in model._meta.get_fields():
            if not field.auto_created:
                self.add_field(field.name)
                if (counter % 2) == 0:
                    self.text += "#                css_class=\"row\"),\n" \
                                 "#                Div(\n"
                counter += 1
        self.prepare_form_footer()
