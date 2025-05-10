#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

def main():
    # Get directory from command line argument or use current directory
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    print(f"Searching for multi-disc CHD files in: {directory}")

    # Get all files in the directory
    files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    
    # Dictionary to store series and their disc files
    series_dict = {}
    
    # Pattern specifically for "(Disc N).chd" format
    disc_pattern = re.compile(r'(.*?)\(Disc\s+(\d+)\)(.*?)\.chd$', re.IGNORECASE)
    
    # Process each file
    for file in files:
        match = disc_pattern.match(file)
        if match:
            # Extract the base name (everything before the disc number)
            base_name = match.group(1).strip()
            disc_num = int(match.group(2))
            
            # Create entry for this series if it doesn't exist
            if base_name not in series_dict:
                series_dict[base_name] = []
            
            # Generate the new filename with "_" prefix
            new_filename = f"_{file}"
            original_path = os.path.join(directory, file)
            new_path = os.path.join(directory, new_filename)
            
            # Add this disc file to the series (using the new filename)
            series_dict[base_name].append((file, new_filename, disc_num))
    
    # Check if we found any series
    if not series_dict:
        print("No multi-disc CHD files found")
        sys.exit(0)
    
    # Sort discs by disc number within each series
    for series in series_dict:
        series_dict[series].sort(key=lambda x: x[2])
        # Keep both original and new filenames after sorting
        series_dict[series] = [(item[0], item[1]) for item in series_dict[series]]
    
    # Create a separate playlist for each series and rename the files
    for series_name, file_pairs in series_dict.items():
        # Save the playlist in the same directory as the CHD files
        output_file = os.path.join(directory, f"{series_name}.m3u")
        
        # Create the m3u playlist
        with open(output_file, 'w', encoding='utf-8') as playlist:

            for original_file, new_file in file_pairs:
                # Rename the original file
                original_path = os.path.join(directory, original_file)
                new_path = os.path.join(directory, new_file)
                
                try:
                    # Skip if file is already renamed
                    if not os.path.exists(new_path):
                        os.rename(original_path, new_path)
                        print(f"Renamed: {original_file} -> {new_file}")
                except Exception as e:
                    print(f"Error renaming {original_file}: {e}")
                
                playlist.write(f"{new_file}\n")
        
        print(f"Created playlist: {output_file} with {len(file_pairs)} disc(s) for '{series_name}'")
    
    print(f"\nTotal: Created {len(series_dict)} playlist(s)")

if __name__ == "__main__":
    main()