import unittest

def run():
    """Runs the testsuite as command line application."""
    try:
        unittest.main(testLoader=BetterLoader(), defaultTest='suite')
    except Exception as e:
        print('Error: %s' % e)
