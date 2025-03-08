import random
import numpy as np
from tqdm import tqdm
import math

# Total number of phone numbers to generate (100 million)
num_phone_numbers = 100_000_000

# Define a reasonable batch size
batch_size = 1_000_000  # Adjust as needed
num_batches = math.ceil(num_phone_numbers / batch_size)

# Output file location
output_file = r"C:\Users\paxso\Downloads\phone_numbers_cpu.txt"

with open(output_file, "w") as file:
    # Loop over batches with a tqdm progress bar
    for batch in tqdm(range(num_batches), desc="Generating Phone Numbers"):
        # Determine number of numbers in current batch
        current_batch = batch_size if batch < num_batches - 1 else num_phone_numbers - batch * batch_size

        # Generate random 8-digit numbers on CPU using NumPy
        random_ints = np.random.randint(0, 10**8, size=current_batch)
        
        # Convert the integers to zero-padded 8-digit strings
        phone_digits = np.char.zfill(random_ints.astype(str), 8)
        # Prepend the "017" prefix to each number using vectorized string addition
        phone_numbers = np.char.add("017", phone_digits)
        
        # Write all phone numbers in this batch to the file (each followed by a newline)
        file.write("\n".join(phone_numbers.tolist()) + "\n")

print("Phone number generation and saving completed.")