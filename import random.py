import random
from tqdm import tqdm  # Import the tqdm library for the progress bar

# Number of phone numbers to generate
num_phone_numbers = 100000000  # 100 million

# Open the output file in write mode
output_file = r"C:\Users\paxso\Downloads\phone_numbers1.txt" # change the location if needed 
with open(output_file, "w") as file:
    
    # Create a tqdm progress bar with the specified total
    progress_bar = tqdm(total=num_phone_numbers, desc="Generating Phone Numbers")
    
    # Generate and write phone numbers to the file
    for _ in range(num_phone_numbers):
        # Generate the 8 random digits for the phone number
        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        
        # Create the full phone number with "017" prefix
        phone_number = "017" + random_digits
        
        # Write the phone number followed by a newline character
        file.write(phone_number + "\n")
        
        # Update the progress bar
        progress_bar.update(1)
    
    # Close the progress bar
    progress_bar.close()

print("Phone number generation and saving completed.")