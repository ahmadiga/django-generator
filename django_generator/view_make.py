from django.conf import settings
from os.path import join, exists

from os import makedirs


class View(object):
    view = ""
    urls = ""
    admin = ""
    model = None
    app_name = None
    model_name = None

    def __init__(self, model, app_name):
        self.model = model
        self.app_name = app_name
        self.model_name = model.__name__

        self.prepare_views()

    def prepare_list_view(self):
        self.view += "#def list_" + self.model_name.lower() + "(request,id=None):\n" \
                                                              "#    " + self.model_name.lower() + "s = " + self.model_name + ".objects.all()\n" \
                                                                                                                             "#    return render(request, '" + self.app_name + "/" + self.model_name.lower() + "/list_" + self.model_name.lower() + ".html', {'" + self.model_name.lower() + "s':" + self.model_name.lower() + "s})\n"
        self.create_list_html()
        self.create_item_html()

    def prepare_manage_view(self):
        self.view += "#def manage_" + self.model_name.lower() + "(request,id=None):\n" \
                                                                "#    if id:\n" \
                                                                "#        " + self.model_name.lower() + " = get_object_or_404(" + self.model_name + ",pk=id)\n" \
                                                                                                                                                    "#    else: \n" \
                                                                                                                                                    "#        " + self.model_name.lower() + " = None \n" \
                                                                                                                                                                                            "#    form =" + self.model_name + "Form(request.POST or None, instance=" + self.model_name.lower() + ")\n" \
                                                                                                                                                                                                                                                                                                 "#    if form.is_valid():\n" \
                                                                                                                                                                                                                                                                                                 "#        form.save()\n" \
                                                                                                                                                                                                                                                                                                 "#        return redirect(reverse('list_" + self.model_name.lower() + "'))\n" \
                                                                                                                                                                                                                                                                                                                                                                       "#    return render(request, '" + self.app_name + "/" + self.model_name.lower() + "/manage_" + self.model_name.lower() + ".html', {'form': form})\n"
        self.create_manage_html()

    def prepare_urls(self):
        self.urls += "# url(r'^list-" + self.model_name.lower() + "/$', views.list_" + self.model_name.lower() + ", name='list_" + self.model_name.lower() + "'), \n"
        self.urls += "# url(r'^manage-" + self.model_name.lower() + "/$', views.manage_" + self.model_name.lower() + ", name='manage_" + self.model_name.lower() + "'), \n"
        self.urls += "# url(r'^manage-" + self.model_name.lower() + "/(\d+)$', views.manage_" + self.model_name.lower() + ", name='manage_" + self.model_name.lower() + "'), \n"
        self.urls += "# url(r'^" + self.model_name.lower() + "-details/(\d+)$', views." + self.model_name.lower() + "_details, name='" + self.model_name.lower() + "_details'), \n"

    def prepare_admin(self):
        self.admin += "# admin.site.register(" + self.model_name + ") \n"

    def create_manage_html(self):
        text = "{% extends \"" + self.app_name + "/layout/layout.html\" %}\n" \
                                                 "{% load crispy_forms_tags %}\n" \
                                                 "{% load i18n %}\n" \
                                                 "{% block content %}\n" \
                                                 "<div class=\"row\">\n" \
                                                 "<div class=\"col-md-12\">\n" \
                                                 "{% crispy form %}\n" \
                                                 "</div>\n" \
                                                 "</div>\n" \
                                                 "{% endblock %}"

        CURRENT_PATH = settings.BASE_DIR
        app_folder = join(CURRENT_PATH, self.app_name, "templates", self.app_name, self.model_name.lower())
        if not exists(app_folder):
            makedirs(app_folder)
        my_file = open(app_folder + '/' + "manage_" + self.model_name.lower() + ".html", "a")
        my_file.writelines(text)
        my_file.close()

    def create_item_html(self):
        text = "{% load i18n %}\n" \
               "<div class=\"row\">\n"

        for field in self.model._meta.get_fields():
            text += "<div class=\"col-md-3\">\n" \
                    "{{ item." + field.name + " }}\n" \
                                              "</div>\n"
        text += "<div class=\"col-md-3\">\n" \
                "<div class=\"btn-group  btn-group-justified\" role=\"group\">\n" \
                "<a class='btn btn-info' href={% url 'manage_" + self.model_name.lower() + "' item.id %}>{% trans \"Edit\" %}</a>\n" \
                                                                                           "<a class='btn btn-info' href={% url '" + self.model_name.lower() + "_details' item.id %}>{% trans \"View\" %}</a>\n" \
                                                                                                                                                               "</div>\n" \
                                                                                                                                                               "</div>\n" \
                                                                                                                                                               "</div>\n"

        CURRENT_PATH = settings.BASE_DIR
        app_folder = join(CURRENT_PATH, self.app_name, "templates", self.app_name, self.model_name.lower())
        if not exists(app_folder):
            makedirs(app_folder)
        my_file = open(app_folder + '/' + self.model_name.lower() + "_item.html", "a")
        my_file.writelines(text)
        my_file.close()

    def create_list_html(self):
        text = "{% extends \"" + self.app_name + "/layout/layout.html\" %}\n" \
                                                 "{% load i18n %}\n" \
                                                 "{% block content %}\n" \
                                                 "<div class=\"row\">\n" \
                                                 "<div class=\"col-md-3 col-md-offset-9\">\n" \
                                                 "<a class='btn btn-info btn-block' href={% url 'manage_" + self.model_name.lower() + "' %}>{% trans 'Add " + self.model_name + "' %}</a>\n" \
                                                                                                                                                                                "</div>\n" \
                                                                                                                                                                                "</div>\n" \
                                                                                                                                                                                "<hr />\n" \
                                                                                                                                                                                "<div class=\"row\">\n" \
                                                                                                                                                                                "<div class=\"col-md-12\">\n" \
 \
                                                                                                                                                                                "{% for item in " + self.model_name.lower() + "s %}\n" \
                                                                                                                                                                                                                              "{% include '" + self.app_name + "/" + self.model_name.lower() + "/" + self.model_name.lower() + "_item.html' %}\n" \
                                                                                                                                                                                                                                                                                                                               "{% endfor %}\n" \
                                                                                                                                                                                                                                                                                                                               "</div>\n" \
                                                                                                                                                                                                                                                                                                                               "</div>\n" \
                                                                                                                                                                                                                                                                                                                               "{% endblock %}\n"

        CURRENT_PATH = settings.BASE_DIR
        app_folder = join(CURRENT_PATH, self.app_name, "templates", self.app_name, self.model_name.lower())
        if not exists(app_folder):
            makedirs(app_folder)
        my_file = open(app_folder + '/' + "list_" + self.model_name.lower() + ".html", "a")
        my_file.writelines(text)
        my_file.close()

    def prepare_item_details_view(self):
        self.view += "#def " + self.model_name.lower() + "_details(request,id=None):\n" \
                                                         "#    " + self.model_name.lower() + " = get_object_or_404(" + self.model_name + ",pk=id)\n" \
                                                                                                                                         "#    return render(request, '" + self.app_name + "/" + self.model_name.lower() + "/" + self.model_name.lower() + "_details.html', {'" + self.model_name.lower() + "': " + self.model_name.lower() + "})\n"
        self.create_details_html()

    def create_details_html(self):
        text = "{% extends \"" + self.app_name + "/layout/layout.html\" %}\n" \
                                                 "{% load i18n %}\n" \
                                                 "{% block content %}\n" \
                                                 "<div class=\"row\">\n"

        counter = 1
        for field in self.model._meta.get_fields():
            try:
                text += "<div class=\"col-md-3\">\n" \
                        "" + field.verbose_name + "\n" \
                                                  "</div>\n" \
                                                  "<div class=\"col-md-3\">\n" \
                                                  "{{ " + self.model_name.lower() + "." + field.name + " }}\n" \
                                                                                                       "</div>\n"
            except:
                text += "<div class=\"col-md-3\">\n" \
                        "" + field.name + "\n" \
                                          "</div>\n" \
                                          "<div class=\"col-md-3\">\n" \
                                          "{{ " + self.model_name.lower() + "." + field.name + " }}\n" \
                                                                                               "</div>\n"

            if (counter % 2) == 0:
                text += "</div>\n" \
                        "<div class=\"row\">\n"
            counter += 1

        text += "</div>\n" \
                "{% endblock %}\n"

        CURRENT_PATH = settings.BASE_DIR
        app_folder = join(CURRENT_PATH, self.app_name, "templates", self.app_name, self.model_name.lower())
        if not exists(app_folder):
            makedirs(app_folder)
        my_file = open(app_folder + '/' + "" + self.model_name.lower() + "_details.html", "a")
        my_file.writelines(text)
        my_file.close()

    def prepare_views(self):
        self.prepare_list_view()
        self.prepare_manage_view()
        self.prepare_item_details_view()
        self.prepare_urls()
        self.prepare_admin()
