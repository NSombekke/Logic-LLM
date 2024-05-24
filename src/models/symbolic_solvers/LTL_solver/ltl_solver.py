import flloat
from flloat.parser.ltlf import LTLfParser
import subprocess
from subprocess import check_output
from os.path import join
import os


class LTL_program:
    def __init__(self, logic_program: str, dataset_name=str) -> None:
        self.logic_program = logic_program
        self.flag = self.parse_logic_program()
        self.dataset_name = dataset_name

    def parse_logic_program(self):
        lines = [x for x in self.logic_program.splitlines() if not x.strip() == ""]
        raw_start_index = lines.index("# raw")
        option_start_index = lines.index("# Options")

        self.raw_formula = lines[raw_start_index + 1 : option_start_index]
        option_traces = lines[option_start_index + 1 :]

        try:
            self.options = [
                x.split(":::")[0].strip()
                for x in option_traces
                if not x.startswith("Question :::")
            ]
        except Exception as e:
            return False

        return True

    def execute_program(self):
        parser = LTLfParser()

        parsed_formula = parser(self.raw_formula)
        self.answers = []

        for option in self.options:
            try:
                parsed_formula.truth(option, 0)
                self.answers.append(parsed_formula.truth(option, 0))
            except Exception as e:
                self.answers.append(False)

        if self.answers.count(True) == 0:
            return self.answers, "Error: No option is correct"
        elif self.answers.count(True) > 1:
            return self.answers, "Error: More than one option is correct"

        return self.answers, ""

    def answer_mapping(self):
        mapping = {0: "A", 1: "B", 2: "C"}
        answer = [i for i in range(len(self.answers)) if self.answers[i] == True]
        if len(answer) == 1:
            return mapping[answer[0]]
        elif len(answer) == 0:
            return "Warning: No option is correct"
        else:
            return "Warning: More than one option is correct"
