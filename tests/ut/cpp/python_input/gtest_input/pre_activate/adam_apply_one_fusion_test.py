# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
from mindspore.ops import operations as P
from mindspore.ops import Primitive

Add = P.TensorAdd()
Sub = P.Sub()
Mul = P.Mul()
RealDiv = P.RealDiv()
Sqrt = P.Sqrt()
Square = P.Square()
make_tuple = Primitive('make_tuple')
tuple_getitem = Primitive('tuple_getitem')
AdamApplyOne = Primitive('AdamApplyOne')


class FnDict:
    def __init__(self):
        self.fnDict = {}

    def __call__(self, fn):
        self.fnDict[fn.__name__] = fn

    def __getitem__(self, name):
        return self.fnDict[name]


def test_adam_apply_one_fusion(tag):
    fns = FnDict()

    @fns
    def before(input0, input1, input2, input3, input4, mul0_x, mul1_x, mul2_x, mul3_x, add2_y):
        square0 = Square(input0)
        mul1 = Mul(mul1_x, input0)
        mul0 = Mul(mul0_x, input2)
        mul2 = Mul(mul2_x, input1)
        mul3 = Mul(mul3_x, square0)
        add0 = Add(mul0, mul1)
        add1 = Add(mul2, mul3)
        sqrt0 = Sqrt(add1)
        add2 = Add(sqrt0, add2_y)
        true_div0 = RealDiv(add0, add2)
        mul4 = Mul(input4, true_div0)
        sub0 = Sub(input3, mul4)
        outputs = make_tuple(add1, add0, sub0)
        output = tuple_getitem(outputs, 0)
        return output

    @fns
    def before_cond1(input0, input1, input2, input3, input4, mul0_x, mul1_x, mul2_x, mul3_x, add2_y):
        square0 = Square(input0)
        mul1 = Mul(mul1_x, input0)
        mul0 = Mul(mul0_x, input2)
        mul2 = Mul(mul2_x, input1)
        mul3 = Mul(mul3_x, square0)
        add0 = Add(mul0, mul1)
        add1 = Add(mul2, mul3)
        sqrt0 = Sqrt(add1)
        add2 = Add(add2_y, sqrt0)
        true_div0 = RealDiv(add0, add2)
        mul4 = Mul(input4, true_div0)
        sub0 = Sub(input3, mul4)
        outputs = make_tuple(add1, add0, sub0)
        output = tuple_getitem(outputs, 0)
        return output

    @fns
    def before_cond2(input0, input1, input2, input3, input4, mul0_x, mul1_x, mul2_x, mul3_x, add2_y):
        square0 = Square(input0)
        mul1 = Mul(mul1_x, input0)
        mul0 = Mul(mul0_x, input2)
        mul2 = Mul(mul2_x, input1)
        mul3 = Mul(square0, mul3_x)
        add0 = Add(mul0, mul1)
        add1 = Add(mul2, mul3)
        sqrt0 = Sqrt(add1)
        add2 = Add(sqrt0, add2_y)
        true_div0 = RealDiv(add0, add2)
        mul4 = Mul(true_div0, input4)
        sub0 = Sub(input3, mul4)
        outputs = make_tuple(add1, add0, sub0)
        output = tuple_getitem(outputs, 0)
        return output

    @fns
    def before_cond3(input0, input1, input2, input3, input4, mul0_x, mul1_x, mul2_x, mul3_x, add2_y):
        square0 = Square(input0)
        mul1 = Mul(mul1_x, input0)
        mul0 = Mul(mul0_x, input2)
        mul2 = Mul(mul2_x, input1)
        mul3 = Mul(mul3_x, square0)
        add0 = Add(mul0, mul1)
        add1 = Add(mul2, mul3)
        sqrt0 = Sqrt(add1)
        add2 = Add(sqrt0, add2_y)
        true_div0 = RealDiv(add0, add2)
        mul4 = Mul(true_div0, input4)
        sub0 = Sub(input3, mul4)
        outputs = make_tuple(add1, add0, sub0)
        output = tuple_getitem(outputs, 0)
        return output

    @fns
    def before_cond4(input0, input1, input2, input3, input4, mul0_x, mul1_x, mul2_x, mul3_x, add2_y):
        square0 = Square(input0)
        mul1 = Mul(mul1_x, input0)
        mul0 = Mul(mul0_x, input2)
        mul2 = Mul(mul2_x, input1)
        mul3 = Mul(mul3_x, square0)
        add0 = Add(mul0, mul1)
        add1 = Add(mul2, mul3)
        sqrt0 = Sqrt(add1)
        add2 = Add(add2_y, sqrt0)
        true_div0 = RealDiv(add0, add2)
        mul4 = Mul(true_div0, input4)
        sub0 = Sub(input3, mul4)
        outputs = make_tuple(add1, add0, sub0)
        output = tuple_getitem(outputs, 0)
        return output

    @fns
    def after(input0, input1, input2, input3, input4, mul0_x, mul1_x, mul2_x, mul3_x, add2_y):
        adam_apply_one = AdamApplyOne(input0, input1, input2, input3, input4, mul0_x, mul1_x, mul2_x, mul3_x, add2_y)
        outputs = make_tuple(tuple_getitem(adam_apply_one, 0), tuple_getitem(adam_apply_one, 1),
                             tuple_getitem(adam_apply_one, 2))
        output = tuple_getitem(outputs, 0)
        return make_tuple(output)

    return fns[tag]
