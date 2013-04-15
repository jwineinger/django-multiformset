===================
django-multiformset
===================

Multiformset is a Django app that provides a base view and template
for using multiple formsets on the same page. 

The specific use case this was developed for is a situation where
you want to allow your users to dynamically add a new form to a page, 
where the form is one of any number of choices. Conceptually, the way
this is solved is by including on the page a formset for each type
of form that the user can use.  For each formset an empty form is
rendered and hidden, to be used as a template. When the user adds
a form, the proper hidden "template" form is cloned and the field
names and ids are adjusted according to the current value of that
specific formset's management form.

Quick start
-----------

1. Add "multiformset" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'multiformset',
      )

2. Subclass the BaseMultiFormsetView into your own view, and set
  the AVAILABLE_FORMS attribute on your class to a tuple of form
  classes that you wish to use.  For example::

      from multiformset.views import BaseMultiFormsetView

      from forms import PizzaForm, BurgerForm


      class MyFavoriteFoodsView(BaseMultiFormsetView):
          AVAILABLE_FORMS = (
              PizzaForm,
              BurgerForm,
          )

3. Setup a URLPattern to your view, like this::

      from myapp.views import MyVavoriteFoodsView

      url(r'^foods/$', MyFavoriteFoodsView.as_view()),

4. Start the development server and visit http://127.0.0.1:8000/foods/
