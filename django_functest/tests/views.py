from __future__ import absolute_import, print_function, unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import mark_safe

from .models import Thing


def test_misc(request):
    return render(request, "django_functest/tests/test_misc.html",
                  {'name': request.session.get('name', None)})


def set_sess_foo_to_bar(request):
    request.session['foo'] = 'bar'
    return render(request, "django_functest/tests/test_misc.html")


class AddSpacersMixin(object):
    def __init__(self, add_spacers=False, **kwargs):
        super(AddSpacersMixin, self).__init__(**kwargs)
        self.add_spacers = add_spacers

    def as_p(self):
        retval = super(AddSpacersMixin, self).as_p()
        if self.add_spacers:
            # Hack to help test interacting with elements
            # that aren't in view.
            retval = mark_safe(retval.replace('</p>', '</p>' + ('<br>' * 100)))
        return retval


class ThingForm(AddSpacersMixin, forms.ModelForm):
    category = forms.ChoiceField(choices=Thing.CATEGORY_CHOICES,
                                 widget=forms.RadioSelect)

    class Meta:
        model = Thing
        fields = ['name', 'big', 'clever', 'element_type', 'category', 'count', 'description']


class ThingFormWithSelectForCategory(AddSpacersMixin, forms.ModelForm):
    class Meta:
        model = Thing
        fields = ThingForm._meta.fields


# Have separate forms so that we test different form enctype
class ThingFormWithUpload(AddSpacersMixin, forms.ModelForm):
    class Meta:
        model = Thing
        fields = ['name', 'notes_file']


def edit_thing(request, thing_id, with_upload=False):
    thing = Thing.objects.get(id=int(thing_id))
    add_spacers = 'add_spacers' in request.GET
    add_js_delay = int(request.GET.get('add_js_delay', '0'))

    if with_upload:
        form_class = ThingFormWithUpload
        redirect_url = reverse('edit_thing_with_upload', kwargs={'thing_id': thing_id})
    else:
        select_for_category = 'select_for_category' in request.GET
        form_class = ThingFormWithSelectForCategory if select_for_category else ThingForm
        redirect_url = reverse('edit_thing', kwargs={'thing_id': thing_id})

    if request.method == "POST":
        if 'clear' in request.POST:
            thing = Thing(id=thing.id, category=Thing.CATEGORY_MAGMA)
            thing.save()
            return HttpResponseRedirect(reverse('thing_cleared', kwargs={'thing_id': thing_id}))
        else:
            thing_form = form_class(data=request.POST,
                                    files=request.FILES,
                                    instance=thing,
                                    add_spacers=add_spacers)
            if thing_form.is_valid():
                thing_form.save()
                return HttpResponseRedirect(redirect_url)
    else:
        thing_form = form_class(instance=thing,
                                add_spacers=add_spacers)

    return render(request, "django_functest/tests/edit_thing.html",
                  {'thing_form': thing_form,
                   'thing': thing,
                   'add_js_delay': add_js_delay,
                   'upload': with_upload,
                   })


def edit_thing_with_upload(request, thing_id):
    return edit_thing(request, thing_id, with_upload=True)


def list_things(request):
    return render(request, "django_functest/tests/list_things.html",
                  {'things': Thing.objects.all()})


def thing_cleared(request, thing_id):
    thing = Thing.objects.get(id=int(thing_id))
    return render(request, "django_functest/tests/thing_cleared.html",
                  {'thing': thing})
