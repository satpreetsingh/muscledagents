from . import colors
from .colors import rgb_to_decimal
from mjcf import elements as e

def populated_ma_asset(asset):
    """
    Adds standard MuscledAgent environment assets into the provided
    Asset() object
    """
    skybox_texture = e.Texture(
        type="skybox",
        fileright="sunny-right.png",
        fileleft="sunny-left.png",
        fileup="sunny-up.png",
        filedown="sunny-down.png",
        filefront="sunny-front.png",
        fileback="sunny-back.png"
    )

    tex2 = e.Texture(
        builtin="flat",
        height=1278,
        mark="cross",
        markrgb=[1, 1, 1],
        name="texgeom",
        random=0.01,
        rgb1=rgb_to_decimal(220, 227, 233),
        rgb2=rgb_to_decimal(231, 235, 246),
        type="cube",
        width=127
    )
    tex3 = e.Texture(
        builtin="checker",
        height=[100],
        name="texplane",
        rgb1=rgb_to_decimal(210, 207, 241),
        rgb2=rgb_to_decimal(110, 163, 230),
        type="2d",
        width=100
    )
    mat1 = e.Material(
        name="MatPlane",
        reflectance=0.5,
        shininess=1,
        specular=1,
        texrepeat=[60, 60],
        texture="texplane"
    )
    mat2 = e.Material(
        name="geom",
        texture="texgeom",
        texuniform=True
    )

    asset.add_children([
        skybox_texture,
        tex2,
        tex3,
        mat1,
        mat2,
    ])

def populate_ma_worldbody(worldbody):
    """
    Adds a standard MuscledAgents floor and global light to the provided
    WorldBody() object.
    """

    light = e.Light(
        cutoff=100,
        diffuse=[1, 1, 1],
        dir=[-0, 0, -1.3],
        directional=True,
        exponent=1,
        pos=[0, 0, 1.3],
        specular=[.1, .1, .1]
    )

    floor_geom = e.Geom(
        conaffinity=1,
        condim=3,
        material="MatPlane",
        name="floor",
        pos=[0, 0, 0],
        rgba=[0.8, 0.9, 0.8, 1],
        size=[40, 40, 40],
        type="plane"
    )

    worldbody.add_children([
        light,
        floor_geom,
    ])