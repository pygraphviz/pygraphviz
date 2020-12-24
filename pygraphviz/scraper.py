import os
from glob import glob
import shutil


def _get_sg_image_scraper():
    """Return the callable scraper to be used by Sphinx-Gallery.

    It allows PyGraphviz users to just use strings as they already can for
    'matplotlib' and 'mayavi'. Details on this implementation can be found in
    `sphinx-gallery/sphinx-gallery/494`_

    .. _sphinx-gallery/sphinx-gallery/494: https://github.com/sphinx-gallery/sphinx-gallery/pull/494
    """
    return PNGScraper()


class PNGScraper:
    """A callable image scraper for png outputs from pygraphviz examples
    for sphinx-gallery.

    Can be used to collect `.png` files generated by pygraphviz in
    sphinx-gallery examples by adding the following to the ``conf.py``::

        sphinx_gallery_conf = {
            ...
            'image_scrapers': ('matplotlib', 'pygraphviz'),
        }

    This class is based on the recipe provide in [1]_.

    References
    ----------
    .. [1] sphinx-gallery documentation - custom image scraper.
       https://sphinx-gallery.github.io/stable/advanced.html
    """

    def __init__(self):
        self.seen = set()

    def __repr__(self):
        return "PNGScraper"

    def __call__(self, block, block_vars, gallery_conf):
        """
        Scrape .png images created by pygraphviz examples.

        Invoked by sphinx-gallery.

        Parameters
        ----------
        block : tuple
            A tuple containing the (label, content, line_number of the
            block.
        block_vars : dict
            Dict of block variables
        gallery_conf : dict
            Mapping of sphinx-gallery configuration values

        Returns
        -------
        str :
            rST-formatted string containing the generated images. This will
            be rendered to HTML during the ``sphinx-build`` process.
        """
        try:
            from sphinx_gallery.scrapers import figure_rst
        except ImportError as e:
            raise ImportError("You must install `sphinx_gallery`") from e

        # Find all PNG files in the directory of this example
        path_current_example = os.path.dirname(block_vars["src_file"])
        pngs = sorted(glob(os.path.join(path_current_example, "*.png")))

        # Iterate through PNGs and copy them to sphinx-gallery output dir
        image_names = []
        image_path_iterator = block_vars["image_path_iterator"]
        for png in pngs:
            if png not in self.seen:
                self.seen |= set(png)
                this_image_path = image_path_iterator.next()
                image_names.append(this_image_path)
                shutil.move(png, this_image_path)

        # Use figure_rst to generate rST for image files
        return figure_rst(image_names, gallery_conf["src_dir"])
