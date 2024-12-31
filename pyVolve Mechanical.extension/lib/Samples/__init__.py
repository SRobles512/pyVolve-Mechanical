def open_sample_file(file_name):
    """Function to open Sample file located at:
    ...\pyRevitStarterKit.extension\lib\Samples\{{file_name}}"""
    import os

    # Find Base Path to .extension
    current_path = os.path.abspath(__file__)
    base_path = current_path
    while not base_path.endswith('.extension'):
        base_path = os.path.dirname(base_path)

    # Open Sample File
    target_path = os.path.join(base_path, 'lib', 'Samples', file_name)
    os.startfile(target_path)
    os.startfile(os.path.dirname(target_path))