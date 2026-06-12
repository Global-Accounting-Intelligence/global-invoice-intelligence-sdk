def map_erpnext_item_to_material(item: dict) -> dict:
    return {
        "material_id": item.get("name"),
        "name": item.get("item_name") or item.get("name"),
        "aliases": [],
        "supplier_references": [],
        "barcodes": [item.get("barcode")] if item.get("barcode") else [],
        "uoms": [item.get("stock_uom")] if item.get("stock_uom") else [],
    }
