import pandas as pd
from io import StringIO
from pulp import LpProblem, LpMaximize, LpMinimize, LpVariable, GLPK_CMD
import pulp

class SubstanceDataLoader():

    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        with open(self.filename, 'r') as f:
            data = f.read()

        data = data.split('\n\n')

        substances, substances_mix = data

        substances = StringIO(substances)
        substances = pd.read_csv(substances, sep=',', dtype={'name': str, 'cost': float, 'efficacy': float})

        substances_mix = StringIO(substances_mix)
        substances_mix = pd.read_csv(substances_mix, sep=',', index_col='name')
         
        return substances, substances_mix

class LPModel():
    
    def __init__(self, substances, substances_mix):
        self.substances = substances
        self.substances_mix = substances_mix

        self.model = LpProblem(name='DrugLinP', sense=LpMaximize)
        self.create_variables()
        self.create_constraints()
        self.create_objective()

    def create_variables(self):
        self.ammount_variables = LpVariable.dicts('ammount', self.substances['name'], lowBound=0, cat='Continuous')
        self.e = 0.7

    def create_constraints(self):
        self.model += pulp.lpSum([self.ammount_variables[substance] for substance in self.substances['name']]) == 1

        M = 100

        self.binary_variables = {}
        substances = self.substances['name'].values.tolist()
        for index, row in self.substances_mix.iterrows():
            for s in substances:
                x_var = LpVariable(name=f'x_{index}_{s}', lowBound=0, upBound=1, cat='Binary')
                y_var = LpVariable(name=f'y_{index}_{s}', lowBound=0, upBound=1, cat='Binary')
                self.model += self.ammount_variables[s] * M >= x_var    
                self.model += self.ammount_variables[index] * M >= y_var
                self.model += x_var >= self.ammount_variables[s]
                self.model += y_var >= self.ammount_variables[index]
                # print(x_var, y_var)

                # z = X AND Y
                z_var = LpVariable(name=f'z_{index}_{s}', lowBound=0, upBound=1, cat='Binary')
                self.model += z_var <= x_var
                self.model += z_var <= y_var
                self.model += z_var >= x_var + y_var - 1

                self.binary_variables[f'z_{index}_{s}'] = z_var

        print(self.binary_variables)

    def create_objective(self):
        self.model += pulp.lpDot([self.ammount_variables[substance] for substance in self.substances['name']], self.substances['cost'].values.tolist())

        efficacy = pulp.lpDot([self.ammount_variables[substance] for substance in self.substances['name']], self.substances['efficacy'].values.tolist())

        substances = self.substances['name'].values.tolist()
        for index, row in self.substances_mix.iterrows():
            for s in substances:
                efficacy += self.binary_variables[f'z_{index}_{s}'] * row[s]
                
        cost = pulp.lpDot([self.ammount_variables[substance] for substance in self.substances['name']], self.substances['cost'].values.tolist())

        self.model += self.e * efficacy - (1 - self.e) * cost
       
    def solve(self):
        self.model.solve(GLPK_CMD())
        return self.model

    def print(self):
        print('Status:', pulp.LpStatus[self.model.status])

        for v in self.model.variables():
            print(v.name, '=', v.varValue)

dl = SubstanceDataLoader('data/substances.csv')
substances, substances_mix = dl.data

# Print the resulting pairs
print(substances_mix)

lp = LPModel(substances, substances_mix)

lp.solve()
answer = lp.print()
print(answer)
print('Objective =', pulp.value(lp.model.objective))
