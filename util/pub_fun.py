# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 20:13:32 2022

@author: Haiyi
@email: yyy99910@gmail.com
@wechart: yyy99966
@github: https://github.com/
"""
import math


def downRound(num,digits):
    num=num*math.pow(10,digits)
    num=math.floor(num)/math.pow(10,digits)
    print(num)
    return num
if __name__ == "__main__":
    downRound(3.14636,2)

