from typing import Any, Dict

import numpy as np

class GeoJSONFormatter:
    def __init__(self, data: Dict[str, Any], right_hand_rule=True):
        self.raw_data = self.processed_data = data
        if right_hand_rule:
            self.right_hand_rule()
        self.round_decimal(6)

    def right_hand_rule(self):
        """
        Section 3.1.6 https://datatracker.ietf.org/doc/html/rfc7946
        
        A linear ring MUST follow the right-hand rule with respect to the
        area it bounds, i.e., exterior rings are counterclockwise, and
        holes are clockwise.
        """

        data = self.processed_data['features'][0]['geometry']['coordinates'][0]
        data = data[::-1]
        self.processed_data['features'][0]['geometry']['coordinates'][0] = data

    def round_decimal(self, n: int = 0):
        data = self.processed_data['features'][0]['geometry']['coordinates'][0]
        arr = np.array(data)
        data = arr.round(n).tolist()
        self.processed_data['features'][0]['geometry']['coordinates'][0] = data
    
    def get_processed_data(self) -> Dict[str, Any]:
        return self.processed_data