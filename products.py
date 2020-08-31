"""Create product class."""


class Product:
    """Define product class."""

    def __init__(self, title, description, media, size, price):
        """Initialize properties of product class."""
        self.title = title
        self.price = price
        self.description = description
        self.media = media
        self.size = size
