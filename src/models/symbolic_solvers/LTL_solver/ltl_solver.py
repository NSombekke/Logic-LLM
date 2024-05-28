import flloat
from flloat.parser.ltlf import LTLfParser
import subprocess
from subprocess import check_output
from os.path import join
import os
import ast


class LTL_program:
    def __init__(self, logic_program: str, dataset_name=str) -> None:
        self.logic_program = logic_program
        self.flag = self.parse_logic_program()
        self.dataset_name = dataset_name

    def parse_logic_program(self):
        lines = [
            x.strip() for x in self.logic_program.splitlines() if not x.strip() == ""
        ]
        print(self.logic_program)
        print(lines)
        raw_start_index = lines.index("# raw LTL formula of the question:")
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
        formula = f"{self.raw_formula[0]}"
        parsed_formula = parser(formula)
        self.answers = []

        for option in self.options:
            try:
                print('trying...')
                option = ast.literal_eval(option)
                parsed_formula.truth(option, 0)
                self.answers.append(parsed_formula.truth(option, 0))
            except Exception as e:
                self.answers.append(False)

        if self.answers.count(True) == 0:
            return self.answers, "Error: No option is correct"
        elif self.answers.count(True) > 1:
            return self.answers, "Error: More than one option is correct"

        return self.answers, ""

    def answer_mapping(self, answers):
        mapping = {0: "A", 1: "B", 2: "C"}
        answer = [i for i in range(len(answers)) if answers[i] == True]
        if len(answer) == 1:
            return mapping[answer[0]]
        else:
            print("Warning: More or less than one option is correct")
            return len(answer)
