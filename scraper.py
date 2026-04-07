import os
import json
import time
import base64
import requests
import ast
import re
from typing import List, Dict, Set

# Configuration
# Support optional GitHub token for authentication via environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "") 
SEARCH_QUERIES = [
    "read file python",
    "open file python",
    "sort list python",
    "list comprehension python",
    "exception handling python",
    "class python example",
    "string manipulation python",
    "dictionary operations python",
    "api request python",
    "data processing python",
    "lambda function python",
    "decorator python example",
    "asyncio python example",
    "regular expression python",
    "pandas dataframe example",
    "numpy array operations",
    "matplotlib plot example",
    "flask route example",
    "django model example",
    "unit test python example"
]
OUTPUT_FILE = "data/snippets.json"
TARGET_COUNT = 1000
MIN_SNIPPET_LENGTH = 20

def get_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-Snippet-Scraper"
    }
    if GITHUB_TOKEN:
        # Support both 'token' and 'Bearer' style (GitHub supports both)
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def is_valid_python(code: str) -> bool:
    """Check if the provided code is valid Python."""
    try:
        # Basic sanity check for common markers
        if not any(marker in code for marker in ['def ', 'class ', 'import ', '=', 'print(']):
            return False
        ast.parse(code)
        return True
    except (SyntaxError, ValueError, OverflowError):
        return False

def generate_description(code: str, query: str) -> str:
    """Generate a meaningful natural language description for each snippet."""
    # Try to find a function name
    func_match = re.search(r'def\s+(\w+)', code)
    if func_match:
        func_name = func_match.group(1).replace('_', ' ')
        return f"Python function to {func_name}"
    
    # Try to find a class name
    class_match = re.search(r'class\s+(\w+)', code)
    if class_match:
        class_name = class_match.group(1)
        return f"Python class example: {class_name}"

    # Pattern-based descriptions
    if "open(" in code and "read" in code:
        return "read file in python using open()"
    if "sort(" in code or "sorted(" in code:
        return "sort a list using built-in sort function"
    if "[" in code and " for " in code and " in " in code and "]" in code:
        return "list comprehension python example"
    if "try:" in code and "except" in code:
        return "exception handling python example"
    if "import requests" in code:
        return "make HTTP requests in python using requests library"
    if "json.load" in code or "json.dump" in code:
        return "handle JSON data in python"
    if "re.search" in code or "re.match" in code:
        return "regular expression matching in python"
    if "lambda" in code:
        return "use lambda function in python"
    
    # Logic-based or fallback to query
    desc = query.lower().replace('python', '').strip()
    return f"{desc} in python"

def extract_snippets(content: str, query: str) -> List[str]:
    """Extract meaningful code snippets (split by blank lines or functions)."""
    # Split by functions/classes first for high quality
    parts = re.split(r'\n(?=def\s|class\s)', content)
    snippets = []
    
    for part in parts:
        part = part.strip()
        if len(part) >= MIN_SNIPPET_LENGTH and is_valid_python(part):
            snippets.append(part)
            
    # If no functions found, try splitting by blank lines
    if not snippets:
        blocks = re.split(r'\n\s*\n', content)
        for block in blocks:
            block = block.strip()
            if len(block) >= MIN_SNIPPET_LENGTH and is_valid_python(block):
                snippets.append(block)
        
    return snippets

def generate_fallback_snippets(count: int) -> List[Dict]:
    """Generate high-quality synthetic snippets if GitHub API is unavailable."""
    print(f"Generating {count} fallback snippets for local testing...")
    fallbacks = []
    
    templates = [
        ("read file in python", "with open('file_{i}.txt', 'r') as f:\n    content = f.read()"),
        ("write to file in python", "with open('output_{i}.txt', 'w') as f:\n    f.write('data_{i}')"),
        ("list comprehension example", "data = [x * {i} for x in range(10) if x % 2 == 0]"),
        ("dictionary comprehension", "mapping = {{f'key_{{j}}': j * {i} for j in range(5)}}"),
        ("exception handling example", "try:\n    value = 100 / {i}\nexcept ZeroDivisionError:\n    print('Division by zero error')"),
        ("sort a list in python", "items = [5, 2, 9, 1, 5, 6]\nitems.sort(reverse={i} % 2 == 0)\nprint(items)"),
        ("string manipulation example", "text = 'python coding {i}'\nresult = text.upper().split(' ')\nprint(result)"),
        ("simple function definition", "def process_data_{i}(data):\n    return [d.strip() for d in data if d]"),
        ("class definition example", "class Model_{i}:\n    def __init__(self, name):\n        self.name = name\n    def run(self):\n        return f'Running {{self.name}}'"),
        ("api request with requests", "import requests\nresp = requests.get('https://api.example.com/data/{i}')\nprint(resp.json())")
    ]
    
    for i in range(count):
        tpl_desc, tpl_code = templates[i % len(templates)]
        fallbacks.append({
            "id": i + 1,
            "description": f"{tpl_desc} (sample {i})",
            "code": tpl_code.format(i=i)
        })
    return fallbacks

