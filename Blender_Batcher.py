import bpy
import os
import logging

search_directory = r"YOUR DIR HERE" # Directory you wanna convert
log_file = os.path.join(search_directory, "BatchConvert.log")
unsupported_files_file = os.path.join(search_directory, "UnsupportedFiles.txt")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

logging.info("Batch conversion started.")

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

def find_mesh_files(directory):
    mesh_files = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if '.mesh.' in file_name and '.mesh.glb' not in file_name:
                file_path = os.path.join(root, file_name)
                mesh_files.append((file_name, file_path, root))
    return mesh_files

def log_unsupported_file(file_name):
    with open(unsupported_files_file, 'a') as f:
        f.write(f"{file_name}\n")

processed_files = set()

mesh_files = find_mesh_files(search_directory)

while mesh_files:
    file_name, file_path, root = mesh_files.pop(0)

    if file_path in processed_files:
        logging.info(f"Skipping already processed file: {file_name}")
        continue

    logging.info(f"Found file: {file_name}")
    
    processed_files.add(file_path)
    
    files_list = [{"name": file_name, "name": file_name}]
    
    try:
        bpy.ops.re_mesh.importfile(filepath=file_path, files=files_list, directory=root)
        logging.info(f"Successfully imported {file_name}")

        export_path = os.path.join(root, f"{os.path.splitext(file_name)[0]}.glb")

        bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')
        logging.info(f"Exported .glb to {export_path}")

        clean_scene()
        logging.info("Scene cleaned up.")

    except Exception as e:
        if "MPLY formatted mesh files" in str(e):
            logging.warning(f"Skipping unsupported file: {file_name} ({e})")
            log_unsupported_file(file_name)
        else:
            logging.error(f"Error processing {file_name}: {e}")
            raise e

logging.info("All mesh files have been processed.")
