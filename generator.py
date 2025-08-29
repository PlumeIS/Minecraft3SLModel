import argparse

import numpy as np
from stl import mesh

import HandleTools
import SkinRenderer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成Minecraft皮肤3D模型')
    parser.add_argument('-i', '--input', default='skin/skin.png',
                        help='输入皮肤图片路径（默认：skin/skin.png）')
    parser.add_argument('-o', '--output', default='output/skin.stl',
                        help='输出STL文件路径（默认：output/skin.stl）')

    parser.add_argument('--head_x', type=float, default=0, help='头部X轴旋转角度（默认：0）')
    parser.add_argument('--head_y', type=float, default=0, help='头部Y轴旋转角度（默认：0）')
    parser.add_argument('--right_arm_x', type=float, default=0, help='右臂X轴旋转角度（默认：0）')
    parser.add_argument('--right_arm_y', type=float, default=0, help='右臂Y轴旋转角度（默认：0）')
    parser.add_argument('--left_arm_x', type=float, default=0, help='左臂X轴旋转角度（默认：0）')
    parser.add_argument('--left_arm_y', type=float, default=0, help='左臂Y轴旋转角度（默认：0）')
    parser.add_argument('--right_leg_x', type=float, default=0, help='右腿X轴旋转角度（默认：0）')
    parser.add_argument('--right_leg_z', type=float, default=0, help='右腿Z轴旋转角度（默认：0）')
    parser.add_argument('--left_leg_x', type=float, default=0, help='左腿X轴旋转角度（默认：0）')
    parser.add_argument('--left_leg_z', type=float, default=0, help='左腿Z轴旋转角度（默认：0）')

    args = parser.parse_args()

    skin_path = args.input
    output_stl = args.output

    renderer = SkinRenderer.MinecraftSkinRenderer(skin_path)
    body = renderer.create_body()
    layers = renderer.create_layers()

    skin_parts = renderer.create_skin_parts(body, layers)

    rotated_parts = HandleTools.rotate(
        skin_parts,
        head_x=args.head_x, head_y=args.head_y,
        right_arm_x=args.right_arm_x, right_arm_y=args.right_arm_y,
        left_arm_x=args.left_arm_x, left_arm_y=args.left_arm_y,
        right_leg_x=args.right_leg_x, right_leg_z=args.right_leg_z,
        left_leg_x=args.left_leg_x, left_leg_z=args.left_leg_z
    )

    combined_voxels = HandleTools.combine(skin_parts)
    combined_mesh = mesh.Mesh(np.concatenate([v.data for v in combined_voxels]))
    combined_mesh.save(output_stl)

    print(f"STL文件已保存: {output_stl}")