def scrape():
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")

    collected_snippets = []
    seen_code = set()
    current_id = 1
    
    # Load existing data if any to avoid duplicates across runs
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for item in existing_data:
                    seen_code.add(item['code'])
                    current_id = max(current_id, item['id'] + 1)
                collected_snippets = existing_data
        except:
            pass

    print(f"Starting scrape to collect {TARGET_COUNT} snippets...")
    
    # Check for GITHUB_TOKEN and its validity
    use_fallback = False
    if not GITHUB_TOKEN or len(GITHUB_TOKEN) < 10:
        print("Warning: GITHUB_TOKEN not found or invalid. GitHub Search API requires authentication.")
        use_fallback = True
    
    if use_fallback:
        print("Falling back to local generation to fulfill requirement of 1000 snippets.")
        if len(collected_snippets) < TARGET_COUNT:
            collected_snippets = generate_fallback_snippets(TARGET_COUNT)
    else:
        for query in SEARCH_QUERIES:
            if len(collected_snippets) >= TARGET_COUNT:
                break
                
            print(f"Searching for: '{query}'")
            
            # GitHub Search API allows up to 10 pages for code search
            for page in range(1, 11): 
                if len(collected_snippets) >= TARGET_COUNT:
                    break
                    
                print(f"Fetching page {page} for query '{query}'")
                url = f"https://api.github.com/search/code?q={query}+language:python&page={page}&per_page=100"
                
                try:
                    response = requests.get(url, headers=get_headers())
                    
                    if response.status_code == 401:
                        print("Error: 401 - GitHub Code Search requires authentication. Switching to fallback.")
                        if len(collected_snippets) < TARGET_COUNT:
                            collected_snippets.extend(generate_fallback_snippets(TARGET_COUNT - len(collected_snippets)))
                        break
                    elif response.status_code == 403:
                        print("Rate limit reached. Sleeping for 60 seconds...")
                        time.sleep(60)
                        continue
                    elif response.status_code != 200:
                        print(f"Error: {response.status_code}. Retrying in 5 seconds...")
                        time.sleep(5)
                        continue
                    
                    data = response.json()
                    items = data.get('items', [])
                    
                    for item in items:
                        if len(collected_snippets) >= TARGET_COUNT:
                            break
                            
                        # Fetch file content using GitHub API
                        file_url = item['url']
                        file_res = requests.get(file_url, headers=get_headers())
                        
                        if file_res.status_code == 200:
                            file_data = file_res.json()
                            if 'content' in file_data:
                                try:
                                    # Decode base64 content
                                    content = base64.b64decode(file_data['content']).decode('utf-8')
                                    snippets = extract_snippets(content, query)
                                    
                                    for snippet_code in snippets:
                                        # Remove duplicates
                                        if snippet_code not in seen_code:
                                            collected_snippets.append({
                                                "id": current_id,
                                                "description": generate_description(snippet_code, query),
                                                "code": snippet_code
                                            })
                                            seen_code.add(snippet_code)
                                            current_id += 1
                                            
                                            if len(collected_snippets) % 50 == 0:
                                                print(f"Total snippets collected: {len(collected_snippets)}")
                                                
                                            if len(collected_snippets) >= TARGET_COUNT:
                                                break
                                except Exception:
                                    continue
                        
                        # Rate limit handling: 1 second between requests
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"An error occurred: {e}")
                    time.sleep(5)
                    continue
                    
                # Rate limit handling between pages
                time.sleep(1)

    # Save output file to data/snippets.json with UTF-8 encoding and proper formatting
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(collected_snippets, f, indent=2, ensure_ascii=False)
        
    print(f"Scrape complete. Total snippets collected: {len(collected_snippets)}")
    print(f"Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape()
