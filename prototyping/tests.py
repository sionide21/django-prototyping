from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from view_decorators import _template_name


class TemplateNameTest(TestCase):
    """
    Ensure the template name function creates `app/viewname.html`
    """
    def test_basic_app(self):
        """
        Simple case

        myapp/
          views.py
            def foo():
        """

        def foo(): pass
        foo.__module__ = 'myapp.views'

        self.assertEqual(_template_name(foo), "myapp/foo.html")

    def test_module_app(self):
        """
        Entire app is in submodule

        myproject/
          myapp/
            views.py
              def foo():
        """

        def foo(): pass
        foo.__module__ = 'myproject.myapp.views'

        self.assertEqual(_template_name(foo), "myapp/foo.html")

    def test_module_views(self):
        """
        Views in submodules should have templates in subfolders

        myapp/
          views/
            api.py
              def foo():
        """

        def foo(): pass
        foo.__module__ = 'myapp.views.api'

        self.assertEqual(_template_name(foo), "myapp/api/foo.html")

    def test_module_app_and_module_views(self):
        """
        Views in submodules should have templates in subfolders even if app is submodule

        myproject/
          myapp/
            views/
              api.py
                def foo():
        """

        def foo(): pass
        foo.__module__ = 'myproject.myapp.views.api'

        self.assertEqual(_template_name(foo), "myapp/api/foo.html")

    def test_nonstandard_views_should_raise_misconfigured(self):
        """
        If views are not in a module or package called `views`, the template name must be specified

        myapp/
          api_views.py
            def foo():
        """

        def foo(): pass
        foo.__module__ = 'myapp.api_views'

        self.assertRaises(ImproperlyConfigured, _template_name, foo)
