import sys
import os
import inspect
import docutils
import docutils.statemachine
import docutils.parsers.rst
import docutils.nodes

sys.path.append(os.path.abspath("../"))

PATH_TO_SRC = os.path.abspath("./source")

# MODULE TO CONFIGURE
import deeptrack
import deeptrack.backend


def parse_class_docstring(class_obj):
    """Parse the docstring of a class using docutils.parsers.rst.

    Parameters
    ----------
    class_obj : class
        The class to parse the docstring from.

    Returns
    -------
    dict
        A dictionary containing the sections of the parsed docstring.
    """
    docstring = inspect.getdoc(class_obj)
    if docstring is None:
        return {}

    # Parse the docstring using docutils.parsers.rst
    parser = docutils.parsers.rst.Parser()
    settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)
    ).get_default_values()
    document = docutils.utils.new_document("<docstring>", settings=settings)
    parser.parse(docstring, document)

    # Extract the sections. Text before the first section is put in the body section.
    sections = {"body": []}
    section_names = ["body"]

    for node in document.children:

        # Ignore system messages
        if isinstance(node, docutils.nodes.system_message):
            continue

        if isinstance(node, docutils.nodes.section):
            # Get the name of the section and add it to the list of sections
            section_name = node.children[0].astext()
            section_names.append(section_name)
            sections[section_name] = []

        # Add the node to the current section
        sections[section_names[-1]].append(parse_node(node))

    return {
        "sections": sections,
    }


def parse_node(node) -> str:
    """Parse a docutils node to a dictionary containing the type of node and its contents.

    Parameters
    ----------
    node : docutils.nodes.Node
        The node to parse.

    Returns
    -------
    dict
        A dictionary containing the parsed node.
    """
    # Get the node type
    node_type = type(node).__name__

    # Get the node children
    children = []
    for child in node.children:
        children.append(parse_node(child))

    # Get the node content
    content = node.astext()
    if node_type == "Text":
        return {
            "type": node_type,
            "content": content,
        }
    else:
        return {
            "type": node_type,
            "children": children,
        }


output_data = {}

# Find all submodules of deeptrack
submodules = [
    obj for name, obj in inspect.getmembers(deeptrack) if inspect.ismodule(obj)
]

# Exclude modules that are not submodules of deeptrack
submodules = [obj for obj in submodules if obj.__name__.startswith("deeptrack.")]

# Recursively find all submodules of submodules
max_depth = 3
for _ in range(max_depth):
    for submodule in submodules:
        nested_submodules = [
            obj for name, obj in inspect.getmembers(submodule) if inspect.ismodule(obj)
        ]
        # exclude modules that are not submodules of deeptrack
        nested_submodules = [
            obj
            for obj in nested_submodules
            if obj.__name__.startswith("deeptrack.") and obj not in submodules
        ]
        submodules.extend(nested_submodules)

output_data["submodules"] = [submodule.__name__ for submodule in submodules]

for submodule in submodules:

    # Find all classes in submodule
    classes = [
        obj for name, obj in inspect.getmembers(submodule) if inspect.isclass(obj)
    ]

    # Exclude classes that are not classes in submodule
    classes = [obj for obj in classes if obj.__module__ == submodule.__name__]

    # Find all functions in submodule
    functions = [
        obj for name, obj in inspect.getmembers(submodule) if inspect.isfunction(obj)
    ]

    # Exclude functions that are not functions in submodule
    functions = [obj for obj in functions if obj.__module__ == submodule.__name__]

    output_data[submodule.__name__] = {
        "classes": {},
        "functions": {},
        "docstring": parse_class_docstring(submodule),
    }

    # Add the documenation for the classes
    for obj in classes:

        doc = parse_class_docstring(obj)

        # Add the qualified name of the superclass
        if obj.__bases__:
            superclass = obj.__bases__[0].__name__
            doc["superclass"] = superclass

        # Add the qualified name of the module of the superclass
        if obj.__bases__:
            superclass_module = obj.__bases__[0].__module__
            doc["superclass_module"] = superclass_module

        # Add the qualified name of the module of the class
        doc["module"] = obj.__module__

        # Add the name of the class
        doc["name"] = obj.__name__

        # Add the qualified name of the class
        doc["qualified_name"] = obj.__module__ + "." + obj.__name__

        # Find the signature of the constructor

        signature = inspect.signature(obj.__init__)
        # remove type annotations
        signature = signature.replace(return_annotation=inspect.Parameter.empty)

        # Remove the self argument
        signature = signature.replace(
            parameters=[p for p in list(signature.parameters.values())[1:]]
        )

        doc["signature"] = str(signature)

        # Add the documenation for the class
        output_data[submodule.__name__]["classes"][obj.__name__] = doc

    # Add the documenation for the functions
    for obj in functions:

        doc = parse_class_docstring(obj)

        # Add the qualified name of the module of the function
        doc["module"] = obj.__module__

        # Add the name of the function
        doc["name"] = obj.__name__

        # Add the qualified name of the function
        doc["qualified_name"] = obj.__module__ + "." + obj.__name__

        # Add the documenation for the function
        output_data[submodule.__name__]["functions"][obj.__name__] = doc

# Save the output data as JSON
import json

with open(os.path.abspath("./data.json"), "w") as f:
    json.dump(output_data, f)