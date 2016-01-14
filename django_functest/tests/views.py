from django.shortcuts import render


def test1(request):
    return render(request, "django_functest/tests/test1.html", {})
