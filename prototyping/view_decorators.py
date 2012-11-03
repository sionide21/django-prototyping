from functools import wraps
from django.shortcuts import render_to_response
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


def _template_name(fn):
    """
    Return template path for a given view.
    """
    parts = fn.__module__.split('.')
    if 'views' not in parts:
        raise ImproperlyConfigured("If your views are not in a views module, you must specify the template explicitly.")
    root = parts.index('views')
    app = parts[root - 1]
    path = [app] + parts[root + 1:] + [fn.__name__]
    return "%s.html" % '/'.join(path)


def view(*args, **kwargs):
    """
    A decorator that removes some of the boiler plate from writing views.

    The simplest case is to return your context as a dict. For example, the following view in `myapp`:

        @view
        def my_view(request):
            return {
                "my_var": "foo"
            }

    will render the template `myapp/my_view.html` with the context `{"my_var": "foo"}`.

    If you return `None`, an empty context will be used.
    If you return an `HTTPResponse` instance, it will be returned directly.

    ## Options

    You can pass options into view to override some behavior:

    json: If True, the returned dict will be rendered as json. Default: `False`
    template: The name of the template file to render. Default: `<appname>/<viewname>.html`

    """
    opts = {}

    def view_decorator(fn):
        @wraps(fn)
        def _view(request, *args, **kwargs):
            ctx = fn(request, *args, **kwargs)
            if not ctx:
                ctx = {}
            if isinstance(ctx, HttpResponse):
                return ctx
            elif opts.get("json"):
                return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder), content_type="application/json")
            else:
                return render_to_response(opts.get("template") or _template_name(fn), ctx)
        return _view

    if len(args) == 1 and not kwargs and callable(args[0]):
        # Decorator without parens
        return view_decorator(args[0])
    else:
        # Decorator with parens
        opts = kwargs
        return view_decorator
