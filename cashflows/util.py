import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


class Cashflow(object):

    def __init__(self, **kwargs):
        self.amount = kwargs['amount']
        self.t = kwargs['t']

    def present_value(self, interest_rate):
        pv = self.amount/((1 + interest_rate)**self.t)
        return pv


class InvestmentProject(object):
    RISK_FREE_RATE = 0.08

    def __init__(self, cashflows, hurdle_rate=RISK_FREE_RATE):
        cashflows_positions = {str(flow.t): flow for flow in cashflows}
        self.cashflow_max_position = max((flow.t for flow in cashflows))
        self.cashflows = []
        for t in range(self.cashflow_max_position + 1):
            self.cashflows.append(cashflows_positions.get(str(t), Cashflow(t=t, amount=0)))
        self.hurdle_rate = hurdle_rate if hurdle_rate else InvestmentProject.RISK_FREE_RATE

    @staticmethod
    def from_csv(filepath, hurdle_rate=RISK_FREE_RATE):
        cashflows = [Cashflow(**row) for row in pd.read_csv(filepath).T.to_dict().values()]
        return InvestmentProject(cashflows=cashflows, hurdle_rate=hurdle_rate)

    @property
    def internal_return_rate(self):
        return np.irr([flow.amount for flow in self.cashflows])

    def plot(self, show=False):
        _amount_ = []
        _t_ = []
        for obj in self.cashflows:
            _amount_.append(obj.amount)
            _t_.append(obj.t)
        fig = plt.figure(1)
        plt.bar(np.arange(len(_amount_)), _amount_)
        plt.xticks(np.arange(len(_t_)), _t_)
        plt.title('CashFlow')
        plt.xlabel('t')
        plt.ylabel('amount')
        if show:
            plt.show()
        return fig

    def net_present_value(self, interest_rate=None):
        npv = 0
        if interest_rate is None:
            interest_rate = self.hurdle_rate
        for i in self.cashflows:
            npv = npv + i.present_value(interest_rate=interest_rate)
        return npv

    def equivalent_annuity(self, interest_rate=None):
        if not interest_rate:
            interest_rate = self.hurdle_rate
        annuity = (self.net_present_value(interest_rate)*interest_rate)/(1-(1 + interest_rate)**(-self.cashflow_max_position))
        return annuity

    def describe(self):
        return {
            "irr": self.internal_return_rate,
            "hurdle-rate": self.hurdle_rate,
            "net-present-value": self.net_present_value(interest_rate=None),
            "equivalent-annuity": self.equivalent_annuity(interest_rate=None)
        }