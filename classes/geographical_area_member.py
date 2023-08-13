from collections import OrderedDict


class GeographicalAreaMember:
    def __init__(self, row):
        self.parent_id = row[0]
        self.parent_description = row[1]
        self.child_id = row[2]
        self.child_description = row[3]

    def api_response(self):
        r = OrderedDict()

        # r["parent_id"] = self.parent_id
        # r["parent_description"] = self.parent_description
        r["child_id"] = self.child_id
        r["child_description"] = self.child_description

        return r
