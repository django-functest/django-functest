from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render

from .models import Thing


def test1(request):
    return render(request, "django_functest/tests/test1.html", {})


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = '__all__'


def edit_thing(request, thing_id):
    thing = Thing.objects.get(id=int(thing_id))
    if request.method == "POST":
        thing_form = ThingForm(data=request.POST,
                               instance=thing)
        if thing_form.is_valid():
            thing_form.save()
            return HttpResponseRedirect(reverse('edit_thing', kwargs={'thing_id': thing_id}))
    else:
        thing_form = ThingForm(instance=thing)

    return render(request, "django_functest/tests/edit_thing.html",
                  {'thing_form': thing_form,
                   'thing': thing,
                   })
