from flask import render_template,  Blueprint

help = Blueprint('help', __name__)


#########################################
@help.route('/help/help_index')
def help_index():
	return render_template('help/help.html')


@help.route('/help/checklist')
def checklist():
	return render_template('help/checklist.html')


#########################################
@help.route('/help/cons_examples_intro')
def cons_examples_intro():
	return render_template('help/worked_examples/cons_examples_intro.html')


#########################################
@help.route('/help/cons_example/<string:name>/<string:page>')
def cons_example(name, page):
	# page is either instructions or results
	name = name.lower()
	if name == 'hppd_no_structure':
		return render_template(f"help/worked_examples/cons_example_HPPD_no_structure/{page}.html")
	elif name == 'hppd_w_structure':
		return render_template(f"help/worked_examples/cons_example_HPPD_w_structure/{page}.html")
	else: # ACE2 is default; as of this writing it has only results page
		return render_template('help/worked_examples/cons_example_ACE2/results.html')


#########################################
@help.route('/help/spec_examples_intro')
def spec_examples_intro():
	return render_template('help/worked_examples/spec_examples_intro.html')


#########################################
@help.route('/help/spec_example/<string:name>/<string:page>')
def spec_example(name, page):
	# page is either instructions or results
	return render_template(f"help/worked_examples/spec_example_{name}/{page}.html")

#########################################
@help.route('/help/input/<string:input_type>')
def input(input_type):
	# input_type: alignment, annotation, sequences, sequence_families, structure
	return render_template(f"help/input/{input_type}.html")


#########################################
@help.route('/help/output/<string:output_type>')
def output(output_type):
	# output_type: pymol  workdir xls
	return render_template(f"help/output/{output_type}.html")


#########################################
@help.route('/help/viewers/<string:viewer_type>')
def viewers(viewer_type):
	# output_type: alignment  structure
	return render_template(f"help/viewers/{viewer_type}.html")


#########################################
# it looks like the route name and the function name must match
# even though the manual does not say so
@help.route('/help/topics/<string:topic>')
def topics(topic):
	# topic: cons_why on_comparative_analysis  spec_why  which_species why_get_seqs
	return render_template(f"help/topics/{topic}.html")



