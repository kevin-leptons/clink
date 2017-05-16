class TestOrder():
    x = 1

    def test_1(self):
        assert self.x == 1
        self.x = 2

    def test_2(self):
        assert self.x == 2
        self.x = 3

    def test_3(self):
        assert self.x == 4

    def test_4(self):
        assert self.x == 3
