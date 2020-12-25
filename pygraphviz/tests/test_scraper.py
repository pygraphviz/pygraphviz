import io
import os

import pytest
from pygraphviz.scraper import PNGScraper

simple = """
import pygraphviz as pgv

A = pgv.AGraph()
A.add_edge(1, 2)
A.layout()
A.draw("simple.png")
"""


def test_scraper(tmpdir):
    pytest.importorskip("sphinx_gallery")
    scraper = PNGScraper()
    src_dir = str(tmpdir)
    out_dir = os.path.join(str(tmpdir), "build", "html")
    img_fname = os.path.join(src_dir, "auto_examples", "images", "sg_img.png")
    gallery_conf = {"src_dir": src_dir, "builder_name": "html"}
    target_file = os.path.join(src_dir, "auto_examples", "plot_test.py")
    print(target_file)
    block = None
    block_vars = dict(
        image_path_iterator=(img for img in [img_fname]),
        example_globals=dict(a=1),
        src_file=target_file,
    )
    os.makedirs(os.path.dirname(img_fname))
    with open(target_file, "w") as fh:
        fh.write('"""\nSimple\n======\n"""')
        fh.write(simple)
    assert not os.path.isfile(img_fname)
    os.makedirs(out_dir)
    scraper(block, block_vars, gallery_conf)
    print(img_fname)
    assert os.path.isfile(img_fname)
