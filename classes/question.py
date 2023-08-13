class Question:
    def __init__(self, row):
        self.document_code = row[0]
        self.measure_type_id = row[1]
        self.question = row[2]
        self.hint = row[3]
        self.implies_wf_category = row[4]
        self.positive = row[5]

    def api_response(self):
        r = {
            "document_code": self.document_code,
            "measure_type_id": self.measure_type_id,
            "question": self.question,
            "hint": self.hint,
            "implies_wf_category": self.implies_wf_category,
            "positive": self.positive,
        }
        return r
