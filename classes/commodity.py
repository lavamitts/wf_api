import os

from collections import OrderedDict
from classes.database import Database
from classes.geographical_area import GeographicalArea
from classes.geographical_area_member import GeographicalAreaMember
from classes.measure import Measure
from classes.measure_condition import MeasureCondition
from classes.question import Question
from classes.argument import Argument
import classes.functions as f


class Commodity:
    def __init__(self, goods_nomenclature_item_id, geographical_area_id=None, args=None):
        self.sql_folder = os.path.join(os.getcwd(), "sql")
        self.goods_nomenclature_item_id = goods_nomenclature_item_id
        self.geographical_area_id = geographical_area_id
        self.args = args
        self.geographical_area_description = ""
        self.questions = []
        self.decision = None

        self.get_args()

        self.expand_commodity()
        self.get_commodity_code_data()
        self.get_measure_conditions()
        self.get_measures()
        self.get_measure_uptree_downtree()
        self.get_geographical_area_members()
        self.get_geographical_areas()
        self.check_if_geography_matters()
        self.filter_measures()
        self.get_regulations()
        self.get_wf_questions()
        self.interpret_arguments()

    def expand_commodity(self):
        self.goods_nomenclature_item_id = self.goods_nomenclature_item_id.ljust(
            10, '0')

    def get_commodity_code_data(self):
        sql = f.get_sql(self.sql_folder, "get_commodity")
        params = [self.goods_nomenclature_item_id]
        d = Database("xi")
        rows = d.run_query(sql, params)
        if rows:
            row = rows[0]
            self.goods_nomenclature_sid = row[0]
            self.goods_nomenclature_item_id = row[1]
            self.description = row[2]
            self.productline_suffix = row[3]
            self.down_tree = row[4]
            self.up_tree = row[5]
            self.leaf = row[6]
            self.significant_digits = row[7]
            self.interest_to_wf = row[8]
            self.uptree_downtree = self.down_tree + \
                self.up_tree + [self.goods_nomenclature_sid]
            self.uptree_downtree = tuple(self.uptree_downtree)

    def get_measures(self):
        self.geographical_area_ids = []
        self.measure_objects = []
        self.measures = []
        params = [self.uptree_downtree]
        sql = f.get_sql(self.sql_folder, "get_measures")
        d = Database("xi")
        rows = d.run_query(sql, params)
        if rows:
            for row in rows:
                measure = Measure(row, self.measure_conditions)
                if measure.impacts_windsor_framework:
                    if measure.geographical_area_id not in self.geographical_area_ids:
                        self.geographical_area_ids.append(
                            measure.geographical_area_id)

                    self.measures.append(measure.api_response())
                    self.measure_objects.append(measure)
        self.geographical_area_ids.sort()

    def get_measure_uptree_downtree(self):
        for measure in self.measure_objects:
            if measure.goods_nomenclature_sid == self.goods_nomenclature_sid:
                measure.shared = True
            elif measure.goods_nomenclature_sid in self.up_tree:
                measure.shared = True
            else:
                measure.shared = False

    def check_if_geography_matters(self):
        self.geography_matters = False
        self.geography_options = []
        geography_ids = []
        if self.geographical_area_id is None:
            for measure in self.measure_objects:
                if measure.geographical_area_id not in geography_ids:
                    obj = {
                        "geographical_area_id": measure.geographical_area_id,
                        "description": self.geographical_areas_dict[measure.geographical_area_id].description,
                        "weighting": self.geographical_areas_dict[measure.geographical_area_id].weighting
                    }
                    self.geography_options.append(obj)
                    geography_ids.append(measure.geographical_area_id)
                if measure.geographical_area_id not in ["1008", "1011"]:
                    self.geography_matters = True

        self.geography_options = sorted(
            self.geography_options, key=lambda x: x["description"], reverse=False)
        self.geography_options = sorted(
            self.geography_options, key=lambda x: x["weighting"], reverse=False)

    def filter_measures(self):
        # filter by regulation
        # filter by geography
        self.measures = []
        self.regulations = []
        self.regulation_ids = []
        if self.geographical_area_id is not None:
            for measure in self.measure_objects:
                if measure.measure_generating_regulation_id not in self.regulation_ids:
                    obj = {
                        "regulation_id": measure.measure_generating_regulation_id,
                        "information_text": measure.information_text,
                        "impacts_windsor_framework": measure.impacts_windsor_framework,
                        "theme_id": measure.theme_id
                    }
                    self.regulations.append(obj)
                    self.regulation_ids.append(
                        measure.measure_generating_regulation_id)
                measure.apply_members(self.geographical_area_members)
                if self.geographical_area_id in measure.members:
                    self.measures.append(measure.api_response())
        else:
            for measure in self.measure_objects:
                self.measures.append(measure.api_response())
                if measure.measure_generating_regulation_id not in self.regulation_ids:
                    obj = {
                        "regulation_id": measure.measure_generating_regulation_id,
                        "information_text": measure.information_text,
                        "impacts_windsor_framework": measure.impacts_windsor_framework,
                        "theme_id": measure.theme_id
                    }
                    self.regulations.append(obj)
                    self.regulation_ids.append(
                        measure.measure_generating_regulation_id)

    def get_regulations(self):
        return

    def get_wf_questions(self):
        self.question_objects = []
        keys = []
        for measure in self.measure_objects:
            if self.geographical_area_id in measure.members:
                if measure.impacts_windsor_framework:
                    for condition in measure.measure_conditions:
                        if condition["certificate_code"] is not None:
                            key = "{measure_type_id}_{certificate_code}".format(
                                measure_type_id=measure.measure_type_id,
                                certificate_code=condition["certificate_code"],
                            )
                            keys.append(key)

        if len(keys) > 0:
            keys = tuple(keys)
            sql = f.get_sql(self.sql_folder, "get_questions")
            params = [keys]
            d = Database("xi")
            rows = d.run_query(sql, params)
            if rows:
                for row in rows:
                    question_object = Question(row)
                    self.question_objects.append(question_object)

        if len(self.question_objects) > 0:
            # Sort by category implied, then by mesaure type
            self.question_objects = sorted(
                self.question_objects, key=lambda x: x.measure_type_id, reverse=False)

            self.question_objects = sorted(
                self.question_objects, key=lambda x: x.implies_wf_category, reverse=False)

            for question in self.question_objects:
                self.questions.append(question.api_response())

    def get_measure_conditions(self):
        self.measure_conditions = []
        params = [self.uptree_downtree]
        sql = f.get_sql(self.sql_folder, "get_measure_conditions")
        d = Database("xi")
        rows = d.run_query(sql, params)
        if rows:
            for row in rows:
                measure_condition = MeasureCondition(row)
                self.measure_conditions.append(measure_condition)

    def get_geographical_area_members(self):
        self.geographical_area_members = []
        sql = f.get_sql(self.sql_folder, "get_geographical_area_members")
        params = [tuple(self.geographical_area_ids)]
        d = Database("xi")
        rows = d.run_query(sql, params)
        if rows:
            for row in rows:
                geographical_area_member = GeographicalAreaMember(row)
                self.geographical_area_members.append(geographical_area_member)

        # Hack to get the currently selected geo ID without going back to the DB
        if self.geographical_area_id is not None:
            sql = f.get_sql(self.sql_folder, "get_my_geographical_area")
            params = [self.geographical_area_id]
            d = Database("xi")
            rows = d.run_query(sql, params)
            if rows:
                row = rows[0]
                self.geographical_area_description = row[2]

    def get_geographical_areas(self):
        self.geographical_areas = []
        self.geographical_areas_dict = {}
        sql = f.get_sql(self.sql_folder, "get_geographical_areas")
        params = [tuple(self.geographical_area_ids)]
        d = Database("xi")
        rows = d.run_query(sql, params)
        if rows:
            for row in rows:
                geographical_area = GeographicalArea(
                    row, self.geographical_area_members)
                self.geographical_areas.append(
                    geographical_area.api_response())
                self.geographical_areas_dict[geographical_area.geographical_area_id] = geographical_area

    def get_context(self):
        self.trade_context = {
            "goods_nomenclature_item_id": self.goods_nomenclature_item_id,
            "geographical_area_id": self.geographical_area_id,
            "geographical_area_description": self.geographical_area_description,
            "arguments": self.arguments_list,
            "decision": self.decision
        }

    def get_args(self):
        self.arguments = []
        self.arguments_list = []
        if self.args is not None:
            for arg in self.args:
                argument = Argument(arg, self.args[arg])
                self.arguments.append(argument)
                self.arguments_list.append(argument.api_response())

    def interpret_arguments(self):
        decision_made = False
        if len(self.arguments) > 0:
            for question in self.question_objects:
                if not decision_made:
                    for argument in self.arguments:
                        if question.document_code == argument.document_code:
                            if question.measure_type_id == argument.measure_type_id:
                                if argument.value is True:
                                    self.decision = question.implies_wf_category
                                    decision_made = True
                                    break

    def api_response(self):
        self.get_context()
        data = OrderedDict()
        data["goods_nomenclature_sid"] = self.goods_nomenclature_sid
        data["goods_nomenclature_item_id"] = self.goods_nomenclature_item_id
        data["productline_suffix"] = self.productline_suffix
        data["description"] = self.description
        data["leaf"] = self.leaf
        data["significant_digits"] = self.significant_digits
        data["interest_to_wf"] = self.interest_to_wf
        data["uptree_downtree"] = self.uptree_downtree
        data["geographical_area_ids"] = self.geographical_area_ids
        data["geography_matters"] = self.geography_matters
        data["geography_options"] = self.geography_options

        r = OrderedDict()
        r["data"] = data
        r["measures"] = self.measures
        r["questions"] = self.questions
        r["regulations"] = self.regulations
        r["geographical_areas"] = self.geographical_areas
        r["trade_context"] = self.trade_context

        return r
