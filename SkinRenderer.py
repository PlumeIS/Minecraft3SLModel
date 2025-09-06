from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image
from stl import mesh


@dataclass
class VoxelParams:
    """体素参数数据类"""
    x: float
    y: float
    z: float
    l: float
    w: float
    h: float


@dataclass
class LayerParams:
    """图层参数数据类"""
    center: Tuple[float, float, float]
    l: float
    w: float
    axle: str
    from_p: Tuple[int, int]
    to_p: Tuple[int, int]
    thickness: float = 0.4


class MinecraftSkinRenderer:
    """Minecraft皮肤渲染器类"""

    # 定义身体部位旋转中心点
    PIVOTS = {
        "head": np.array([8.0, 4.0, 24.0]),
        "right_arm": np.array([4.0, 4.0, 24.0]),
        "left_arm": np.array([12.0, 4.0, 24.0]),
        "right_leg": np.array([6.0, 4.0, 12.0]),
        "left_leg": np.array([10.0, 4.0, 12.0])
    }

    def __init__(self, skin_path: str, slim: bool = False):
        self.skin_path: str = skin_path
        self.slim: bool = slim

    @staticmethod
    def create_voxel(params: VoxelParams) -> mesh.Mesh:
        """创建体素网格"""
        x, y, z, l, w, h = params.x, params.y, params.z, params.l, params.w, params.h

        vertices = np.array([
            [x, y, z],
            [x + l, y, z],
            [x + l, y + w, z],
            [x, y + w, z],
            [x, y, z + h],
            [x + l, y, z + h],
            [x + l, y + w, z + h],
            [x, y + w, z + h]
        ])

        faces = np.array([
            [0, 3, 1], [1, 3, 2],  # 底面
            [0, 1, 4], [1, 5, 4],  # 前面
            [1, 2, 5], [2, 6, 5],  # 右侧面
            [2, 3, 6], [3, 7, 6],  # 后面
            [3, 0, 7], [0, 4, 7],  # 左侧面
            [4, 5, 6], [4, 6, 7]  # 顶面
        ])

        # 创建Mesh对象
        voxel = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, face in enumerate(faces):
            for j in range(3):
                voxel.vectors[i][j] = vertices[face[j], :]
        return voxel

    def create_body(self) -> Dict[str, mesh.Mesh]:
        """创建身体基础网格"""
        basic = {
            "right_leg": MinecraftSkinRenderer.create_voxel(VoxelParams(4, 2, 0, 4, 4, 12)),
            "left_leg": MinecraftSkinRenderer.create_voxel(VoxelParams(8, 2, 0, 4, 4, 12)),
            "body": MinecraftSkinRenderer.create_voxel(VoxelParams(4, 2, 12, 8, 4, 12)),
            "head": MinecraftSkinRenderer.create_voxel(VoxelParams(4, 0, 24, 8, 8, 8))
        }

        classic = {
            "right_arm": MinecraftSkinRenderer.create_voxel(VoxelParams(0, 2, 12, 4, 4, 12)),
            "left_arm": MinecraftSkinRenderer.create_voxel(VoxelParams(12, 2, 12, 4, 4, 12))
        }

        slim = {
            "right_arm": MinecraftSkinRenderer.create_voxel(VoxelParams(1, 2, 12, 3, 4, 12)),
            "left_arm": MinecraftSkinRenderer.create_voxel(VoxelParams(12, 2, 12, 3, 4, 12))
        }

        if not self.slim:
            basic.update(classic)
        else:
            basic.update(slim)

        return basic

    @staticmethod
    def create_layer(layer_params: LayerParams, pixels, thickness: float = 0.4) -> List[mesh.Mesh]:
        """创建皮肤图层"""
        center, l, w, axle, from_p, to_p = (
            layer_params.center, layer_params.l, layer_params.w,
            layer_params.axle, layer_params.from_p, layer_params.to_p
        )

        sizeL = l + 2 * thickness
        sizeW = w + 2 * thickness
        dl = sizeL / l
        dw = sizeW / w
        rl = sizeL / 2
        rw = sizeW / 2

        # 确定起始点和步长
        if axle == "x":
            start_y = center[1] - rl
            start_z = center[2] - rw
            step_y, step_z = dl, dw
        elif axle == "y":
            start_x = center[0] - rl
            start_z = center[2] - rw
            step_x, step_z = dl, dw
        elif axle == "z":
            start_x = center[0] - rl
            start_y = center[1] - rw
            step_x, step_y = dl, dw
        else:
            raise ValueError("axle must be 'x', 'y', or 'z'")

        # 确定迭代方向
        step_x_dir = 0 if to_p[0] > from_p[0] else -1
        step_y_dir = 0 if to_p[1] > from_p[1] else -1

        voxels = []
        for i, p_x in enumerate(range(from_p[0] + step_x_dir, to_p[0] + step_x_dir, 1 if to_p[0] > from_p[0] else -1)):
            for j, p_y in enumerate(
                    range(from_p[1] + step_y_dir, to_p[1] + step_y_dir, 1 if to_p[1] > from_p[1] else -1)):
                if pixels[p_x, p_y][3] != 0:  # 检查alpha通道
                    if axle == "x":
                        x = center[0]
                        y = start_y + i * step_y
                        z = start_z + j * step_z
                        tx, ty, tz = thickness, dl, dw
                    elif axle == "y":
                        x = start_x + i * step_x
                        y = center[1]
                        z = start_z + j * step_z
                        tx, ty, tz = dl, thickness, dw
                    else:  # axle == "z"
                        x = start_x + i * step_x
                        y = start_y + j * step_y
                        z = center[2]
                        tx, ty, tz = dl, dw, thickness

                    voxels.append(MinecraftSkinRenderer.create_voxel(
                        VoxelParams(x, y, z, tx, ty, tz)))

        return voxels

    def create_layers(self, thickness: float = 0.4) -> Dict[str, List[mesh.Mesh]]:
        """创建所有皮肤图层"""
        texture_mapping = self.create_texture_mapping(thickness)

        skin_img = Image.open(self.skin_path).convert('RGBA')
        skin_pixels = skin_img.load()

        layers = {}
        for part_name, part_faces in texture_mapping.items():
            part_layers = []
            for face_name, layer_params in part_faces.items():
                part_layers.extend(MinecraftSkinRenderer.create_layer(layer_params, skin_pixels, thickness))
            layers[f"{part_name}_layer"] = part_layers

        return layers

    def create_texture_mapping(self, thickness: float = 0.4) -> dict[
        str, dict[str, LayerParams] | dict[str, LayerParams] | dict[str, LayerParams] | dict[str, LayerParams] | dict[
            str, LayerParams] | dict[str, LayerParams]]:
        basic_texture_mapping = {
            "head": {
                "front": LayerParams((8, 8, 28), 8, 8, "y", (40, 16), (48, 8)),
                "back": LayerParams((8, 0 - thickness, 28), 8, 8, "y", (64, 16), (56, 8)),
                "left": LayerParams((4 - thickness, 4, 28), 8, 8, "x", (32, 16), (40, 8)),
                "right": LayerParams((12, 4, 28), 8, 8, "x", (56, 16), (48, 8)),
                "top": LayerParams((8, 4, 32), 8, 8, "z", (40, 0), (48, 8)),
                "bottom": LayerParams((8, 4, 24 - thickness), 8, 8, "z", (48, 0), (56, 8)),
            },
            "body": {
                "front": LayerParams((8, 6, 18), 8, 12, "y", (20, 48), (28, 36)),
                "back": LayerParams((8, 2 - thickness, 18), 8, 12, "y", (40, 48), (32, 36)),
                "left": LayerParams((4 - thickness, 4, 18), 4, 12, "x", (16, 48), (20, 36)),
                "right": LayerParams((12, 4, 18), 4, 12, "x", (32, 48), (28, 36)),
                "top": LayerParams((8, 4, 24), 8, 4, "z", (20, 32), (28, 36)),
                "bottom": LayerParams((8, 4, 12 - thickness), 8, 4, "z", (28, 32), (36, 36)),
            },
            "right_leg": {
                "front": LayerParams((6, 6, 6), 4, 12, "y", (4, 48), (8, 36)),
                "back": LayerParams((6, 2 - thickness, 6), 4, 12, "y", (16, 48), (12, 36)),
                "left": LayerParams((4 - thickness, 4, 6), 4, 12, "x", (0, 48), (4, 36)),
                "right": LayerParams((8, 4, 6), 4, 12, "x", (12, 48), (8, 36)),
                "top": LayerParams((6, 4, 12), 4, 4, "z", (4, 32), (8, 36)),
                "bottom": LayerParams((6, 4, 0 - thickness), 4, 4, "z", (8, 32), (12, 36)),
            },
            "left_leg": {
                "front": LayerParams((10, 6, 6), 4, 12, "y", (4, 64), (8, 52)),
                "back": LayerParams((10, 2 - thickness, 6), 4, 12, "y", (16, 64), (12, 52)),
                "left": LayerParams((8 - thickness, 4, 6), 4, 12, "x", (0, 64), (4, 52)),
                "right": LayerParams((12, 4, 6), 4, 12, "x", (12, 64), (8, 52)),
                "top": LayerParams((10, 4, 12), 4, 4, "z", (4, 48), (8, 52)),
                "bottom": LayerParams((10, 4, 0 - thickness), 4, 4, "z", (8, 48), (12, 52)),
            }
        }
        classic = {
            "right_arm": {
                "front": LayerParams((2, 6, 18), 4, 12, "y", (44, 48), (48, 36)),
                "back": LayerParams((2, 2 - thickness, 18), 4, 12, "y", (56, 48), (52, 36)),
                "left": LayerParams((0 - thickness, 4, 18), 4, 12, "x", (40, 48), (44, 36)),
                "right": LayerParams((4, 4, 18), 4, 12, "x", (52, 48), (48, 36)),
                "top": LayerParams((2, 4, 24), 4, 4, "z", (44, 32), (48, 36)),
                "bottom": LayerParams((2, 4, 12 - thickness), 4, 4, "z", (48, 32), (52, 36)),
            },
            "left_arm": {
                "front": LayerParams((14, 6, 18), 4, 12, "y", (52, 64), (56, 52)),
                "back": LayerParams((14, 2 - thickness, 18), 4, 12, "y", (64, 64), (60, 52)),
                "left": LayerParams((12 - thickness, 4, 18), 4, 12, "x", (48, 64), (52, 52)),
                "right": LayerParams((16, 4, 18), 4, 12, "x", (60, 64), (56, 52)),
                "top": LayerParams((14, 4, 24), 4, 4, "z", (52, 48), (56, 52)),
                "bottom": LayerParams((14, 4, 12 - thickness), 4, 4, "z", (56, 48), (60, 52)),
            }
        }
        slim = {
            "right_arm": {
                "front": LayerParams((2.5, 6, 18), 3, 12, "y", (44, 48), (47, 36)),
                "back": LayerParams((2.5, 2 - thickness, 18), 3, 12, "y", (54, 48), (51, 36)),
                "left": LayerParams((1 - thickness, 4, 18), 4, 12, "x", (40, 48), (44, 36)),
                "right": LayerParams((4, 4, 18), 4, 12, "x", (51, 48), (47, 36)),
                "top": LayerParams((2.5, 4, 24), 3, 4, "z", (44, 32), (47, 36)),
                "bottom": LayerParams((2.5, 4, 12 - thickness), 3, 4, "z", (47, 32), (50, 36)),
            },
            "left_arm": {
                "front": LayerParams((14-.5, 6, 18), 3, 12, "y", (52, 64), (55, 52)),
                "back": LayerParams((14-.5, 2 - thickness, 18), 3, 12, "y", (62, 64), (59, 52)),
                "left": LayerParams((12 - thickness, 4, 18), 4, 12, "x", (48, 64), (52, 52)),
                "right": LayerParams((15, 4, 18), 4, 12, "x", (59, 64), (55, 52)),
                "top": LayerParams((14-.5, 4, 24), 3, 4, "z", (52, 48), (55, 52)),
                "bottom": LayerParams((14-.5, 4, 12 - thickness), 3, 4, "z", (55, 48), (58, 52)),
            }
        }

        if not self.slim:
            basic_texture_mapping.update(classic)
        else:
            basic_texture_mapping.update(slim)

        return basic_texture_mapping

    @staticmethod
    def create_skin_parts(body_parts: Dict[str, mesh.Mesh], layer_parts: Dict[str, List[mesh.Mesh]]) -> Dict[
        str, List[mesh.Mesh]]:
        """归类网格部分"""
        return {
            "head": [body_parts["head"], *layer_parts["head_layer"]],
            "body": [body_parts["body"], *layer_parts["body_layer"]],
            "right_arm": [body_parts["right_arm"], *layer_parts["right_arm_layer"]],
            "left_arm": [body_parts["left_arm"], *layer_parts["left_arm_layer"]],
            "right_leg": [body_parts["right_leg"], *layer_parts["right_leg_layer"]],
            "left_leg": [body_parts["left_leg"], *layer_parts["left_leg_layer"]],
        }
