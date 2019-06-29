from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Compound, CompoundForExperiments, Experiment, ProteinTarget, ExperimentType, ExperimentLog, ExtraPermissions
from .forms import CompoundForExperimentsForm, ExperimentForm, ProteinTargetForm, ExperimentTypeForm, ExperimentSearchForm
from .views import check_password_valid


@login_required()
def search_view(request):
    check_password_valid(request)
    print(request.GET)
    if request.GET:
        form = ExperimentSearchForm(request.GET)
        # print(form.cleaned_data)
        #print(request.POST)
        query = request.GET['text']
        query_cas = request.GET['cas']
        query_type = request.GET['exp_type']
        target = request.GET['target']
        smiles = request.GET['smiles']
        stype = request.GET['stype']
        try:
            cut = float(request.GET['cutoff'])
        except ValueError:
            cut = None
        #print(query, query_cas, query_type, target, smiles, stype, cut)
        if smiles != '':
            structure = True
        else:
            structure = False

        result = search(request.user, query, query_cas, 'and', query_type, target, smiles, stype, cut)
        #result = None
        if result:
            found = len(result)
            paginator = Paginator(result, 20)
            page = request.GET.get('page')
            try:
                cmpds_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                cmpds_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                cmpds_list = paginator.page(paginator.num_pages)
        else:
            found = 0
            cmpds_list = []

        cmpd_dict_list = []
        for compound in cmpds_list:
            experiments = compound.experiment_set.all()
            targets = set([item.target for item in experiments])
            exp_dict = []
            for item in targets:
                exp_dict.append((str(item), [{'exp': jtem, 'bc': jtem.print_binding()}
                                             for jtem in experiments.filter(target=item) if not jtem.is_deleted()]))

            cmpd_dict_list.append({'a':compound, 'b':exp_dict})

    else:
        form = ExperimentSearchForm()
        structure = False
        found = 0
        cmpd_dict_list = None
        form.fields['stype'].initial = 'sub'

    return render(request, 'chembase/experiment_search.html',
                  {'form': form, 'results': cmpd_dict_list, 'str': structure, 'found': found,
                   })

def search_ajax(request):
    if request.method == 'POST':
        query_ = request.POST.get('query')
        cut_ = request.POST.get('cutoff')
        result = search(user='abstract_user', query=query_, query_cas=query_, linker='or', cut=float(cut_), dele=True)

        return JsonResponse(
            {item.id: {'name': item.name, 'cas': item.cas, 'subtitle': item.subtitle, 'image': item.image} for item in
             result})

@login_required
def autocomplete_ajax(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = CompoundForExperiments.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.name)

        return JsonResponse(results, safe=False)

@login_required
def search(user, query='', query_cas='', linker='and', query_type='', target='', smiles='', stype='sub', cut=0.6):
    if (query != '' or query_cas != '' or query_type != '' or target != '' or smiles != ''):
        qa = Q()
        qb = Q()
        for item in query.split():
            qa = qa & Q(name__icontains=item)
            qb = qb & Q(all_names__icontains=item)

        q1 = qa | qb

        q2 = Q(cas__icontains=query_cas)

        if query_type:
            q4 = Q(experiment__exp_type__exact=query_type)
        else:
            q4 = Q()

        if target:
            q5 = Q(experiment__target__exact=target)
        else:
            q5 = Q()

        if linker == 'and':
            q = q1 & q2 & q4 & q5
        elif linker == 'or':
            q = q1 | q2
            if query_type:
                q = q | q4
            if target:
                q = q | q5

        found_cmpds = CompoundForExperiments.objects.filter(q).distinct()
        print(found_cmpds)

        if smiles == '':
            if query != '':
                query_to_compare = query
                sorted_cmpds = Compound.extra_methods.sort_by_name_simil(found_cmpds, query_to_compare, 0.001)
            elif query_cas != '':
                query_to_compare = query_cas
                sorted_cmpds = Compound.extra_methods.sort_by_name_simil(found_cmpds, query_to_compare, 0.001)
            else:
                sorted_cmpds = found_cmpds

        else:
            if stype == 'sim':
                sorted_cmpds = Compound.extra_methods.sort_by_str_simil(found_cmpds, smiles, cut)
            else:
                sorted_cmpds = Compound.extra_methods.substr_match(found_cmpds, smiles, cut)

        return sorted_cmpds
    else:
        return None

@login_required()
def cmpd_detail(request, cmpd_id):
    check_password_valid(request)
    user = request.user
    compound = get_object_or_404(CompoundForExperiments, pk=cmpd_id)
    can_edit = compound.can_edit(user)
    can_add = user.has_perm('chembase.add_experiment')

    experiments = compound.experiment_set.all()
    targets = set([item.target for item in experiments])
    exp_dict = []
    for item in targets:
        exp_dict.append((str(item), [{'exp':jtem, 'bc': jtem.print_binding(), 'can_edit': jtem.can_edit(user)}
                                     for jtem in experiments.filter(target=item) if not jtem.is_deleted()]))

    return render(request, 'chembase/experiment_detail.html', {'compound': compound, 'experiments':exp_dict,
                                                               'can_edit':can_edit, 'can_add': can_add})
