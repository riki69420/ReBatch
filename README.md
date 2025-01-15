# Batch Convert `.mesh` Files to `.glb` in Blender

This script is designed to automate the conversion of `.mesh` files into `.glb` files using Blender. It searches through a specified directory and its subdirectories for `.mesh` files, imports them into Blender using the RE-Mesh Editor, and exports the scene to `.glb` format. The script handles unsupported files, logs the process, and cleans the scene after each export.

## Prerequisites

Before running the script, ensure you have the following:

1. **Blender**: The script is compatible with Blender 4.0+.
2. **RE-Mesh Editor Addon**: This addon is required for importing `.mesh` files into Blender. You can download it [here](https://github.com/NSACloud/RE-Mesh-Editor).

## Setup Instructions

### 1. Install the RE-Mesh Editor Addon
   - Download the [RE-Mesh Editor Addon](https://github.com/NSACloud/RE-Mesh-Editor).
   - Open Blender.
   - Go to `Edit` → `Preferences` → `Add-ons` → `Install`.
   - Select the downloaded `.zip` file and install it.
   - Enable the RE-Mesh Editor addon from the Add-ons tab.

### 2. Script Configuration
   - Save the script file to a location on your computer.
   - Modify the `search_directory` variable in the script to point to the directory containing your `.mesh` files. You can use an absolute path like `F:/torrents/Dragon's Dogma 2/REtool/re_chunk_000/natives/stm` or any other path that contains `.mesh` files.

### 3. Run the Script in Blender
   - Open Blender and go to the Scripting tab.
   - Click `New` to create a new script and paste the provided Python script into the Blender text editor.
   - Adjust the `search_directory` path to match the location of your `.mesh` files.
   - Press `Run Script` to start the batch conversion process.

### 4. How It Works
   - The script will search through the specified directory and its subdirectories for files that match the `.mesh.` pattern (excluding those that end with `.mesh.glb`).
   - For each valid `.mesh` file found:
     - The script imports the mesh using the RE-Mesh Editor.
     - It exports the scene as a `.glb` file to the same directory with the same base filename.
     - The scene is cleaned up (deleted objects and cleared collections) after each export to prepare for the next file.
   - The script logs its progress and any errors in `BatchConvert.log` in the specified directory.
   - Unsupported files are logged in `UnsupportedFiles.txt` for reference.

### 5. Output
   - After processing, you will find:
     - `.glb` files in the same directory as the source `.mesh` files.
     - A `BatchConvert.log` file containing the log of all actions performed by the script.
     - An `UnsupportedFiles.txt` file listing any files that could not be processed (e.g., unsupported file formats).

## Example Directory Structure

Here’s an example of the expected directory structure:

```
F:/torrents/Dragon's Dogma 2/REtool/re_chunk_000/natives/stm/
├── character/
│   ├── ch/
│   │   └── ch21_000/
│   │       ├── ch21_000.mesh.231011879
│   │       ├── ch21_000.mesh.231011880
│   │       └── ch21_000.mesh.231011881
├── appdata/
│   └── contents/
│       └── dng_019/
│           └── sm11_074_04_sm11_074_04_va_00.mesh.231011879
```

The script will process files like `ch21_000.mesh.231011879`, import them into Blender, and export them as `ch21_000.glb`.

## Notes
- **Supported Files**: Only `.mesh` files without the `.mesh.glb` suffix will be processed.
- **Error Handling**: If an unsupported file format is found (like MPLY format), the script will skip that file and log it as unsupported.
- **Log Files**: All actions, including errors, will be logged in `BatchConvert.log`. Unsupported files will be listed in `UnsupportedFiles.txt`.

## Troubleshooting
- If the script seems to hang or doesn’t process files, ensure the path to the mesh files is correctly specified.
- If you encounter an error related to unsupported formats (e.g., "MPLY formatted mesh files are not supported yet"), check if the mesh format is compatible with the RE-Mesh Editor.
- Ensure that the RE-Mesh Editor addon is properly installed and enabled in Blender.
