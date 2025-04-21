# author @realyn
import requests
import os

CONFIG = {
    "conversions": [
        {
            "input_url": "https://gist.githubusercontent.com/ddgksf2013/12ef6aad209155e7eb62c5b00c11b9dd/raw/StartUpAds.conf",
            "output_file": "Adblock/StartUpAds.plugin",
            "name": "墨鱼去开屏2.0",
            "desc": "Converted from QX StartUp AdBlock Rules"
        }
    ]
}

def convert_to_loon(qx_content, name, desc, input_url):
    loon_content = f"#!name={name}\n"
    loon_content += f"#!desc={desc}\n"
    loon_content += f"#!author=ddgksf2013\n"
    loon_content += f"#!tgchannel=https://t.me/ddgksf2021\n"
    loon_content += f"# Loon Plugin Source: https://github.com/ddgksf2013/Plugins\n"
    loon_content += f"# Original QX Config Source: {input_url}\n\n"
    
    sections = {
        "Rewrite": [],
        "Map Local": [],
        "Script": [],
        "MITM": []
    }
    
    current_section = None
    last_comment = ""  
    for line in qx_content.split('\n'):
        stripped_line = line.strip()
        if not stripped_line:
            continue  
        

        if stripped_line.startswith('hostname = '):
            sections["MITM"].append(stripped_line)
            continue
        

        if stripped_line.startswith('#') or stripped_line.startswith(';'):
            last_comment = stripped_line
            continue
        
        if "reject" in stripped_line:
            parts = stripped_line.split()
            if len(parts) >= 2:
                if last_comment:  
                    sections["Rewrite"].extend([last_comment, f"{parts[0]} reject"])
                else:
                    sections["Rewrite"].append(f"{parts[0]} reject")

        elif "script-response-body" in stripped_line or "script-request" in stripped_line:
            parts = stripped_line.split()
            if len(parts) >= 4:
                script_type = "http-response" if "script-response-body" in stripped_line else "http-request"
                pattern = parts[0]
                script_path = parts[-1]
                script_name = os.path.basename(script_path).split('.')[0]
                
                script_line = f"{script_type} {pattern} script-path={script_path}"
                if script_type == "http-response":
                    script_line = f"{script_type} {pattern} script-path={script_path}, requires-body=true, tag={script_name}"
                    #script_line = f"{script_name} = type={script_type},pattern={pattern},requires-body=1,max-size=0,script-path={script_path}"
                
                if last_comment:
                    sections["Script"].extend([last_comment, script_line])
                else:
                    sections["Script"].append(script_line)
        
        last_comment = ""  
    
    for section, content in sections.items():
        if content:
            loon_content += f"[{section}]\n" + "\n".join(content) + "\n\n"
    
    return loon_content

def process_file(input_url, output_file, name, desc):
    print(f"Fetching QX content from URL: {input_url}")
    response = requests.get(input_url)
    qx_content = response.text

    print(f"Fetched QX content (first 500 characters):\n{qx_content[:500]}...")
    print(f"Total length of fetched content: {len(qx_content)} characters")

    print("Starting conversion to Loon format...")
    loon_content = convert_to_loon(qx_content, name, desc, input_url)

    print(f"Generated Loon content (first 500 characters):\n{loon_content[:500]}...")
    print(f"Total length of generated Loon content: {len(loon_content)} characters")

    print(f"Attempting to write content to file: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(loon_content)
        print(f"Successfully wrote to {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
    except Exception as e:
        print(f"Error handling file: {e}")
    
    # 添加调试信息
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir()}")

def main():
    for conversion in CONFIG['conversions']:
        process_file(conversion['input_url'], conversion['output_file'], conversion['name'], conversion['desc'])

if __name__ == "__main__":
    main()
