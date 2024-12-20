import pytest
import punctilious as pu
import uuid
from test_shared_library import create_atomic_connector, create_function


class TestSlug:
    def test_slug(self):
        """Test of representation with multiple string-constant renderers.
        """

        s1 = pu.Slug("foo")
        s2 = pu.Slug("bar")
        s3 = pu.Slug("foo")
        assert s1 != s2
        assert s1 == s3

    def test_unique_identifier(self):
        uuid1 = uuid.uuid4()
        uuid2 = uuid.uuid4()
        foo = pu.Slug('foo')
        bar = pu.Slug('bar')
        taz = pu.Slug('taz')
        i1 = pu.UniqueIdentifier(foo, uuid1)
        i2 = pu.UniqueIdentifier(bar, uuid2)
        with pytest.raises(Exception):
            pu.UniqueIdentifier(taz, uuid1)
        with pytest.raises(Exception):
            pu.UniqueIdentifier(foo, uuid1)
        print(hash(i1))
        assert i1.slug == pu.Slug('foo')
        assert i2.slug == pu.Slug('bar')
        assert i1 == i1
        assert i1 != i2
