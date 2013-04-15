from django.forms.formsets import formset_factory, all_valid
from django.http import HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.views.generic import TemplateView


class BaseMultiFormsetView(TemplateView):
	template_name = 'multiformset/add.html'
	AVAILABLE_FORMS = ()

	def get_available_forms(self):
		return self.AVAILABLE_FORMS

	def get_formset_class(self, form_class, **kwargs):
		formset_kwargs = dict(kwargs)
		formset_kwargs['extra'] = formset_kwargs.get('extra', 0)
		return formset_factory(form_class, **formset_kwargs)

	def get_formset(self, formset_class, prefix, initial=None):
		return formset_class(
			data=self.request.POST or None,
			files=self.request.FILES or None,
			prefix=prefix,
			initial=initial,
		)

	def get_initial(self, form_class):
		return None

	def get_form_template_name(self, form_class):
		try:
			templates = ['multiformset/forms/%s.html' % form_class.__name__]
			template =select_template(templates)
			return template.name
		except TemplateDoesNotExist:
			return None

	def get_formsets(self):
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
		formsets = self.get_formsets()

		if all_valid(formsets):
			return self.all_valid(formsets)
		else:
			return self.render_to_response({'formsets': formsets})

	def get_context_data(self, **kwargs):
		context = super(BaseMultiFormsetView, self).get_context_data(**kwargs)

		context.update({
			'formsets': self.get_formsets(),
		})
		return context

	def all_valid(self, formsets):
		return HttpResponseRedirect(self.request.get_full_path())