import re
from urllib.parse import quote

def convert_github_to_colab(url: str) -> str:
    if not url.startswith('https://github.com/'):
        return url
        
    colab_url = url.replace('https://github.com/', 'https://colab.research.google.com/github/')
    
    # the %2520 is the reason colab doesn't work directly. it's added by url bars when spaces are present in the URL.
    return quote(colab_url, safe='/:?&=').replace('%2520', '%20')

def update_readme(readme_path: str = 'README.md'):
    """
    Reads a README file, finds GitHub notebook links without a Colab badge,
    and adds a badge next to them.
    
    Args:
        readme_path (str): The path to the README file.
    """
    print(f"Reading file: '{readme_path}'...")
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{readme_path}' was not found.")
        print("Please make sure you are running this script in the correct directory.")
        return

    colab_badge_template = ' [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})'
    pattern = re.compile(r'\[([^\]]+)\]\((https:\/\/github\.com\/[^\)]+\.ipynb)\)(?!\s*\[\!\[Open In Colab)', re.IGNORECASE)
    links_updated = []

    def add_badge_if_missing(match: re.Match) -> str:
        original_link_markdown = match.group(0)
        github_url = match.group(2)
        
        print(f"  -> Found notebook link without badge: {github_url}")
        links_updated.append(github_url)
        
        colab_url = convert_github_to_colab(github_url)
        colab_badge = colab_badge_template.format(colab_url=colab_url)
        
        return original_link_markdown + colab_badge

    new_content = pattern.sub(add_badge_if_missing, content)

    if links_updated:
        print(f"\nFound {len(links_updated)} missing badge(s).")
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ README.md has been successfully updated!")
        except IOError as e:
            print(f"Error writing to file '{readme_path}': {e}")
    else:
        print("No missing Colab badges found!")

if __name__ == "__main__":
    update_readme()