"""For every inference-rule in the punctilious package,
generate the restructured text documentation page.
"""

import jinja2
import os

file_loader = jinja2.FileSystemLoader('../jinja_templates')
env = jinja2.Environment(loader=file_loader)
script_path = os.getcwd()
script_name = os.path.basename(__file__)
ci_path = os.path.abspath(os.path.join(script_path, os.pardir))
project_path = os.path.abspath(os.path.join(ci_path, os.pardir))
math_path = os.path.abspath(os.path.join(project_path, 'docs', 'source', 'math', 'inference_rule'))
math_template = env.get_template('inference_rule_math_template.jinja2')
python_path = os.path.abspath(os.path.join(project_path, 'docs', 'source', 'python', 'class'))
declaration_python_class_template = env.get_template(
    'inference_rule_declaration_python_class_template.jinja2')
inclusion_python_class_template = env.get_template(
    'inference_rule_inclusion_python_class_template.jinja2')

inference_rules = ['absorption', 'biconditional-elimination-1', 'biconditional-elimination-2',
    'biconditional-introduction', 'conjunction-elimination-1', 'conjunction-elimination-2',
    'conjunction-introduction', 'disjunction-introduction-1', 'disjunction-introduction-2',
    'double-negation-elimination', 'double-negation-introduction', 'equal-terms-substitution',
    'equality-commutativity', 'inconsistency-introduction-1', 'inconsistency-introduction-2',
    'inconsistency-introduction-3', 'modus-ponens', 'proof-by-contradiction-1',
    'proof-by-contradiction-2', 'proof-by-refutation-1', 'proof-by-refutation-2',
    'variable-substitution']

for ir in inference_rules:
    dashed_name = ir
    underscored_name = ir.replace("-", "_")
    pascalcased_name = ir.replace("_", " ").title().replace(" ", "")
    print(f'Generate: {ir}')
    filename = f'{underscored_name}_math_inference_rule.rst'
    file_path = os.path.abspath(os.path.join(math_path, filename))
    rst_file_content = math_template.render(script_name=script_name, dashed_name=dashed_name,
        underscored_name=underscored_name, pascalcased_name=pascalcased_name)
    with open(file_path, 'w') as f:
        f.write(rst_file_content)
    filename = f'{underscored_name}_declaration_python_class.rst'
    file_path = os.path.abspath(os.path.join(python_path, filename))
    rst_file_content = declaration_python_class_template.render(script_name=script_name,
        dashed_name=dashed_name, underscored_name=underscored_name,
        pascalcased_name=pascalcased_name)
    with open(file_path, 'w') as f:
        f.write(rst_file_content)
    filename = f'{underscored_name}_inclusion_python_class.rst'
    file_path = os.path.abspath(os.path.join(python_path, filename))
    rst_file_content = inclusion_python_class_template.render(script_name=script_name,
        dashed_name=dashed_name, underscored_name=underscored_name,
        pascalcased_name=pascalcased_name)
    with open(file_path, 'w') as f:
        f.write(rst_file_content)
