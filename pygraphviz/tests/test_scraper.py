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


def test_scraper_only_block_pngs(tmpdir):
    """Only PNGs named in the block are collected, e.g. for parallel builds."""
    pytest.importorskip("sphinx_gallery")
    scraper = _get_sg_image_scraper()
    src_dir = str(tmpdir)
    A = pgv.AGraph()
    A.add_edge(1, 2)
    A.layout()
    # "other.png" stands in for an image written by another example in the
    # same directory that is running at the same time
    for name in ("mine.png", "other.png"):
        A.draw(os.path.join(src_dir, name))
    out_dir = os.path.join(src_dir, "build", "html")
    os.makedirs(out_dir)
    out_files = [os.path.join(out_dir, f"img_{ii}.png") for ii in range(2)]
    block = ("code", 'A.draw("mine.png")', 1)
    block_vars = {
        "image_path_iterator": iter(out_files),
        "src_file": os.path.join(src_dir, "mine.py"),
    }
    gallery_conf = {"src_dir": src_dir, "builder_name": "html"}
    rst = scraper(block, block_vars, gallery_conf)
    assert os.path.isfile(out_files[0])
    assert not os.path.isfile(out_files[1])
    assert "img_0.png" in rst
    assert not os.path.isfile(os.path.join(src_dir, "mine.png"))
    assert os.path.isfile(os.path.join(src_dir, "other.png"))


def test_scraper_same_name_twice(tmpdir):
    """A file name reused by a later block (or example) is collected again."""
    pytest.importorskip("sphinx_gallery")
    scraper = _get_sg_image_scraper()
    src_dir = str(tmpdir)
    A = pgv.AGraph()
    A.add_edge(1, 2)
    A.layout()
    out_dir = os.path.join(src_dir, "build", "html")
    os.makedirs(out_dir)
    block = ("code", 'A.draw("same.png")', 1)
    gallery_conf = {"src_dir": src_dir, "builder_name": "html"}
    for ii in range(2):
        A.draw(os.path.join(src_dir, "same.png"))
        out_file = os.path.join(out_dir, f"img_{ii}.png")
        block_vars = {
            "image_path_iterator": iter([out_file]),
            "src_file": os.path.join(src_dir, f"example_{ii}.py"),
        }
        scraper(block, block_vars, gallery_conf)
        assert os.path.isfile(out_file)
