class ERPNextConnector:
    def __init__(self, config: dict):
        self.config = config

    def export_materials(self) -> list[dict]:
        return []

    def push_match_result(self, match_result: dict) -> dict:
        return {"status": "not_implemented", "match_result": match_result}
