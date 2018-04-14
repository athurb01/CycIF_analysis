import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

data_directory = 'C:/Users/Amy Thurber/Dropbox (Partners HealthCare)/Experiments/FI13_matlab_out/matlab_output'
# go to data directory and load all 03h*.txt files into a single dataframe.
os.chdir(data_directory)

df = pd.concat([
    pd.read_table(path, sep = ',')
    for path in glob.glob('FI13_03h_20x_*.txt')
])
    

# add FOV column to easily separate by image location
df['FOV'] = (
    df['well']
    + df['field'].astype(str).str.pad(2, fillchar='0')
)


# add condition info from make_design_FI09
df = df.merge(design, left_on=['row','column'], right_on=['row','column'])

# assign markers 
df['marker'] = None
marker_map = {'rd1':
    [
    ['Hoechst', 'none', 'p50_CST', 'none'],
    ['Hoechst', 'none', 'RelA_CST', 'none'],
    ['Hoechst', 'none', 'p50_SC', 'RelA_SC'],
    ['Hoechst', 'none', 'p50_ab', 'none'],
    ['Hoechst', 'none', 'pRelA_CST', 'none'],
    ['Hoechst', 'none', 'JNK_ab', 'none'],
    ['Hoechst', 'none', 'STAT6_CST', 'none'],
    ['Hoechst', 'LAMP1_ab', 'none', 'RelA_ab']
    ]
}
marker_map['rd2'] = [
    ['Hoechst', 'none', 'p50_SC', 'none'],
    ['Hoechst', 'none', 'JNK_ab', 'RelA_ab'],
    ['Hoechst', 'none', 'IRF3_CST', 'IRF1_CST'],
    ['Hoechst', 'p_cJun', 'p38_CST', 'ERK_CST'],
    ['Hoechst', 'p_TBK1', 'STAT1_CST', 'none'],
    ['Hoechst', 'none', 'none', 'none'],
    ['Hoechst', 'none', 'none', 'none'],
    ['Hoechst', 'none', 'none', 'none']
]
marker_map['rd3'] = [
    ['Hoechst', 'p_38', 'p_STAT1', 'p_STAT6'],
    ['Hoechst', 'none', 'p_ERK', 'p_STAT3'],
    ['Hoechst', 'none', 'p_JNK', 'Cytc'],
    ['Hoechst', 'none', 'none', 'none'],
    ['Hoechst', 'none', 'none', 'none'],
    ['Hoechst', 'none', 'none', 'LC3'],
    ['Hoechst', 'none', 'none', 'none'],
    ['Hoechst', 'none', 'none', 'none']
]
columns = pd.unique(df['column'])
channels = pd.unique(df['channel'])
cycle_keys = list(marker_map.keys())
cycle = {'rd1': 1, 'rd2':2, 'rd3':3}

for r in cycle_keys:
    for c in range(0,8):
        for ch in range(0,4):
            idx = (df['column'] == columns[c]) & (df['channel'] == channels[ch]) & (df['round'] == cycle[r])
            df.loc[idx, 'marker'] = marker_map[r][c][ch]

# use groupby to get pop statistics of each FOV/marker
gb = df.groupby(['experiment', 'timepoint', 'well', 'field','round', 'marker',])

popMeans = gb.mean()
#get non-numerical data back
popMeans['drug'] = gb.first()['drug']
popMeans['row'] = gb.first()['row']


# select single channel and plot data
# make colors reflect column
sns.set(font_scale=1)
sns.set_style("white")
g = sns.stripplot(popMeans.loc[pd.IndexSlice[:,:,:,:,1, 'STAT6_CST'], 'drug'], popMeans.loc[pd.IndexSlice[:,:,:,:,1, 'STAT6_CST'], 'modeNuclei'], hue = popMeans.loc[pd.IndexSlice[:,:,:,:,1, 'STAT6_CST'], 'drug'],  jitter=True)
g.set_ylim([0,0.0125])
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.1)

#plt.savefig(r"C:\Users\Amy Thurber\Dropbox (Partners HealthCare)\Experiments\FI13_matlab_out\python_plots\p50_CST_rd1.png")

# make subplots for each marker
markers = set(x for l in marker_matrix_rd3 for x in l)


sns.set(font_scale=2)
sns.set_style("white")
fig, axs = plt.subplots(int(np.ceil(len(markers)/3)),3)
#axs.plot(label='big')
axs = axs.ravel()
count = 0
for m in markers:
    sns.stripplot(x = popMeans.loc[pd.IndexSlice[:,:,:,:,1, m], 'drug'], y = popMeans.loc[pd.IndexSlice[:,:,:,:,1, m], 'modeNuclei'], hue = popMeans.loc[pd.IndexSlice[:,:,:,:,1, m], 'drug'], data = popMeans, jitter=True, ax=axs[count])
    count = count + 1

#plt.savefig(r"C:\Users\Amy Thurber\Dropbox (Partners HealthCare)\Experiments\FI13_matlab_out\python_plots\bigMess.png")

favorite_measures = ['modeNuclei', 'intIntensityNuclei', 'modeCell', 'intIntensityCell']
# Jeremy's solution
for f in favorite_measures:
    for r in cycle_keys:
        markers = set(x for l in marker_map[r] for x in l)
        p = sns.factorplot(
        x='drug', y= f, col='marker', col_wrap=3, hue='drug',
        kind='strip', jitter=True, size=2.2, aspect=1.5, sharey = False,
    
        data=popMeans.loc[pd.IndexSlice[:,:,:,:,cycle[r],markers],:].reset_index('marker')
        )
        p.set_xticklabels(rotation=30)
        plt.tight_layout()
        name = 'FI13' + f + '_' + r
        plt.savefig(r"C:\Users\Amy Thurber\Dropbox (Partners HealthCare)\Experiments\FI13_matlab_out\python_plots\name.png")