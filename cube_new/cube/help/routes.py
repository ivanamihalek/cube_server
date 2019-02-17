from flask import render_template,  Blueprint

help = Blueprint('help', __name__)

@help.route('/cons_why')
def cons_why():
    return render_template('help/cons_why.html')

@help.route('/spec_why')
def spec_why():
    return render_template('help/spec_why.html')


'''
@help.route('/aligning_seqs')
def aligning_seqs():
    return render_template('help/aligning_seqs.html')

@help.route('/checklist')
def checklist():
    return render_template('help/checklist.html')

@help.route('/cons_why')
def cons_why():
    return render_template('help/cons_why.html')

@help.route('/getting_annotation')
def getting_annotation():
    return render_template('help/getting_annotation.html')

@help.route('/getting_groups_of_seqs')
def getting_groups_of_seqs():
    return render_template('help/getting_groups_of_seqs.html')

@help.route('/getting_seqs')
def getting_seqs():
    return render_template('help/getting_seqs.html')

@help.route('/getting_structure')
def getting_structure():
    return render_template('help/getting_structure.html')

@help.route('/help')
def help():
    return render_template('help/help.html')

@help.route('/on_comparative_analysis')
def on_comparative_analysis():
    return render_template('help/on_comparative_analysis.html')

@help.route('/pymol_output')
def pymol_output():
    return render_template('help/pymol_output.html')

@help.route('/spec_why')
def spec_why():
    return render_template('help/spec_why.html')

@help.route('/viewing_alignment')
def viewing_alignment():
    return render_template('help/viewing_alignment.html')

@help.route('/viewing_structure')
def viewing_structure():
    return render_template('help/viewing_structure.html')

@help.route('/which_species')
def which_species():
    return render_template('help/which_species.html')

@help.route('/why_get_seqs')
def why_get_seqs():
    return render_template('help/why_get_seqs.html')

@help.route('/workdir_output')
def workdir_output():
    return render_template('help/workdir_output.html')

@help.route('/xls_output')
def xls_output():
    return render_template('help/xls_output.html')

'''