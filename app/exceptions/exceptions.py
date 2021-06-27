class DBConnectionError(Exception):
    """
    Exception raised when connection with database cannot be established
    """
    def __init__(self, url: str=None, message: str="Failed to connect to the database"):
        self.message = message
        self.url = url
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} -> {self.url}"

class DBDisconnectError(Exception):
    def __init__(self, url: str=None, message: str="Failed to disconnect from the database"):
        self.message = message
        self.url = url
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} -> {self.url}"

class LatLonError(Exception):
    def __init__(self, lat: float, lon: float, message: str="Invalid coordinates"):
        self.lat = lat
        self.lon = lon
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} -> lat={self.lat:.4f} lon={self.lon:.4f}"

class TokenNotFoundError(Exception):
    def __init__(self, token: str, message: str="Token not found"):
        self.token = token
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} -> token={self.token}"