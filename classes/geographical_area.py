from collections import OrderedDict


class GeographicalArea:
    def __init__(self, row, geographical_area_members):
        self.geographical_area_sid = row[0]
        self.geographical_area_id = row[1]
        self.description = row[2]
        self.geographical_code = int(row[3])
        self.members = []
        self.check_members(geographical_area_members)
        self.get_weighting()
        self.get_friendly()

    def get_weighting(self):
        if self.geographical_code == 1:
            self.weighting = 99
        else:
            self.weighting = 0

    def get_friendly(self):
        replacements = {
            "1011": {
                "geographical_area_sid": 400,
                "geographical_area_id": "1011",
                "description": "Other countries"
            },
            "1008": {
                "geographical_area_sid": 400,
                "geographical_area_id": "1008",
                "description": "Other countries"
            },
            "1013": {
                "geographical_area_sid": 400,
                "geographical_area_id": "1013",
                "description": "European Union member states"
            }
        }
        # replacements = {}
        if self.geographical_area_id in replacements:
            for replacement in replacements:
                if self.geographical_area_id == replacement:
                    self.geographical_area_sid = replacements[replacement]["geographical_area_sid"]
                    self.geographical_area_id = replacements[replacement]["geographical_area_id"]
                    self.description = replacements[replacement]["description"]

    def check_members(self, geographical_area_members):
        for member in geographical_area_members:
            if member.parent_id == self.geographical_area_id:
                self.members.append(member.api_response())

    def api_response(self):
        r = OrderedDict()

        r["geographical_area_sid"] = self.geographical_area_sid
        r["geographical_area_id"] = self.geographical_area_id
        r["description"] = self.description
        r["geographical_code"] = self.geographical_code
        r["members"] = self.members

        return r
