import os
import pytest

import pygraphviz as pgv
from pygraphviz.scraper import _get_sg_image_scraper


def test_scraper(tmpdir):
    pytest.importorskip("sphinx_gallery")
    scraper = _get_sg_image_scraper()

    ### Source
    src_dir = str(tmpdir)
    src_file = os.path.join(src_dir, "simple.py")  # no need for this to exist
    # Create source PNG
    A = pgv.AGraph()
    A.add_edge(1, 2)
    A.layout()
    A.draw(os.path.join(src_dir, "simple.png"))

    ### Target
    out_dir = os.path.join(src_dir, "build", "html")
    os.makedirs(out_dir)
    out_file = os.path.join(out_dir, "simple.png")
    # Target should **not** exist
    assert not os.path.isfile(out_file)
    # Copy source PNG to target location
    block = None
    block_vars = {
        "image_path_iterator": (img for img in [out_file]),
        "src_file": src_file,
    }
    gallery_conf = {"src_dir": src_dir, "builder_name": "html"}
    scraper(block, block_vars, gallery_conf)
    # Target should exist
    assert os.path.isfile(out_file)
