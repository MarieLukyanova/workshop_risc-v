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

MAIN_S = r"""
.globl main
.text
main:
    la a0, x
    call read_data
    ld a1, x
    call solution
    call print_result
    addi a0, x0, 0
    addi a7, x0, 93
    ecall


.data
x: .dword 0
"""

PRINT_RESULT_C = r"""
#include<stdio.h>
#include<stdint.h>

void print_result(int64_t result){
    fprintf(stderr, "%ld\n", result);
}

void read_data(int64_t *a, int64_t *b){
    scanf("%ld %ld", a, b);
}
"""


class Lab9First(BaseTaskClass):
    def __init__(
            self, *args,
            n: int,
            deep: int,
            student_id: int,
            **kwself
    ):
        super().__init__(*args, **kwself)
        self.deep = deep
        self.student_id = student_id
        self.asm_code, self.expected_result = start_gen(n=n, deep=self.deep, student_id=self.student_id)
        self.check_files = {
            "main.s": MAIN_S,
            "print_result.c": PRINT_RESULT_C,
        }

    def generate_task(self) -> str:
        return TASK_DESCRIPTION + self.asm_code

    def _generate_tests(self):
        self.tests = []
        self.tests.append(TestItem(
            input_str=f"{self.expected_result}",
            showed_input=f"",
            expected=str(self.expected_result),
            compare_func=self._compare_default
        ))