@login_required()
def add_exp_cmpd(request):
    check_password_valid(request)

    if not request.user.has_perm('chembase.add_experiment'):
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

    if not request.user.has_perm('chembase.add_experiment'):
        return redirect('/login/?next=%s' % request.path)

    if request.method == 'POST':

        save_as = request.POST.get('save_as')
        if save_as == 'new':
            form = CompoundForExperimentsForm(request.POST)
            action = 'add'
        else:
            edited_cmpd = CompoundForExperiments.objects.get(pk=save_as)
            form = CompoundForExperimentsForm(request.POST, instance=edited_cmpd)
            action = 'edit'

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

            user = request.user
            system_log_entry = ExperimentLog(model_name='Compound', model_instance_id=new_cmpd.id,
                                             author=user, action=action, comment='')
            system_log_entry.save()

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
        bc_value, bc_mult, bc_unit = item.format_binding()
        print(bc_value, bc_mult, bc_unit)

        if not item.can_edit(request.user):
            return redirect('/login/?next=%s' % request.path)

        item_form = ExperimentForm(instance=item, initial={'binding_const':bc_value, 'binding_unit':bc_mult})
        #item_form.fields['binding_const'].value = bc_value
        #item_form.fields['binding_unit'].value = bc_mult

        target_form = ProteinTargetForm()
        target_form.fields['target'].initial = item.target

        exp_type_form = ExperimentTypeForm()
        exp_type_form.fields['exp_type'].initial = item.exp_type

    else:
        if not request.user.has_perm('chembase.add_experiment'):
            return redirect('/login/?next=%s' % request.path)

        item_form = ExperimentForm()
        item_id = 'new'

        target_form = ProteinTargetForm()

        exp_type_form = ExperimentTypeForm()

    return render(request, 'chembase/add_experiment.html', {'compound': cmpd, 'form': item_form, 'item_id': item_id,
                                                            'pform': target_form, 'tform': exp_type_form})


@login_required()
def save_exp(request):
    if not request.user.has_perm('chembase.add_experiment'):
        return redirect('/login/?next=%s' % request.path)
    if request.method == 'POST':
        cmpd_id = request.POST.get('cmpd_id')
        cmpd = CompoundForExperiments.objects.get(pk=cmpd_id)

        target_form = ProteinTargetForm(request.POST)
        if target_form.is_valid():
            target = target_form.cleaned_data['target']
        else:
            target_name = request.POST.get('target')
            target = ProteinTarget(target=target_name)
            target.save()

        exp_type_form = ExperimentTypeForm(request.POST)
        if exp_type_form.is_valid():
            exp_type = exp_type_form.cleaned_data['exp_type']
        else:
            exp_type_name = request.POST.get('exp_type')
            exp_type = ExperimentType(exp_type = exp_type_name)
            exp_type.save()

        item_id = request.POST.get('item_id')
        if item_id == 'new':
            form = ExperimentForm(request.POST)
            action = 'add'
        else:
            edited_exp = Experiment.objects.get(pk=item_id)
            if not edited_exp.can_edit(request.user):
                return redirect('/login/?next=%s' % request.path)
            form = ExperimentForm(request.POST, instance=edited_exp)
            action = 'edit'
        if form.is_valid():
            clean = form.cleaned_data
            new_exp = form.save(commit=False)
            new_exp.compoundForExperiments = cmpd
            new_exp.exp_type = exp_type
            new_exp.target = target

            try:
                bconstant = float(clean['binding_const'])*10**(-1*int(clean['binding_unit']))
            except (KeyError, TypeError):
                bconstant = clean['binding_const']
            finally:
                new_exp.binding_const = bconstant

            if item_id == 'new':
                new_exp.author = request.user

            new_exp.save()

            #new_item.compound = cmpd
            #new_item.save()

            ###log
            user = request.user
            system_log_entry = ExperimentLog(model_name='Experiment', model_instance_id=new_exp.id,
                                             author=user, action=action, comment='')
            system_log_entry.save()

        # if item_id == 'new':
        # #    del_item = History(item=new_item, action='added')
        # #    del_item.save()
        #     return redirect('chembase:add_item_done', item_id=new_item.id)
        # else:
        return redirect('chembase:exp_cmpd_detail', cmpd_id=cmpd.id)


@login_required()
def delete_experiment(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')
        exp = Experiment.objects.get(pk=item_id)
        user = request.user
        if exp.can_edit(user):
            exp.delete(user)

        # return JsonResponse({'status':'success'})
        return redirect('chembase:exp_cmpd_detail', cmpd_id=exp.compoundForExperiments.id)


def account_view(request):
    check_password_valid(request)
    return render(request,'chembase/account_exp.html')