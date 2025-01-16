# RE-Mesh Editor Batch Convert Tool

This script provides a tool for batch importing `.mesh` files into Blender using the RE-Mesh Editor plugin, exporting them as `.glb` or `.blend` with packed files, and logging the process.

## Features

- **Batch File Processing**: Automatically imports `.mesh` files found within a directory and its subdirectories.
- **Export Options**:
  - Export to `.glb` format with minimal file size.
  - Export to `.blend` format with packed files (textures, meshes, etc.).
- **Logging**: Logs the batch conversion process, including unsupported files, to `BatchConvert.log`.
- **Unsupported Files**: Files that fail to import are logged in `UnsupportedFiles.txt` for further analysis.

## Requirements

- Blender 4.0+ (or compatible version).
- RE-Mesh Editor plugin installed and enabled in Blender.
- Python 3.6 or higher for running the script.

## Installation

1. Clone this repository or download the script.
2. Install and configure the RE-Mesh Editor addon for Blender.
3. Place the script in a location of your choice.

## Usage

1. Open Blender.
2. Open a new text file in Blender’s Text Editor, and paste the script into it.
3. Modify the `search_directory` variable to point to the folder containing the `.mesh` files you want to batch process.
4. Set the `ExportBlendNoGLB` flag:
   - `True` to export `.blend` files with packed data.
   - `False` to export `.glb` files.
   
   Example:
   ```python
   ExportBlendNoGLB = True  # Change to False for GLB export
   ```

5. Run the script to start batch processing.

### Logs and Unsupported Files

- The script logs all actions to `BatchConvert.log` in the `search_directory`.
- Files that fail to import are saved in `UnsupportedFiles.txt`.

### Exported Files

- If `ExportBlendNoGLB` is set to `True`, each `.mesh` file will be exported as a `.blend` file with packed resources.
- If `ExportBlendNoGLB` is set to `False`, each `.mesh` file will be exported as a `.glb` file.

---

## Contribution

If you'd like to contribute to the project or suggest improvements, please feel free to create an issue or submit a pull request. Any contributions are welcome!
