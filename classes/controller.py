from classes.commodity import Commodity


class Controller:
    def __init__(self):
        pass

    def get_commodity(self, goods_nomenclature_item_id, geographical_area_id=None, args=None):
        commodity = Commodity(goods_nomenclature_item_id, geographical_area_id, args)
        return commodity.api_response()
