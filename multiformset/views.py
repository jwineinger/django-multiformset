from django.forms.formsets import formset_factory, all_valid
from django.http import HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.views.generic import TemplateView


class BaseMultiFormsetView(TemplateView):
	template_name = 'multiformset/add.html'
	AVAILABLE_FORMS = ()

	def get_available_forms(self):
		"""
		Returns a tuple of form classes to be used for formset creation. Can
		be used to filter the list of forms or adjust ordering.
		"""
		return self.AVAILABLE_FORMS

	def get_formset_class(self, form_class, **kwargs):
		"""
		Creates a formset class from a form class. If 'extra' is not passed as
		keyword argument, then it will be set to zero so that no initial forms
		are displayed for any formset.
		"""
		formset_kwargs = dict(kwargs)
		formset_kwargs['extra'] = formset_kwargs.get('extra', 0)
		return formset_factory(form_class, **formset_kwargs)

	def get_formset(self, formset_class, prefix, initial=None):
		"""
		Gets a formset instance from a formset class, optionally binding POST
		and FILES if they are set.  Additionally, the formset prefix to use
		and any initial data for the formset can be set.
		"""
		return formset_class(
			data=self.get_formset_data(),
			files=self.get_formset_files(),
			prefix=prefix,
			initial=initial,
		)

	def get_formset_data(self):
		"""
		Method used to get the 'data' for creating formset instances.
		"""
		return self.request.POST or None

	def get_formset_files(self):
		"""
		Method used to get the 'files' for creating formset instances.
		"""
		return self.request.FILES or None

	def get_initial(self, form_class):
		"""
		Intended to be overridden by views that subclass this one. Users can
		use the form_class argument to look up any initial data that should
		be given to the formset initializer.  You must do this for "edit"
		views.
		"""
		return None

	def get_form_template_name(self, form_class):
		"""
		Method that tries to find a template specific to a form class so that
		users can provide custom renderings easily. If a template is found, it
		will be used for both initial forms and the blank "template" form. If
		no template is found, then the forms will be rendered using the as_p()
		method.
		"""
		try:
			templates = ['multiformset/forms/%s.html' % form_class.__name__]
			template = select_template(templates)
			return template.name
		except TemplateDoesNotExist:
			return None

	def get_formsets(self):
		"""
		Method to get a list of all of the formsets for the request.  Called by
		both get() and post().
		"""
		formsets = []
		for form_class in self.get_available_forms():
			formset_class = self.get_formset_class(form_class)
			formset = self.get_formset(
				formset_class,
				form_class.__name__,
				initial=self.get_initial(form_class),
			)
			formset.template_name = self.get_form_template_name(form_class)
			formsets.append(formset)
		return formsets

	def post(self, request, *args, **kwargs):
		"""
		Handles POST requests.  Gets formsets and validates them.  If all are
		valid then it passes the formsets list to the all_valid() method for
		processing/saving.  If validation fails, the page is re-rendered with
		the formset instances that failed validation.
		"""
		formsets = self.get_formsets()

		if all_valid(formsets):
			return self.all_valid(formsets)
		else:
			context = {'formsets': formsets}
			return self.render_to_response(self.get_context_data(**context))

	def get_context_data(self, **kwargs):
		"""
		Gets the context data for GET requests and for POST requests that fail
		validation.

		Override this if you need to include additional forms in your page. You
		will need to override post() as well to validate and pass the
		additional forms to the all_valid() method as well.
		"""
		context = super(BaseMultiFormsetView, self).get_context_data(**kwargs)

		context.update({
			'formsets': kwargs.get('formsets') or self.get_formsets(),
		})
		return context

	def all_valid(self, formsets, **kwargs):
		"""
		Called when all formsets are valid.  This method should be used to do
		any processing/saving of the form data.

		Subclasses can use kwargs to pass other data (such as additional form
		instances).
		"""
		return HttpResponseRedirect(self.request.get_full_path())