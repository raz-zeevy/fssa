import re
import datetime
import sys

def update_html_version(version):
    try:
        with open('docs/index.html', 'r', encoding='utf-8') as file:
            content = file.read()
            
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # Update version
        content = re.sub(r'<td>v[\d\.]+</td>', f'<td>v{version}</td>', content)
        # Update date
        content = re.sub(r'<td>\d{4}-\d{2}-\d{2}</td>', f'<td>{today}</td>', content)
        
        with open('docs/index.html', 'w', encoding='utf-8') as file:
            file.write(content)
            
        print(f"Successfully updated HTML with version {version} and date {today}")
        
    except Exception as e:
        print(f"Error updating HTML: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_html.py <version>")
        sys.exit(1)
    
    update_html_version(sys.argv[1]) 