from typing import Optional
import numpy as np
from ..base_module import BaseTaskClass, TestItem
from .lab9_gen import start_gen

DEFAULT_TYPE = "int64"
INT_TYPES = {
    "int64":  np.int64,
    "int32":  np.int32,
    "int16":  np.int16,
    "int8":   np.int8,
    "uint64": np.uint64,
    "uint32": np.uint32,
    "uint16": np.uint16,
    "uint8":  np.uint8
}
TASK_DESCRIPTION = """
Вам предоставлена сломанная программа которая, ваша задача найти в чем ошибка в коде, и исправить его, чтобы программа выводила SUCCESS.
Для решения требуется чтобы условие t3 == t4 было истинно. Изначально t4 = 0.  Загрузите исправленный код для проверки.

Ваша функция с ошибкой:   

"""

PRINT_RESULT_C = r"""
#include<stdio.h>
#include<stdint.h>

void print_result(int64_t result){
    fprintf(stderr, "%ld\n", result);
}
"""


class Lab9First(BaseTaskClass):
    def __init__(
            self, *args,
            n: int,
            deep: int,
            answer: str = "",
            **kwself
    ):
        super().__init__(*args, **kwself)
        self.deep = deep
        self.asm_code, self.expected_result = start_gen(n=n, deep=self.deep, student_id=self.seed)
        self.answer = answer
        self.check_files = {
            "print_result.c": PRINT_RESULT_C,
        }


    def load_student_solution(
    self, solfile: Optional[str] = None, solcode: Optional[str] = None):
    # Do nothing, pass solution (answer) as argument
        pass


    def generate_task(self) -> str:
        return TASK_DESCRIPTION + self.asm_code


    def check_sol_prereq(self) -> Optional[str]:
        return None


    def compile(self) -> Optional[str]:
        return None
    

    def run_tests(self) -> tuple[bool, str]:
        self.check_files["main.s"] = self.asm_code.replace("_start", "main")
        self.solution = ""
        if (err := self._compile_internal(compile_args="-static")) is not None:
            return (False, f"Bad source code generated. Error: {err}.\n"
                            "Contact to the authors to solve the problem"
                    )

        dummy_test = TestItem(
            input_str="", showed_input="",
            expected="text", compare_func=self._compare_default
        )
        res = self._run_solution_internal(dummy_test)
        if res is None:
            return (False, "Bad source code generated.\n"
                            "Contact to the authors to solve the problem"
                    )
        if self.answer.strip() == str(self.expected_result).strip():
            return True, "OK"
        return False, "Wrong answer"


    def _generate_tests(self):
        pass