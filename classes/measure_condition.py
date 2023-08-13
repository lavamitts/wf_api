class MeasureCondition:
    def __init__(self, row):
        self.measure_sid = row[0]
        self.measure_condition_sid = row[1]
        self.condition_code = row[2]
        self.certificate_type_code = row[3]
        self.certificate_code = row[4]
        self.condition_duty_amount = row[5]
        self.condition_monetary_unit_code = row[6]
        self.condition_measurement_unit_code = row[7]
        self.condition_measurement_unit_qualifier_code = row[8]
        self.certificate_code = row[9]
        self.certificate_description = row[10]

    def api_response(self):
        r = {
            "measure_condition_sid": self.measure_condition_sid,
            "certificate_code": self.certificate_code,
            "certificate_description": self.certificate_description,
        }
        return r
