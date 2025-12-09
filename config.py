PROBLEMS = {
  'two_sum': {
      'func_name_correct': 'two_sum_correct',
      'func_name_buggy': 'two_sum_buggy',
      'schema': {
         'nums': {'type':'int_list', 'min_len':2, 'max_len':100, 'min_val': -10**9, 'max_val': 10**9},
         'target': {'type':'int', 'min_val': -10**9, 'max_val': 10**9}
      }
  },
}

GA_DEFAULTS = {
  'population_size': 50,
  'generations': 50,
  'crossover_prob': 0.8,
  'mutation_prob': 0.15,
  'elitism': 2,
}
