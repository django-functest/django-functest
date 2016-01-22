from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import mark_safe

from .models import Thing


def test1(request):
    return render(request, "django_functest/tests/test1.html", {})


class ThingForm(forms.ModelForm):
    def __init__(self, add_spacers=False, **kwargs):
        super(ThingForm, self).__init__(**kwargs)
        self.add_spacers = add_spacers

    def as_p(self):
        retval = super(ThingForm, self).as_p()
        if self.add_spacers:
            # Hack to help test interacting with elements
            # that aren't in view.
            retval = mark_safe(retval.replace('</p>', '</p>' + ('<br>' * 100)))
        return retval

    class Meta:
        model = Thing
        fields = '__all__'


def edit_thing(request, thing_id):
    thing = Thing.objects.get(id=int(thing_id))
    add_spacers = 'add_spacers' in request.GET
    add_js_delay = int(request.GET.get('add_js_delay', '0'))

    if request.method == "POST":
        if 'clear' in request.POST:
            thing = Thing(id=thing.id)
            thing.save()
            return HttpResponseRedirect(reverse('edit_thing', kwargs={'thing_id': thing_id}))
        else:
            thing_form = ThingForm(data=request.POST,
                                   instance=thing,
                                   add_spacers=add_spacers)
            if thing_form.is_valid():
                thing_form.save()
                return HttpResponseRedirect(reverse('edit_thing', kwargs={'thing_id': thing_id}))
    else:
        thing_form = ThingForm(instance=thing,
                               add_spacers=add_spacers)

    return render(request, "django_functest/tests/edit_thing.html",
                  {'thing_form': thing_form,
                   'thing': thing,
                   'add_js_delay': add_js_delay,
                   })
