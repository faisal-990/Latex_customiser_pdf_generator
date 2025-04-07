import re


def extract_components(tex_file):
    # This now captures the full command including arguments
    pattern = r"\\(section|subsection|rowcolor|begin|end)({[^}]*}|\[[^\]]*\])?"
    return re.findall(pattern, tex_file)
