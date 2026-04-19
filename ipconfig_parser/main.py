import json
import re
from pathlib import Path


def clean_value(val: str) -> str:
    if not val:
        return ""
    return re.sub(r"\(.*?\)", "", val).strip()


def clean_description(val: str) -> str:
    if not val:
        return ""
    if val.startswith("Intel"):
        return "Intel"
    if val.startswith("Bluetooth Device"):
        return "Bluetooth Device"

    return val.strip()


def parse_ipconfig(filename, text):
    adapters = []
    sections = re.split(r'\n(?=[a-zA-Z].*adapter.*:)', text)

    for section in sections:
        lines = section.strip().splitlines()
        if not lines or "adapter" not in lines[0].lower():
            continue

        adapter = {
            "adapter_name": lines[0].strip(": "),
            "description": "",
            "physical_address": "",
            "dhcp_enabled": "",
            "ipv4_address": "",
            "subnet_mask": "",
            "default_gateway": [],
            "dns_servers": []
        }

        current_key = None

        for line in lines[1:]:
            if ":" in line:
                key_part, val_part = line.split(":", 1)
                key = key_part.replace(".", "").strip().lower()
                val = clean_value(val_part)

                current_key = None

                if "description" in key:
                    adapter["description"] = clean_description(val)

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
                    if val and val != "127.0.0.1":
                        adapter["default_gateway"].append(val)

                elif "dns servers" in key:
                    current_key = "dns"
                    if val:
                        adapter["dns_servers"].append(val)

            else:
                val = clean_value(line)
                if not val:
                    continue

                if current_key == "gateway":
                    if val != "127.0.0.1":
                        adapter["default_gateway"].append(val)

                elif current_key == "dns":
                    adapter["dns_servers"].append(val)

        adapters.append(adapter)

    return {"file_name": filename, "adapters": adapters}


def read_file(path):
    try:
        return path.read_text(encoding="utf-16")
    except:
        return path.read_text(encoding="utf-8", errors="ignore")


def main():
    results = []
    for path in sorted(Path(".").glob("*.txt")):
        text = read_file(path)
        results.append(parse_ipconfig(path.name, text))

    print(json.dumps(results, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()