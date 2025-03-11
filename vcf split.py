import os

# Input and output file paths
VCF_FILE = r"C:\Users\paxso\Downloads\supreme file\ligit\contacts015,8.vcf"
OUTPUT_DIR = r"C:\Users\paxso\Downloads\supreme file\ligit\ 5,8"
MAX_SIZE = 19 * 1024 * 1024  # 19MB in bytes

def split_vcf(file_path, output_dir, max_size):
    """Splits a large VCF file into smaller parts (≤19MB each)."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create output directory if missing

    part_number = 1
    current_size = 0
    current_vcf = []
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            current_vcf.append(line)
            current_size += len(line.encode("utf-8"))  # Measure in bytes
            
            # If file size exceeds max_size, write and start a new file
            if current_size >= max_size and line.strip() == "END:VCARD":
                output_file = os.path.join(output_dir, f"contacts_part{part_number}.vcf")
                with open(output_file, "w", encoding="utf-8") as out:
                    out.writelines(current_vcf)
                print(f"Saved: {output_file} ({round(current_size / (1024 * 1024), 2)} MB)")

                # Reset for next file
                current_vcf = []
                current_size = 0
                part_number += 1

    # Save remaining contacts (last part)
    if current_vcf:
        output_file = os.path.join(output_dir, f"contacts_part{part_number}.vcf")
        with open(output_file, "w", encoding="utf-8") as out:
            out.writelines(current_vcf)
        print(f"Saved: {output_file} ({round(current_size / (1024 * 1024), 2)} MB)")

    print(f"✅ Splitting complete! Files are saved in: {output_dir}")

# Run the function
split_vcf(VCF_FILE, OUTPUT_DIR, MAX_SIZE)
