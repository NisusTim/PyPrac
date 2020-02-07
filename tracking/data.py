import pandas as pd
import numpy as np

np.arrays = [['one','one','one','two','two','two'],[1,2,3,1,2,3]]

df = pd.DataFrame(np.random.randn(6,2),index=pd.MultiIndex.from_tuples(list(zip(*np.arrays))),columns=['A','B'])

