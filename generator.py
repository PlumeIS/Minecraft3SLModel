import os

import numpy as np
from stl import mesh

import SkinRenderer
import HandleTools

if __name__ == '__main__':
    skin_path = "skin/skin.png"
    output_stl = "output/skin.stl"

    renderer = SkinRenderer.MinecraftSkinRenderer(skin_path)
    body = renderer.create_body()
    layers = renderer.create_layers()

    skin_parts = renderer.create_skin_parts(body, layers)

    rotated_parts = HandleTools.rotate(
        skin_parts,
        head_x=10, head_y=15,
        right_arm_x=-15, right_arm_y=10,
        left_arm_x=-10, left_arm_y=-10,
        right_leg_x=90, right_leg_z=6,
        left_leg_x=90, left_leg_z=-5
    )

    combined_voxels = HandleTools.combine(skin_parts)
    combined_mesh = mesh.Mesh(np.concatenate([v.data for v in combined_voxels]))
    combined_mesh.save(output_stl)

    try:
        os.system(f"start {output_stl}")
    except:
        print(f"STL文件已保存: {output_stl}")
