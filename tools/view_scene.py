#!/usr/bin/env python3
"""Open one scene in the MuJoCo viewer.

The sdfvoxel plugin only accepts absolute tile paths, while scene.xml keeps them
relative so the package stays relocatable. This script writes a copy with absolute
paths next to scene.xml, loads the plugin and starts the viewer.

    python tools/view_scene.py mj_3dgs_hall --plugin /path/to/libsdfvoxel.so
"""
import argparse
import re
from pathlib import Path

import mujoco
import mujoco.viewer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene", help="scene folder, e.g. mj_3dgs_hall")
    ap.add_argument("--plugin", required=True, help="path to libsdfvoxel.so")
    args = ap.parse_args()

    scene_dir = Path(args.scene).resolve()
    xml = (scene_dir / "scene.xml").read_text(encoding="utf-8")
    xml = re.sub(
        r'(<config key="path" value=")(?!/)([^"]+)"',
        lambda m: f'{m.group(1)}{(scene_dir / m.group(2)).as_posix()}"',
        xml,
    )
    abs_xml = scene_dir / ".scene_abs.xml"
    abs_xml.write_text(xml, encoding="utf-8")

    mujoco.mj_loadPluginLibrary(str(Path(args.plugin).resolve()))
    model = mujoco.MjModel.from_xml_path(str(abs_xml))
    mujoco.viewer.launch(model)


if __name__ == "__main__":
    main()
