import itertools
import pandas as pd

# Create lists with the different factors.
rows = ['B', 'C', 'D', 'E' , 'F', 'G']
columns = range(2, 10 + 1)
#==============================================================================
# fields = range(1, 3 + 1)
# compartments = ['nuclei', 'cells', 'cytoplasm', 'bugs']
# channels = ['DAPI', 'Cy3', 'Cy5', 'FITC']
# cycles = range(1, 7 + 1)
#==============================================================================
# Generate a dataframe with all combinations of all factors (Cartesian product).
design = pd.DataFrame(list(itertools.product(
    rows, columns
)))
design.columns = ['row', 'column']

# Add some helpful columns that are made up by combining other factors.
# Don't need well because already in matlab output

#==============================================================================
# design['ChannelCycle'] = (
#     design['Channel']
#     + '-'
#     + design['Cycle'].astype(str).str.pad(4, fillchar='0')
# )
#==============================================================================

# Fill in the treatment base on a pattern on Row.
design.loc[design['row'].isin(['B']), 'drug'] = 'chlor_24h'
design.loc[design['row'].isin(['C']), 'drug'] = 'IFN_LPS'
design.loc[design['row'].isin(['D']), 'drug'] = 'IL4_IL13'
design.loc[design['row'].isin(['E']), 'drug'] = 'IL6'
design.loc[design['row'].isin(['F']), 'drug'] = 'Control'
design.loc[design['row'].isin(['G']) & design['column'].isin(['2', '3', '4', '5']), 'drug'] = 'LPS_3h'
design.loc[design['row'].isin(['G']) & design['column'].isin(['6', '7', '8', '9']), 'drug'] = 'chlor_3h'
# Deleted activation and MOI because not relavent


# Fill in the Marker by applying various patterns on Column.
# not necessary because written in Matlab

