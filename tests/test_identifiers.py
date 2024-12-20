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
        uid1 = pu.UniqueIdentifier(foo, uuid1)
        uid2 = pu.UniqueIdentifier(bar, uuid2)
        uid3 = pu.UniqueIdentifier(taz, uuid1)
        uid4 = pu.UniqueIdentifier(foo, uuid1)
        assert uid1.slug == pu.Slug('foo')
        assert uid2.slug == pu.Slug('bar')
        assert uid1 == uid1
        assert uid1 != uid2
        assert uid1 == uid3
        assert uid1 == uid4
        assert uid3 == uid4
