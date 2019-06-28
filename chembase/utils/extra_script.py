# -*- coding: utf-8 -*-



## additional script file for generating and saving pictures and data of compounds for PD1 project imported as molfiles.
## to be used only once


from chembase.models import CompoundForExperiments, Experiment, ProteinTarget, ExperimentType
from . import functions

pdl1 = ProteinTarget.objects.filter(target__exact='PD-L1')[0]
nmr = ExperimentType.objects.filter(exp_type__exact='NMR')[0]

for cmpd in CompoundForExperiments.objects.all():
    exp = Experiment(compoundForExperiments=cmpd, target=pdl1, exp_type=nmr)
    exp.save()

# compounds = CompoundForExperiments.objects.all()
# for item in compounds:
#     molfile = item.molfile
#     print(item.id)
#     if not item.image:
#         molecule = functions.Molecule(molfile=molfile)
#         properties = molecule.properties()
#         item.weight = properties['mass']
#         item.smiles = properties['smiles']
#         item.inchi = properties['inchi']
#         item.formula = functions.Molecule.clean_formula(properties['formula'])
#         item.save()
#
#         temp_image_path = molecule.render_image('Exp'+str(item.id))
#         print(temp_image_path)
#         ##remove <<?timestamp=>> ending
#         image_name = temp_image_path.split('?')[0]
#         final_image_name = str(item.name) + '_exp_cmpd_num_' + str(item.id) + '.png'
#
#         file_base = '/home/marcin/Dokumenty/projekty/production/Chem/chembase/static/chembase/images/'
#         image_name_out = file_base + final_image_name
#         print(image_name_out)
#         try:
#             image_data = open('/home/marcin/Dokumenty/projekty/production/Chem/chembase' + image_name,
#                               'rb+').read()
#         except FileNotFoundError:
#             pass
#         else:
#             with open(image_name_out, 'wb+') as destination:
#                 destination.write(image_data)
#             item.image = 'images/' + final_image_name
#             item.save()