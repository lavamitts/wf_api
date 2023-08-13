from collections import OrderedDict


class Measure:
    def __init__(self, row, measure_conditions):
        self.shared = None
        self.measure_sid = row[0]
        self.measure_type_id = row[1]
        self.geographical_area_id = row[2] if row[2] != "EU" else "1013"
        self.measure_type_description = row[3]
        self.validity_start_date = row[4]
        self.validity_end_date = row[5]
        self.measure_generating_regulation_id = row[6]
        self.goods_nomenclature_item_id = row[7]
        self.goods_nomenclature_sid = row[8]

        self.impacts_windsor_framework = row[9]
        self.theme_id = row[10]
        self.information_text = row[11]

        self.measure_conditions = []
        self.members = [self.geographical_area_id]
        self.get_measure_conditions(measure_conditions)

    def get_measure_conditions(self, measure_conditions):
        for mc in measure_conditions:
            if mc.measure_sid == self.measure_sid:
                self.measure_conditions.append(mc.api_response())

    def apply_members(self, members):
        if len(self.geographical_area_id) == 4:
            for member in members:
                if member.parent_id == self.geographical_area_id:
                    self.members.append(member.child_id)
        a = 1

    def api_response(self):
        r = OrderedDict()
        r["measure_sid"] = self.measure_sid
        r["measure_type_id"] = self.measure_type_id
        r["measure_type_description"] = self.measure_type_description
        r["geographical_area_id"] = self.geographical_area_id
        r["measure_generating_regulation_id"] = self.measure_generating_regulation_id
        r["shared"] = self.shared
        r["validity_start_date"] = self.validity_start_date
        r["validity_end_date"] = self.validity_end_date
        r["measure_conditions"] = self.measure_conditions
        r["impacts_windsor_framework"] = self.impacts_windsor_framework
        r["theme_id"] = self.theme_id
        r["information_text"] = self.information_text
        return r
