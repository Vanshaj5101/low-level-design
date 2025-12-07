class LegacyRectangle:
    def draw_legacy(self, x1, y1, x2, y2):
        print(f"drawing rectangle from ({x1}, {y1}) to ({x2}, {y2})")


class RectangleAdapter:
    def __init__(self, rectangle):
        self.rectangle = rectangle

    def draw(self, x, y, width, height):
        x2 = x + width
        y2 = y + height
        self.rectangle.draw_legacy(x, y, x2, y2)


# Client code
legacy = LegacyRectangle()
adapter = RectangleAdapter(legacy)
adapter.draw(10, 20, 30, 40)
