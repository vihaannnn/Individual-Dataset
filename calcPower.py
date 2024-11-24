
def calc_power():
  """
  Function to calculate power analysis of the data
  Args - N/A
  Output - Power Analysis
  """
  from math import sqrt 
  from statsmodels.stats.power import TTestPower 
  # factors for power analysis 
  d = 0.5
  alpha = 0.05
  power = 0.8
    
  # perform power analysis to find sample size  
  # for given effect 
  obj = TTestPower() 
  n = obj.solve_power(effect_size=d, alpha=alpha, power=power, alternative='two-sided') 
    
  print('Sample size/Number needed in each group: {:.3f}'.format(n))

def main():
  calc_power()
if __name__ == '__main__':
  main()
