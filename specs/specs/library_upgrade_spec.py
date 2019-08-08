from expects import expect, be_empty
from mamba import description, it

from library_upgrade import get_libraries

with description("get libraries") as self:
    with it("should return an empty list for an empty file"):
        expect(get_libraries([])).to(be_empty)
