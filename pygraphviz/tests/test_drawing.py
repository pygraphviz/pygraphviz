from tempfile import TemporaryFile
import pygraphviz as pgv
import pytest


def test_drawing_error():
    with pytest.raises(AttributeError):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        d = A.draw()


def test_name_error():
    with pytest.raises(ValueError):
        A = pgv.AGraph(name="test graph")
        A.draw("foo", prog="foo")


def test_drawing_no_error_with_no_layout():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    d = A.draw(prog="nop")
    A.string_nop()


def test_drawing_makes_file_handle():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    with TemporaryFile() as fh:
        A.draw(fh, format="png", prog="twopi")
        assert fh.tell() > 0
    with TemporaryFile() as fh:
        A.draw(path=fh, prog="circo", format="png")
        assert fh.tell() > 0


def test_drawing_makes_file_path(tmp_path):
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    out = tmp_path / "draw.png"
    A.draw(out, format="png", prog="twopi")
    assert out.is_file()
    out2 = tmp_path / "draw.png"
    A.draw(str(out2), format="png", prog="twopi")
    assert out2.is_file()


def test_drawing_to_create_dot_string():
    A = pgv.AGraph(name="test graph")
    A.add_path([1, 2, 3, 4])
    A.layout()
    dot_rep = A.to_string()
    assert "test graph" in dot_rep
    assert "strict graph" in dot_rep
    assert "pos" in dot_rep
    assert "height" in dot_rep
    assert "width" in dot_rep
    assert "1 -- 2" in dot_rep
    assert "2 -- 3" in dot_rep
    assert "3 -- 4" in dot_rep

    # unfortunately, the layout and dot outcomes vary
    # with system and graphviz version. One example is
    # shown here, the numbers can be very different.
    expected = """strict graph "test graph" {
	graph [bb="0,0,70.071,250.3"];
	node [label="\\N"];
	1	[height=0.5,
		pos="27,18",
		width=0.75];
	2	[height=0.5,
		pos="43.071,88.469",
		width=0.75];
	1 -- 2	[pos="31.139,36.148 33.557,46.75 36.596,60.077 39.002,70.627"];
	3	[height=0.5,
		pos="41.467,160.69",
		width=0.75];
	2 -- 3	[pos="42.666,106.69 42.423,117.64 42.115,131.52 41.872,142.47"];
	4	[height=0.5,
		pos="32.966,232.3",
		width=0.75];
	3 -- 4	[pos="39.322,178.76 38.043,189.53 36.424,203.17 35.14,213.98"];
}
"""
    # print("dot representation:", dot_rep)
    # assert expected == dot_rep


class TestExperimentalGraphvizLibInterface:
    def test_drawing_error(self):
        with pytest.raises(AttributeError):
            A = pgv.AGraph(name="test graph")
            A.add_path([1, 2, 3, 4])
            d = A._draw()

    def test_name_error(self):
        with pytest.raises(ValueError):
            A = pgv.AGraph(name="test graph")
            A._draw("foo", prog="foo")

    def test_drawing_no_error_with_no_layout(self):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        d = A._draw(prog="nop")
        A.string_nop()

    def test_drawing_png_output_with_NULL_smoketest(self):
        """The PNG format can contain NULL bytes, which can cause cstring
        allocation problems if the size isn't handled correctly. See gh-424.
        """
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        d = A._draw(prog="dot", format="png")

    def test_drawing_to_create_dot_string(self):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        A._layout()
        dot_rep = A.to_string()
        assert "test graph" in dot_rep
        assert "strict graph" in dot_rep
        assert "pos" in dot_rep
        assert "height" in dot_rep
        assert "width" in dot_rep
        assert "1 -- 2" in dot_rep
        assert "2 -- 3" in dot_rep
        assert "3 -- 4" in dot_rep

        # unfortunately, the layout and dot outcomes vary
        # with system and graphviz version. One example is
        # shown here, the numbers can be very different.
        expected = """strict graph "test graph" {
        graph [bb="0,0,70.071,250.3"];
        node [label="\\N"];
        1	[height=0.5,
            pos="27,18",
            width=0.75];
        2	[height=0.5,
            pos="43.071,88.469",
            width=0.75];
        1 -- 2	[pos="31.139,36.148 33.557,46.75 36.596,60.077 39.002,70.627"];
        3	[height=0.5,
            pos="41.467,160.69",
            width=0.75];
        2 -- 3	[pos="42.666,106.69 42.423,117.64 42.115,131.52 41.872,142.47"];
        4	[height=0.5,
            pos="32.966,232.3",
            width=0.75];
        3 -- 4	[pos="39.322,178.76 38.043,189.53 36.424,203.17 35.14,213.98"];
    }
    """
        # print("dot representation:", dot_rep)
        # assert expected == dot_rep

    def test_drawing_makes_file(self):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        with TemporaryFile() as fh:
            A._draw(fh, format="png", prog="twopi")
            assert fh.tell() > 0

    def test_drawing_makes_file1(self):
        A = pgv.AGraph(name="test graph")
        A.add_path([1, 2, 3, 4])
        with TemporaryFile() as fh:
            A._draw(path=fh, prog="circo", format="png")
            assert fh.tell() > 0
