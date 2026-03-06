from seaweed_algebra import example

def test_pipeline_works():
    """A simple dummy test to ensure the CI pipeline runs successfully."""
    assert True

def test_import():
    """Test importing something from the library. Check that 1+1=2, literally."""
    assert example.add_one(1) == 2