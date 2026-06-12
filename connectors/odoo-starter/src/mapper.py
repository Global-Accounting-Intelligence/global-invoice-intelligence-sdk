def map_odoo_product_to_material(product: dict) -> dict:
    return {'material_id': product.get('id'), 'name': product.get('name')}
