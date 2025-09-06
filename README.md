# Minecraft 皮肤转 3D 模型生成器

这是一个用于将 Minecraft 皮肤转换为带外层图层的 3D STL 模型文件的 Python 工具。生成的模型可以用于 3D 打印或其它 3D 建模用途。

## 功能特点

- 生成包含外层图层（第二层）的完整模型
- 可调节身体各部位的旋转角度

## 安装依赖

在使用此工具前，请确保已安装以下 Python 库：

```bash
pip install numpy
pip install numpy-stl
```

## 使用方法

### 基本命令
```bash
python generator.py -i [输入皮肤路径] -o [输出STL路径]
```

### 参数说明

| 参数 | 缩写 | 默认值 | 描述 |
|------|------|--------|------|
| --input | -i | skin/skin.png | 输入皮肤图片路径 |
| --output | -o | output/skin.stl | 输出STL文件路径 |

### 部位旋转参数

- --head_x：头部 X 轴旋转角度（默认：0）
- --head_y：头部 Y 轴旋转角度（默认：0）
- --right_arm_x：右臂 X 轴旋转角度（默认：0）
- --right_arm_y：右臂 Y 轴旋转角度（默认：0）
- --left_arm_x：左臂 X 轴旋转角度（默认：0）
- --left_arm_y：左臂 Y 轴旋转角度（默认：0）
- --right_leg_x：右腿 X 轴旋转角度（默认：0）
- --right_leg_z：右腿 Z 轴旋转角度（默认：0）
- --left_leg_x：左腿 X 轴旋转角度（默认：0）
- --left_leg_z：左腿 Z 轴旋转角度（默认：0）

### 示例命令

1. 使用默认设置生成模型：
```bash
python generator.py
```
2. 指定输入和输出路径：
```bash
python generator.py -i my_skin.png -o my_model.stl
```
3. 调整头部和手臂角度：
```bash
python generator.py --head_x 15 --head_y 30 --right_arm_x 45 --left_arm_x -20
```

## 输出说明

程序会生成一个 STL 格式的 3D 模型文件，包含 Minecraft 皮肤的所有部位及其外层图层。生成的模型保持了 Minecraft 风格的方块状外观，适合用于 3D 打印。

## 项目结构
```
.
├── generator.py # 主程序入口
├── SkinRenderer.py # 皮肤渲染器
├── HandleTools.py # 模型处理工具
├── skin/ # 默认皮肤目录
│ └── skin.png # 示例皮肤文件
└── output/ # 输出目录
  └── skin.stl # 示例输出文件
```

## TODO
+ [x] 兼容 slim 皮肤
+ [ ] 兼容非 64x 皮肤
+ [ ] 生成支持多色的 3mf文件

##  许可证
本项目采用 MIT 许可证。详见 LICENSE 文件。

## 贡献
欢迎提交 Issue 和 Pull Request 来改进这个项目。
