import bpy
import os
import logging
import re

search_directory = r"F:\torrents\MonsterHunterWilds\re_chunk_000\natives\stm\art\model\character"
log_file = os.path.join(search_directory, "BatchConvert.log")
unsupported_file = os.path.join(search_directory, "UnsupportedFiles.txt")
mesh_pattern = re.compile(r"\.mesh\.\d+$")
skip_patterns = ['.mesh.fbx', '.blend']
export_as_blend = False  # True: .blend, False: .fbx
max_retries = 1

is_background = bpy.app.background

open(log_file, 'w').close()
open(unsupported_file, 'w').close()

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logging.info("Batch conversion started.")

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)
    # Purge orphan datablocks
    for datablock_list in (bpy.data.images, bpy.data.meshes, bpy.data.materials,
                           bpy.data.textures, bpy.data.curves, bpy.data.armatures,
                           bpy.data.actions, bpy.data.node_groups):
        for datablock in list(datablock_list):
            if datablock.users == 0:
                try:
                    datablock_list.remove(datablock)
                except Exception:
                    pass

def find_mesh_files(directory):
    files = []
    for root, _, names in os.walk(directory):
        for fn in names:
            if any(skip in fn for skip in skip_patterns):
                continue
            if mesh_pattern.search(fn):
                files.append((fn, os.path.join(root, fn), root))
    return files

def log_unsupported(fn):
    with open(unsupported_file, 'a') as uf:
        uf.write(fn + '\n')

def process_mesh(fn, path, root):
    try:
        bpy.ops.re_mesh.importfile(filepath=path, files=[{"name": fn}], directory=root)
        if export_as_blend:
            bpy.ops.file.pack_all()
            out = os.path.join(root, f"{os.path.splitext(fn)[0]}.blend")
            bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)
            logging.info(f"Exported packed .blend: {out}")
        else:
            out = os.path.join(root, f"{os.path.splitext(fn)[0]}.fbx")
            bpy.ops.export_scene.fbx(
                filepath=out,
                use_selection=False,
                use_visible=False,
                use_active_collection=False,
                global_scale=1.0,
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_NONE',
                use_space_transform=True,
                bake_space_transform=False,
                object_types={'OTHER', 'LIGHT', 'ARMATURE', 'CAMERA', 'EMPTY', 'MESH'},
                use_mesh_modifiers=True,
                use_mesh_modifiers_render=True,
                mesh_smooth_type='OFF',
                colors_type='SRGB',
                prioritize_active_color=False,
                use_subsurf=False,
                use_mesh_edges=False,
                use_tspace=False,
                use_triangles=False,
                use_custom_props=False,
                add_leaf_bones=True,
                primary_bone_axis='Y',
                secondary_bone_axis='X',
                use_armature_deform_only=False,
                armature_nodetype='NULL',
                bake_anim=True,
                bake_anim_use_all_bones=True,
                bake_anim_use_nla_strips=True,
                bake_anim_use_all_actions=True,
                bake_anim_force_startend_keying=True,
                bake_anim_step=1.0,
                bake_anim_simplify_factor=1.0,
                path_mode='COPY',
                embed_textures=True,
                batch_mode='OFF',
                use_batch_own_dir=True,
                axis_forward='-Z',
                axis_up='Y'
            )
            logging.info(f"Exported .fbx: {out}")
        clean_scene()
        logging.info(f"Scene cleaned.")
        return True
    except Exception as exc:
        msg = str(exc)
        if 'MPLY formatted mesh files' in msg or 'NoneType' in msg:
            logging.warning(f"Unsupported: {fn} | {msg}")
            log_unsupported(fn)
            return False
        else:
            logging.warning(f"Error on {fn}: {msg}")
            return False

def main():
    wm = bpy.context.window_manager
    files = find_mesh_files(search_directory)
    total = len(files)
    logging.info(f"Found {total} mesh files to process.")

    if not is_background:
        wm.progress_begin(0, total)

    retry_counts = {}
    processed = 0
    queue = files.copy()

    while queue:
        fn, path, root = queue.pop(0)
        attempts = retry_counts.get(fn, 0) + 1
        success = process_mesh(fn, path, root)
        if not success and attempts <= max_retries:
            retry_counts[fn] = attempts
            logging.warning(f"Retrying {fn}, attempt {attempts}")
            queue.append((fn, path, root))
            continue
        elif not success:
            logging.error(f"Failed after retries: {fn}")
            log_unsupported(fn)
        processed += 1
        if not is_background:
            wm.progress_update(processed)
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.header_text_set(f"Batch: {processed}/{total} - {fn}")

    if not is_background:
        wm.progress_end()
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.header_text_set(None)

    logging.info("All files processed.")

if __name__ == '__main__':
    main()
