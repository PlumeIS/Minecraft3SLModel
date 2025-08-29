import math
from typing import Dict, List

import numpy as np
from stl import mesh

from SkinRenderer import MinecraftSkinRenderer


def combine(skin_parts: Dict[str, List[mesh.Mesh]]) -> List[mesh.Mesh]:
    """合并所有网格部分"""
    return [mesh_obj for part in skin_parts.values() for mesh_obj in part]


def rotate_mesh(mesh_obj: mesh.Mesh, pivot: np.ndarray, rotation_matrix: np.ndarray) -> None:
    """旋转单个网格对象"""
    vectors = mesh_obj.vectors.reshape(-1, 3)
    vectors -= pivot
    vectors = np.dot(vectors, rotation_matrix.T)
    vectors += pivot
    mesh_obj.vectors = vectors.reshape(mesh_obj.vectors.shape)


def rotate(
        skin_parts: Dict[str, List[mesh.Mesh]],
        head_x: float = 0,
        head_y: float = 0,
        head_z: float = 0,
        right_arm_x: float = 0,
        right_arm_y: float = 0,
        left_arm_x: float = 0,
        left_arm_y: float = 0,
        right_leg_x: float = 0,
        right_leg_z: float = 0,
        left_leg_x: float = 0,
        left_leg_z: float = 0
) -> Dict[str, List[mesh.Mesh]]:
    """旋转皮肤各部分"""
    rotations = {
        "head": [
            (head_x, "x", MinecraftSkinRenderer.PIVOTS["head"]),
            (head_y, "y", MinecraftSkinRenderer.PIVOTS["head"]),
            (head_z, "z", MinecraftSkinRenderer.PIVOTS["head"])
        ],
        "right_arm": [
            (right_arm_x, "x", MinecraftSkinRenderer.PIVOTS["right_arm"]),
            (right_arm_y, "y", MinecraftSkinRenderer.PIVOTS["right_arm"])
        ],
        "left_arm": [
            (left_arm_x, "x", MinecraftSkinRenderer.PIVOTS["left_arm"]),
            (left_arm_y, "y", MinecraftSkinRenderer.PIVOTS["left_arm"])
        ],
        "right_leg": [
            (right_leg_x, "x", MinecraftSkinRenderer.PIVOTS["right_leg"]),
            (right_leg_z, "z", MinecraftSkinRenderer.PIVOTS["right_leg"])
        ],
        "left_leg": [
            (left_leg_x, "x", MinecraftSkinRenderer.PIVOTS["left_leg"]),
            (left_leg_z, "z", MinecraftSkinRenderer.PIVOTS["left_leg"])
        ]
    }

    for part_name, part_rotations in rotations.items():
        for angle, axis, pivot in part_rotations:
            if angle != 0:
                rad_angle = math.radians(angle)
                if axis == "x":
                    rotation_matrix = np.array([
                        [1, 0, 0],
                        [0, math.cos(rad_angle), -math.sin(rad_angle)],
                        [0, math.sin(rad_angle), math.cos(rad_angle)]
                    ])
                elif axis == "y":
                    rotation_matrix = np.array([
                        [math.cos(rad_angle), 0, math.sin(rad_angle)],
                        [0, 1, 0],
                        [-math.sin(rad_angle), 0, math.cos(rad_angle)]
                    ])
                else:  # axis == "z"
                    rotation_matrix = np.array([
                        [math.cos(rad_angle), -math.sin(rad_angle), 0],
                        [math.sin(rad_angle), math.cos(rad_angle), 0],
                        [0, 0, 1]
                    ])

                for mesh_obj in skin_parts[part_name]:
                    rotate_mesh(mesh_obj, pivot, rotation_matrix)

    return skin_parts
