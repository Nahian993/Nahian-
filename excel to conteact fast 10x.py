import pandas as pd
import numpy as np
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

# File paths
EXCEL_FILE = r"C:\Users\paxso\Downloads\supreme file\ligit\015 - 018.xlsx"
VCF_OUTPUT = r"C:\Users\paxso\Downloads\supreme file\ligit\contacts015,8.vcf"

# Batch size for multiprocessing
BATCH_SIZE = 10000

def create_vcard_batch(data_chunk):
    """Process a batch of contacts into vCards."""
    vcards = []
    for row in data_chunk:
        # Ensure row has at least 4 elements
        if len(row) < 4:
            continue  # Skip invalid rows

        phone = str(row[0]) if len(row) > 0 and pd.notna(row[0]) else ""
        first_name = str(row[2]) if len(row) > 2 and pd.notna(row[2]) else ""
        last_name = str(row[3]) if len(row) > 3 and pd.notna(row[3]) else ""

        vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{last_name};{first_name};;;\nFN:{first_name} {last_name}\nTEL;TYPE=CELL:{phone}\nEND:VCARD\n"
        vcards.append(vcard)
    
    return vcards

def main():
    # Read Excel file into NumPy array
    df = pd.read_excel(EXCEL_FILE, dtype=str)
    
    # Ensure at least 4 columns exist
    if df.shape[1] < 4:
        print("❌ ERROR: The Excel file must have at least 4 columns! Check the file and try again.")
        return

    data = df.to_numpy()
    total_rows = data.shape[0]
    
    # Split into batches
    chunks = [data[i:i + BATCH_SIZE] for i in range(0, total_rows, BATCH_SIZE)]
    
    # Use ProcessPoolExecutor to utilize ALL CPU cores efficiently
    vcard_results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(create_vcard_batch, chunk): chunk for chunk in chunks}
        
        # Progress bar
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Contacts", unit="batch"):
            vcard_results.extend(future.result())  # Collect results

    # Write to file
    with open(VCF_OUTPUT, "w", encoding="utf-8") as vcf_file:
        vcf_file.writelines(vcard_results)
    
    print(f"✅ Done! {total_rows} contacts saved to: {VCF_OUTPUT}")

if __name__ == "__main__":
    main()
