import os
import argparse
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def convert_image(file_path):
    """Convert a PNG image to JPG format."""
    try:
        # Check if the file is a PNG
        if not file_path.lower().endswith('.png'):
            return f"Skipped {file_path} - not a PNG file"
        
        print(file_path)

        # Create the output path with .jpg extension
        output_path = os.path.splitext(file_path)[0] + '.jpg'
        
        # Open the image and convert it
        with Image.open(file_path) as img:
            # Convert RGBA to RGB if needed (JPG doesn't support alpha channel)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Save as JPG
            img.save(output_path, 'JPEG', quality=95)
        
        return f"Converted: {file_path} -> {output_path}"
    
    except Exception as e:
        return f"Error converting {file_path}: {str(e)}"

def process_directory(directory_path, max_workers=None):
    """Process all PNG images in the given directory using parallel processing."""
    # Get all PNG files in the directory
    directory = Path(directory_path)
    png_files = [str(f) for f in directory.glob('*.png')]
    
    if not png_files:
        print(f"No PNG files found in {directory_path}")
        return
    
    print(f"Found {len(png_files)} PNG files to convert")
    
    # Process the files in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(convert_image, png_files))
    
    # Print results
    for result in results:
        print(result)
    
    print(f"Conversion complete. Processed {len(png_files)} files.")

def main():
    parser = argparse.ArgumentParser(description='Convert PNG images to JPG using parallel processing')
    parser.add_argument('directory', help='Directory containing PNG images')
    parser.add_argument('--workers', type=int, default=None, 
                        help='Maximum number of worker processes (default: CPU count)')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return
    
    process_directory(args.directory, args.workers)

if __name__ == "__main__":
    main()
