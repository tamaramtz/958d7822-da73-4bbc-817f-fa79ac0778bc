import fire
import json 

from util import Cashflow
from util import InvestmentProject


class Main(object):

    def present_value(self, amount, t, i):
        flow = Cashflow(amount, t)
        print ("The present value of cashflow{amount} in time {t} is {pv}.".format(amount=amount, t=t,
                                                                                   pv=flow.present_value(
                                                                                       interest_rate=i)))
    @staticmethod
    def describe_investment(filepath, hurdle_rate=None):
        investment_project = InvestmentProject.from_csv(filepath=filepath, hurdle_rate=hurdle_rate)
        description = investment_project.describe()
        print(json.dumps(description, indent=4))

    @staticmethod
    def plot_investment(filepath, save="", show=False):
        inv =InvestmentProject(cashflows, hurdle_rate)
        fig = inv.plot()
        if save:
            fig.savefig(save)


if __name__ == "__main__":
    fire.Fire(Main)
#What does it means when the internal-rate of return is greater than the hurdle rate?
#If the IRR exceeds the hurdle rate, the project would most likely be executed. Because the investment creates value.

#Can the net present value be negative? Why?
#Yes, because it means that when the value of the outflows is greater than the inflows, the NPV is negative.
