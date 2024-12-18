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

    def test_identifier(self):
        uuid1 = uuid.uuid4()
        uuid2 = uuid.uuid4()
        foo = pu.Slug('foo')
        bar = pu.Slug('bar')
        taz = pu.Slug('taz')
        i1 = pu.UniqueIdentifier(uuid1, foo, bar)
        i2 = pu.UniqueIdentifier(uuid2, foo, bar)
        i3 = pu.UniqueIdentifier(uuid1, foo, bar)
        i4 = pu.UniqueIdentifier(uuid1, foo, taz)
        print(hash(i1))
        print(hash(i4))
        assert i1.package_slug == pu.Slug('foo')
        assert i1.package_uuid == uuid1
        assert i1.slug == pu.Slug('bar')
        assert i4.slug == pu.Slug('taz')
        assert i1 != i2
        assert i1 == i3
        assert i1 != i4
