from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from .models import CompoundForExperiments
from .forms import CompoundForExperimentsForm
from .views import check_password_valid

@login_required()
def add_exp_cmpd(request):
    check_password_valid(request)

    if not request.user.has_perm('chembase.add_compound'):
        return redirect('/login/?next=%s' % request.path)

    if request.method == 'POST':
        form = CompoundForExperimentsForm(request.POST)
    else:
        form = CompoundForExperimentsForm()

    return render(request, 'chembase/add_exp_cmpd.html', {'form': form})

