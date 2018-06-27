#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

class Env_FX:
    def __init__(self, chart, len_input):
        self.chart_raw, self.chart_diff = self._arrange_chart(chart, len_input)
        self.action_space = ActionSpace(3)
        self.len_input = len_input

        self.idx = 0
        self.position = 0

    def _arrange_chart(self, chart, len_input):
        chart_diff_ = list(np.array(chart[1:]) - np.array(chart[:-1]))
        chart = chart[1:]
        chart_raw = []
        chart_diff = []
        for i in range(len(chart)-len_input+1):
            chart_raw.append(chart[i:i+len_input])
            chart_diff.append(chart_diff_[i:i+len_input])
        return chart_raw, chart_diff

    def reset(self):
        self.idx = 0
        self.position = 0
        return self.chart_diff[0] + [0]

    def step(self, action):
        reward = 0
        price = self.chart_raw[self.idx][-1]
        # buy
        if action == 1:
            if self.position < 0:
                reward = int((-self.position - price)*100)
                self.position = 0
            elif self.position == 0:
                self.position = price
        # sell
        elif action == 2:
            if self.position > 0:
                reward = int((price - self.position)*100)
                self.position = 0
            elif self.position == 0:
                self.position = -price

        self.idx += 1
        if self.idx == len(self.chart_raw):
            return (self.chart_diff[self.idx-1]+[np.sign(self.position)], reward, True)
        else:
            return (self.chart_diff[self.idx]+[np.sign(self.position)], reward, False)



class ActionSpace:
    def __init__(self, n):
        self.n = n

    def sample(self):
        return random.randrange(self.n)



