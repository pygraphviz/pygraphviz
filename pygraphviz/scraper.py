import os
from glob import glob
import shutil
from sphinx_gallery.scrapers import figure_rst

class PNGScraper():
    """A sphinx-gallery compliant image scraper for png outputs from pygraphviz
    examples.
    
    See <https://sphinx-gallery.github.io/stable/advanced.html>.
    """
    def __init__(self):
        self.seen = set()

    def __repr__(self):
        return 'PNGScraper'

    def __call__(self, block, block_vars, gallery_conf):
        # Find all PNG files in the directory of this example
        path_current_example = os.path.dirname(block_vars['src_file'])
        pngs = sorted(glob(os.path.join(path_current_example, '*.png')))

        # Iterate through PNGs and copy them to sphinx-gallery output dir
        image_names = []
        image_path_iterator = block_vars['image_path_iterator']
        for png in pngs:
            if png not in self.seen:
                self.seen |= set(png)
                this_image_path = image_path_iterator.next()
                image_names.append(this_image_path)
                shutil.move(png, this_image_path)

        # Use figure_rst to generate rST for image files
        return figure_rst(image_names, gallery_conf['src_dir'])
