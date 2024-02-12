from controllers.scrap_texts.remove_single_header_reverse import remove_single_header_reverse
from controllers.scrap_texts.remove_multiple_footer import remove_multiple_footer
from controllers.scrap_texts.remove_single_header import remove_single_header
from controllers.scrap_texts.remove_single_footer import remove_single_footer
from controllers.scrap_texts.remove_single_footer_reverse import remove_single_footer_reverse
import os
from dotenv import load_dotenv

load_dotenv()

header = os.getenv("HEADER")
footer = os.getenv("FOOTER")
subfooter = os.getenv("SUBFOOTER")

h_experts = os.getenv("H_EXPERTS")
f_experts = os.getenv("F_EXPERTS")

substring = os.getenv("SUBSTRING")
spfooter = os.getenv("SPFOOTER")
spfooter2 = os.getenv("SPFOOTER2")

def advanced_filters(isActive, url, file_path):
    """
    Apply advanced filters to the given file based on the URL.

    Args:
        isActive (bool): Indicates whether the advanced filters should be applied.
        url (str): The URL to determine which filters to apply.
        file_path (str): The path to the file to be filtered.

    Returns:
        None

    Examples:
        >>> advanced_filters(True, "scalian.com/es/experts", "path/to/file")
        # Applies filters for experts page
        >>> advanced_filters(False, "scalian.com/es/nuestro-grupo/gobernanza", "path/to/file")
        # Does not apply any filters
    """
    
    if not isActive:
        return
    if "scalian.com/es/experts" in url:
        remove_single_header(file_path, h_experts)
        remove_single_footer(file_path, f_experts)
    elif "scalian.com/es/nuestro-grupo/gobernanza" in url:
        remove_single_header(file_path, h_experts)
        remove_single_footer(file_path, substring)
        remove_single_footer_reverse(file_path, spfooter2)
    elif "scalian.com/es" in url:
        remove_single_header(file_path, h_experts)
        remove_single_footer(file_path, substring)
        remove_single_footer_reverse(file_path, spfooter)
    elif "scalian-spain" in url:
        remove_single_header_reverse(file_path, header)
        remove_multiple_footer(file_path, footer, subfooter)