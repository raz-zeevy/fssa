import re


def extract_all_dimensions(filepath):
    with open(filepath, 'r') as file:
        text = file.read()

    # Regular expression to split the text into different dimensionality blocks
    blocks = re.split(r'\s+D\s*I\s*M\s*E\s*N\s*S\s*I\s*O\s*N\s*A\s*L\s*I\s*T\s*Y\s+\d+', text)

    # Process each block
    results = []
    for block in blocks[1:]:  # Skip the first split which is before the first dimensionality header
        # Extract the first three rows with labels
        header_regex = re.compile(r'^(.*?)\.\.+ +([\d.]+)$', re.MULTILINE)
        header_matches = header_regex.findall(block)
        header_data = {re.sub(r'[\s]+', '_', m[0].strip().lower()): float(m[1].strip()) for m in header_matches}

        # Regular expression to match the data lines
        data_regex = re.compile(r'^\s*(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*([\d.]*)$', re.MULTILINE)
        matches = data_regex.findall(block)

        # Convert to a structured format
        coordinates = [{'serial_number': int(m[0]), 'distance': float(m[1]),
                        'coordinates' : [float(m[i]) for i in range(2,
                                                                    len(m))
                                         if m[i] != ""]}
                       for m in matches]
        if not coordinates: continue
        # Combine header and coordinates data
        header_data['coordinates'] = coordinates
        results.append(header_data)

    return results


if __name__ == '__main__':
    output_path = r"C:\Users\Raz_Z\Projects\Shmuel\fssa\output\test_3_gui.fss"
    # output_path = r"C:\Users\Raz_Z\Projects\Shmuel\fssa\output\test_simple.fss"
    print(extract_all_dimensions(output_path))
