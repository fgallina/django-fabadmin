import inspect
import os

from ansi2html import Ansi2HTMLConverter
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.datastructures import SortedDict
from fabric.main import load_tasks_from_module

from fabadmin.forms import FabfileForm
import subprocess


class Task(object):
    """Class that summarizes a fabric task."""

    def __init__(self, func):
        argspec = inspect.getargspec(func)
        defaults = argspec.defaults
        args = argspec.args
        has_args = bool(len(args))
        docstring = func.__doc__.strip()
        first_newline = docstring.find("\n")
        name = func.__name__
        if first_newline == -1:
            short_docstring = docstring
        else:
            short_docstring = docstring[:first_newline]
        self.name = name
        self.value = name
        self.description = docstring
        self.short_description = short_docstring
        self.has_args = has_args
        if has_args:
            if defaults:
                required_args = args[:-len(defaults)]
                non_required_args = args[-len(defaults):]
                default_args = SortedDict()
                self.required_args = required_args
                for i, arg in enumerate(non_required_args):
                    default_args[arg] = defaults[i]
                self.default_args = default_args
            else:
                self.required_args = args
                self.default_args = {}
        else:
            self.required_args = []
            self.default_args = {}
        self.is_null = False


class NullTask(object):
    """Class that emulates a null task."""

    def __init__(self):
        self.name = "--------"
        self.value = ""
        self.description = ""
        self.short_description = ""
        self.has_args = ""
        self.required_args = ""
        self.default_args = ""
        self.is_null = False


@staff_member_required
def task_list(request):
    """List available fabric tasks."""
    fabfile_path = settings.FABADMIN_FABFILE
    filename = os.path.split(fabfile_path)[1]
    module = os.path.splitext(filename)[0]
    fabfile = __import__(module)
    _, new_style, classic, default = load_tasks_from_module(fabfile)
    tasks = []
    for task_group in [new_style, classic, default]:
        if task_group:
            for task in task_group.values():
                tasks.append(Task(task))
    task_choices = [NullTask()] + tasks
    output = ""
    if request.method == "POST":
        fabfile_form = FabfileForm(request.POST, tasks=task_choices)
        if fabfile_form.is_valid():
            cleaned_data = fabfile_form.cleaned_data
            task = cleaned_data['task']
            arguments = cleaned_data['arguments']
            args = ['fab', '-f', fabfile_path, task + ":" + arguments]
            process = subprocess.Popen(
                args, shell=False, stdout=subprocess.PIPE
            )
            converter = Ansi2HTMLConverter()
            shell_output = process.communicate()[0]
            output = converter.convert(shell_output, False)
    else:
        fabfile_form = FabfileForm(tasks=task_choices)
    return render_to_response("fabadmin/task_list.html", {
        'tasks': tasks,
        'fabfile_form': fabfile_form,
        'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
        'output': output
    }, RequestContext(request, {}))
