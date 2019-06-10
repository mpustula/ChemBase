from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from .models import CompoundForExperiments, Experiment, ProteinTarget, ExperimentType
from .forms import CompoundForExperimentsForm, ExperimentForm, ProteinTargetForm, ExperimentTypeForm
from .views import check_password_valid


@login_required()
def cmpd_detail(request, cmpd_id):
    check_password_valid(request)
    can_edit = True
    can_add = True

    compound = get_object_or_404(CompoundForExperiments, pk=cmpd_id)

    return render(request, 'chembase/experiment_detail.html', {'compound': compound, 'can_edit':can_edit, 'can_add': can_add})


@login_required()
def add_exp_cmpd(request):
    check_password_valid(request)

    if not request.user.has_perm('chembase.add_compound'):
        return redirect('/login/?next=%s' % request.path)

    if request.method == 'POST':
        rtype = request.POST.get('type')
        if rtype == 'edit':
            cmpd_id = request.POST.get('cmpd_id')
            compound = CompoundForExperiments.objects.get(pk=cmpd_id)
            str_image = '/static/chembase/' + compound.image
            form = CompoundForExperimentsForm(instance = compound)
            save_as=cmpd_id
        else:
            form = CompoundForExperimentsForm(request.POST)
            str_image = ''
            save_as='new'
    else:
        form = CompoundForExperimentsForm()
        str_image = ''
        save_as = 'new'

    return render(request, 'chembase/add_exp_cmpd.html', {'form': form, 'structure_im':str_image,'save_as':save_as})


@login_required()
def save_exp_cmpd(request):

    if not request.user.has_perm('chembase.add_compound'):
        return redirect('/login/?next=%s' % request.path)

    if request.method == 'POST':

        save_as = request.POST.get('save_as')
        if save_as == 'new':
            form = CompoundForExperimentsForm(request.POST)
        else:
            edited_cmpd = CompoundForExperiments.objects.get(pk=save_as)
            form = CompoundForExperimentsForm(request.POST, instance=edited_cmpd)

        if form.is_valid():
            new_cmpd = form.save(commit=False)
            if save_as == 'new':
                user = request.user
                new_cmpd.author = user
            new_cmpd.save()

            ##remove <<?timestamp=>> ending
            image_name = (request.POST['image']).split('?')[0]
            final_image_name = str(new_cmpd.name)+'_exp_cmpd_num_' + str(new_cmpd.id) + '.png'

            file_base = '/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/images/'
            image_name_out = file_base + final_image_name
            try:
                image_data = open('/home/marcin/Dokumenty/projekty/production/Chem/chembase' + image_name,
                                  'rb+').read()
            except FileNotFoundError:
                pass
            else:
                with open(image_name_out, 'wb+') as destination:
                    destination.write(image_data)
                new_cmpd.image = 'images/' + final_image_name
                new_cmpd.save()

            return redirect('chembase:exp_cmpd_detail', new_cmpd.id)

    else:
        form = CompoundForExperimentsForm()
        return render(request, 'chembase/add_exp_cmpd.html', {'form': form})


@login_required()
def add_experiment(request, cmpd_id):
    check_password_valid(request)
    cmpd = CompoundForExperiments.objects.get(pk=cmpd_id)
    rtype = request.POST.get('type')
    if rtype == 'edit':
        item_id = request.POST.get('item_id')
        item = Experiment.objects.get(pk=item_id)

        #if not item.is_allowed(request.user, 'chembase.change_item'):
        #    return redirect('/login/?next=%s' % request.path)

        #comment_list = item.annotation_set.all()
        #if comment_list:
        #    comment = comment_list[0].annotation
        #else:
        #    comment = ''
        item_form = ExperimentForm(instance=item)
        #item_form.fields['comment'].initial = comment
        #room_init = item.room
        #place_init = item.place
        #place_num_init = item.place_num
        # owner_group_choices=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='add_item')
        #owner_group_choices = ExtraPermissions.permitted_groups(request.user, 'chembase.add_item')
        # print(owner_group_choices)
        # choices=((item.owner.id,item.owner.name),((item.group.id,item.group.name) for item in owner_group_choices))
        # choices.append(((item.group.id,item.group.name) for item in owner_group_choices))
        #item_form.fields['owner'].choices = ((item.id, item.name) for item in owner_group_choices)
        #if not ExtraPermissions.check_perm(request.user, 'chembase.add_item', item.owner):
        #    item_form.fields['owner'].choices.append((item.owner.id, item.owner.name))


    else:
        #if not can_add_item(request.user):
        #    return redirect('/login/?next=%s' % request.path)

        item_form = ExperimentForm()
        item_id = 'new'
        #room_init = ''
        #place_init = ''
        #place_num_init = ''
        # owner_group_choices=ExtraPermissions.objects.filter(user__exact=request.user,permission__codename__exact='add_item')
        #owner_group_choices = ExtraPermissions.permitted_groups(request.user, 'chembase.add_item')
        # print(owner_group_choices)
        #item_form.fields['owner'].choices = ((item.id, item.name) for item in owner_group_choices)


    return render(request, 'chembase/add_experiment.html', {'compound': cmpd, 'form': item_form, 'item_id': item_id})




