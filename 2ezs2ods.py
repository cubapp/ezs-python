#!/usr/bin/env python3
"""
CSV to ODS Converter
--------------------
Converts a semicolon-separated CSV file containing formulas and values into an OpenDocument Spreadsheet (.ods).
Zajišťuje správné typování desetinných čísel (float), aby je LibreOffice Calc vždy interpretoval jako čísla.
"""

import argparse
from datetime import datetime
import os
import sys
import zipfile

def convert_csv_to_ods(input_path: str, output_path: str, debug: bool = False) -> None:
    if debug:
        print(f"[DEBUG] Čtu vstupní soubor: {input_path}")
        
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Chyba při čtení souboru: {e}", file=sys.stderr)
        sys.exit(1)

    rows_data = [[p.strip() for p in line.split(';')] for line in lines]
    
    if debug:
        print(f"[DEBUG] Načteno {len(rows_data)} řádků.")

    mimetype = b"application/vnd.oasis.opendocument.spreadsheet"

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
 <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.spreadsheet"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
</manifest:manifest>
'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" office:version="1.2">
 <office:meta>
  <meta:generator>Python CSV to ODS Converter via uv</meta:generator>
 </office:meta>
</office:document-meta>
'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" office:version="1.2">
 <office:styles>
  <style:style style:name="Default" style:family="table-cell"/>
 </office:styles>
</office:document-styles>
'''

    content_xml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:calc="http://openoffice.org/2000/calc" office:version="1.2">
 <office:body>
  <office:spreadsheet>
   <table:table table:name="List 1">
'''

    content_xml_footer = '''   </table:table>
  </office:spreadsheet>
 </office:body>
</office:document-content>
'''

    rows_xml = []
    for r_idx, row in enumerate(rows_data, start=1):
        row_str = "    <table:table-row>\n"
        for c_idx, val in enumerate(row):
            if val.startswith('='):
                formula_expr = val[1:]
                ods_formula = f"{formula_expr.upper()}"
                row_str += f'      <table:table-cell table:formula="{ods_formula}" office:value-type="float" office:value="0">\n'
                row_str += f'        <text:p>{val}</text:p>\n'
                row_str += f'      </table:table-cell>\n'
            else:
                try:
                    # Převedeme čárku na tečku pro float konverzi
                    num_val = float(val.replace(',', '.'))
                    # V ODS uložíme číselnou hodnotu s tečkou, zobrazení v text:p může zachovat čárku
                    display_val = val # např. "8,83"
                    row_str += f'      <table:table-cell office:value-type="float" office:value="{num_val}">\n'
                    row_str += f'        <text:p>{display_val}</text:p>\n'
                    row_str += f'      </table:table-cell>\n'
                except ValueError:
                    row_str += f'      <table:table-cell office:value-type="string">\n'
                    row_str += f'        <text:p>{val}</text:p>\n'
                    row_str += f'      </table:table-cell>\n'
        row_str += "    </table:table-row>\n"
        rows_xml.append(row_str)

    full_content_xml = content_xml_header + "".join(rows_xml) + content_xml_footer

    if debug:
        print(f"[DEBUG] Zapisuji ODS soubor: {output_path}")

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", mimetype)
        zf.writestr("META-INF/manifest.xml", manifest_xml)
        zf.writestr("content.xml", full_content_xml)
        zf.writestr("styles.xml", styles_xml)
        zf.writestr("meta.xml", meta_xml)

    print(f"Soubor byl úspěšně vytvořen: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Konverze CSV do ODS formátu (LibreOffice Calc) se správným typováním čísel.")
    parser.add_argument("input", help="Cesta ke vstupnímu CSV souboru.")
    parser.add_argument("-o", "--output", help="Volitelný název výstupního ODS souboru.")
    parser.add_argument("-t", "--timestamp", action="store_true", help="Přidá do názvu souboru aktuální datum a čas (např. soubor-2026.11.27-14.34.ods).")
    parser.add_argument("-d", "--debug", action="store_true", help="Zapne ladící výpisy (debug).")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Chyba: Vstupní soubor '{args.input}' neexistuje.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        base_name = args.output
        if base_name.lower().endswith('.ods'):
            base_name = base_name[:-4]
    else:
        base_name, _ = os.path.splitext(args.input)

    if args.timestamp:
        ts_str = datetime.now().strftime("%Y.%m.%d-%H.%M")
        output_filename = f"{base_name}-{ts_str}.ods"
    else:
        output_filename = f"{base_name}.ods"

    convert_csv_tokenId = convert_csv_to_ods(args.input, output_filename, debug=args.debug)

if __name__ == "__main__":
    main()
