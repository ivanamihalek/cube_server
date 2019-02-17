from flask import render_template,  Blueprint

help = Blueprint('help', __name__)

@help.route('/help/aligning_seqs')
def aligning_seqs():
    return render_template('help/aligning_seqs.html')

@help.route('/help/checklist')
def checklist():
    return render_template('help/checklist.html')

@help.route('/help/cons_why')
def cons_why():
    return render_template('help/cons_why.html')


@help.route('/help/getting_annotation')
def getting_annotation():
    return render_template('help/getting_annotation.html')

@help.route('/help/getting_groups_of_seqs')
def getting_groups_of_seqs():
    return render_template('help/getting_groups_of_seqs.html')

@help.route('/help/getting_seqs')
def getting_seqs():
    return render_template('help/getting_seqs.html')

@help.route('/help/getting_structure')
def getting_structure():
    return render_template('help/getting_structure.html')

@help.route('/help/help_index')
def help_index():
    return render_template('help/help.html')


@help.route('/help/on_comparative_analysis')
def on_comparative_analysis():
    return render_template('help/on_comparative_analysis.html')


@help.route('/help/pymol_output')
def pymol_output():
    return render_template('help/pymol_output.html')

@help.route('/help/spec_why')
def spec_why():
    return render_template('help/spec_why.html')


@help.route('/help/viewing_alignment')
def viewing_alignment():
    return render_template('help/viewing_alignment.html')

@help.route('/help/viewing_structure')
def viewing_structure():
    return render_template('help/viewing_structure.html')


@help.route('/help/which_species')
def which_species():
    return render_template('help/which_species.html')


@help.route('/help/why_get_seqs')
def why_get_seqs():
    return render_template('help/why_get_seqs.html')

@help.route('/help/workdir_output')
def workdir_output():
    return render_template('help/workdir_output.html')


@help.route('/help/xls_output')
def xls_output():
    return render_template('help/xls_output.html')


@help.route('/help/worked_examples/spec_examples')
def xls_output():
    return render_template('help/worked_examples/spec_examples.html')
