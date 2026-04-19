import json
import re
from pathlib import Path

def is_ipv4(val):
    return re.match(r'^\d+\.\d+\.\d+\.\d+$', val) is not None

def parse_ipconfig(filename, text):
    adapters = []
    sections = re.split(r'\n(?=[a-zA-Z].*adapter.*:)', text)
    
    for section in sections:
        lines = section.strip().splitlines()
        if not lines or "adapter" not in lines[0].lower():
            continue
            
        adapter = {
            "adapter_name": lines[0].strip(": "),
            "description": "", "physical_address": "", "dhcp_enabled": "",
            "ipv4_address": "", "subnet_mask": "", "default_gateway": "",
            "dns_servers": []
        }
        
        current_key = None
        for line in lines[1:]:
            if " . . . . . . . . . . . :" in line:
                key_part, val_part = line.split(":", 1)
                key = key_part.replace(".", "").strip().lower()
                val = re.sub(r'\(.*?\)', '', val_part).strip()
                
                current_key = None

                if "description" in key:
                    adapter["description"] = val

                elif "physical address" in key:
                    adapter["physical_address"] = val

                elif "dhcp enabled" in key:
                    adapter["dhcp_enabled"] = val

                elif "ipv4 address" in key or "autoconfiguration ipv4" in key: 
                    adapter["ipv4_address"] = val

                elif "subnet mask" in key:
                    adapter["subnet_mask"] = val

                elif "default gateway" in key:
                    current_key = "gateway"
                    
                    if val:
                        if is_ipv4(val):
                            adapter["default_gateway"] = val
                        elif not adapter["default_gateway"]:
                            adapter["default_gateway"] = val

                elif "dns servers" in key:
                    current_key = "dns"
                    if val:
                        adapter["dns_servers"].append(val)

            elif line.strip() and current_key:
                val = re.sub(r'\(.*?\)', '', line).strip()

                if current_key == "dns":
                    adapter["dns_servers"].append(val)

                elif current_key == "gateway":
                    if is_ipv4(val):
                        adapter["default_gateway"] = val
                    elif not adapter["default_gateway"]:
                        adapter["default_gateway"] = val

        adapters.append(adapter)
    return {"file_name": filename, "adapters": adapters}

def main():
    results = []
    for p in Path(".").glob("parser_input_*.txt"):
        try:
            content = p.read_text(encoding="utf-16")
        except UnicodeDecodeError:
            content = p.read_text(encoding="utf-8", errors="ignore")
            
        results.append(parse_ipconfig(p.name, content))
    
    output_json = json.dumps(results, indent=2, ensure_ascii=False)
    print(output_json)
    Path("output.json").write_text(output_json, encoding="utf-8")

if __name__ == "__main__":
    main()