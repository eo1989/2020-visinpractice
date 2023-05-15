# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # One Vis Tool to Rule Them All
#
# Matt Harrison (@\__mharrison__)
#
# https://github.com/mattharrison/2020-visinpractice
#
# ## Outline
#
# * Intro
# * Categorical Plot
# * Continuous Plot
# * Continuous - Continuous Plot
# * Continuous - Categorical Plot
# * Categorical - Categorical Plot
# * Styling
# * Summary
#

# > Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics. - seaborn.pydata.org
#
# * Leverages Matplotlib and Pandas
# * Has common plots
# * Has styling tooling
# * Has a gallery on website

# ## Installation
#
#     pip/conda install seaborn

# ## Setup/Data

# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.reset_defaults()

url = 'https://github.com/mattharrison/datasets/raw/master/data/ames-housing-dataset.zip'
df = pd.read_csv(url)
df

with pd.option_context('min_rows', 60):
    print(df.dtypes)

# ## Categorical

df.select_dtypes(object)

sns.reset_defaults()
neighborhood = sns.countplot(x='Neighborhood', data=df)
# print(neighborhood)

sns.countplot(y='Neighborhood', data=df)

fig, ax = plt.subplots(figsize=(10,6))
sns.countplot(y='Neighborhood', data=df, ax=ax, order=sorted(df.Neighborhood.unique()))

fig, ax = plt.subplots(figsize=(10,6))
sns.countplot(y='Neighborhood', data=df, ax=ax, order=df.Neighborhood.value_counts().index)

# +
catplot = sns.catplot(y='Neighborhood',
                      data=df,
                      order=df.Neighborhood.value_counts().index,
                      kind='count',
                      col='Yr Sold',
                      col_wrap=2)

plt.show(catplot)
# -

# ## Continuous

sns.kdeplot(x='SalePrice', data=df)

sns.displot(x='SalePrice', data=df, rug=True)

sns.displot(x='SalePrice', data=df, rug=True, aspect=1.6)

import matplotlib.ticker as tc
grid = sns.displot(x='SalePrice', data=df, rug=True, aspect=1.6)
grid.axes[0][0].xaxis.set_major_locator(tc.FixedLocator([0, 50_000, 200_000, 500_000]))
grid.axes[0][0].xaxis.set_ticklabels('0,50k,200k,500k'.split(','))

import matplotlib.ticker as tc
grid = sns.displot(x='SalePrice', data=df, rug=True, aspect=1.6, 
                   col='Yr Sold', col_wrap=2)
plt.show(grid)



# ## 2D Cont-cont

sns.lmplot(x='SalePrice', y='1st Flr SF', data=df)

sns.relplot(x='SalePrice', y='1st Flr SF', data=df)

sns.relplot(x='SalePrice', y='1st Flr SF', data=df, col='Yr Sold', col_wrap=2)



# ## 2D Cont-cat

sns.catplot(y='Neighborhood', x='SalePrice', data=df)

sns.catplot(y='Neighborhood', x='SalePrice', data=df, kind='violin', order=['NAmes','Gilbert', 'GrnHill', 'Veenker'])

grid = sns.catplot(y='Neighborhood', x='SalePrice', data=df, kind='box', order=['NAmes','Gilbert', 'GrnHill', 'Veenker'])
grid.set_xticklabels(step=2)


grid = sns.catplot(y='Neighborhood', x='SalePrice', data=df, kind='boxen', order=['NAmes','Gilbert', 'GrnHill', 'Veenker'],
                  col='Yr Sold', col_wrap=2)
grid.set_xticklabels(step=2)




# ## 2D Cat-Cat

(df
 .pipe(lambda df_: pd.crosstab(df_['Yr Sold'], df_['Sale Condition']))
 .plot.bar(stacked=True)
)

(df
 .pipe(lambda df_: pd.crosstab(df_['Yr Sold'], df_['Sale Condition']))
 .pipe(lambda df_: df_.div(df_.sum(axis=1), axis=0))
 .plot.bar(stacked=True)
 .legend(bbox_to_anchor=(1,1))
)




# ## Styling

# +
color_palette = ["#440154", "#482677", "#404788", "#33638d", "#287d8e", "#1f968b",
                '#29af7f', '#55c667', '#73d055', '#b8de29', '#fde725']

sns.set(font='Lato')
style_dict = {'font.family': 'sans-serif', 
              'font.sans-serif': ['Lato'],
              'axes.facecolor': 'white',
              'grid.color': '#c0c0c0',
              'axis.grid': True}
# To set font must use sns.set_style
sns.set_style(style_dict)
sns.set_context('talk')

with sns.color_palette('viridis'):
    pd.Series(range(10)).plot.barh(title='Yr Sold')

sns.palplot(color_palette)

# +
style_dict = {'font.family': 'sans-serif',
 'font.sans-serif': ['Lato'],
 'axes.facecolor': 'white',
 'grid.color': '#c0c0c0',
 'axis.grid': True}
sns.set_style(style_dict) # font can't be set in context manager :(

with sns.plotting_context('talk'):
    with sns.color_palette('viridis'):
        ax = (df
         .pipe(lambda df_: pd.crosstab(df_['Yr Sold'], df_['Sale Condition']))
         .pipe(lambda df_: df_.div(df_.sum(axis=1), axis=0))
         .fillna(0)
         .plot.bar(stacked=True)
        )
        ax.legend(bbox_to_anchor=(1,1))
        ax.set_title('Condition Percentages per Year')

# -

with sns.plotting_context('talk'):
    with sns.color_palette('viridis'):     
        grid = sns.relplot(x='SalePrice', y='1st Flr SF', data=df.sample(500, random_state=42), 
                           hue='Yr Sold', palette='viridis', alpha=.5)

# fix ticks - adjusting step is like using range (taking every 2nd tick)
with sns.plotting_context('talk'):
    with sns.color_palette('viridis'):     
        grid = sns.relplot(x='SalePrice', y='1st Flr SF', data=df.sample(500, random_state=42), 
                           hue='Yr Sold', palette='viridis', alpha=.5)
        grid.fig.suptitle('Sale Price against Square Footage')
        plt.subplots_adjust(top=.9)  # don't overlap title
        grid.set_xticklabels(step=2)  # need to do it in two calls...
        grid.set_xticklabels(labels=['$0', '400k', '800k'])
        grid.set_xlabels('Sales Price ($)')
        plt.text(x=400_000, y=4_000, s='Comparing sales in Ames, Iowa', fontsize=10, ha='center')
        plt.text(x=950_000, y=-300, s='@__mharrison__', fontsize=10)
        txt = '''A data set describing the sale of individual residential property in Ames, Iowa from 2006 to 2010. 
The data set contains 2930 observations and a large number of explanatory variables (23 nominal, 
23 ordinal, 14 discrete, and 20 continuous) involved in assessing home values. '''
        plt.text(x=-100_000, y=-1200, s=txt, fontsize=10, ha='left', )
        

[f'${int(val.get_position()[0]/1000)}k' for val in grid.axes.flat[0].get_xticklabels()]#, '400k', '800k'])

# fix ticks - adjusting step is like using range (taking every 2nd tick)
# using list comprehension to avoid error...
neighborhoods = ['NAmes','Gilbert', 'GrnHill', 'Veenker']
data = df.query('Neighborhood.isin(@neighborhoods)')
with sns.plotting_context('talk'):
    with sns.color_palette('viridis'):     
        grid = sns.relplot(x='SalePrice', y='1st Flr SF', data=data,
                           hue='Neighborhood', hue_order=neighborhoods,
                           palette='viridis', alpha=.5, aspect=1.3)
        grid.fig.suptitle('Sale Price against Square Footage')
        grid.set_xlabels('Sales Price ($)')
        plt.subplots_adjust(top=.9)  # don't overlap title
        grid.set_xticklabels(step=2)  # need to do it in two calls...
        grid.set_xticklabels(labels=[f'{int(val.get_position()[0]/1000)}k' for val in grid.axes.flat[0].get_xticklabels()]),
        plt.text(x=data['SalePrice'].max()/2, y=data['1st Flr SF'].max(), s='Comparing sales in Ames, Iowa', fontsize=10, ha='center')
        plt.text(x=data['SalePrice'].max() + 100_000, y=data['1st Flr SF'].min()-500, s='@__mharrison__', fontsize=10)
        txt = '''A data set describing the sale of individual residential property in Ames, Iowa from 2006 to 2010. 
The data set contains 2930 observations and a large number of explanatory variables (23 nominal, 
23 ordinal, 14 discrete, and 20 continuous) involved in assessing home values. '''
        plt.text(x=50_000, y=data['1st Flr SF'].min()-800, s=txt, fontsize=10, ha='left', )
        

with sns.plotting_context('notebook'):
    with sns.color_palette('viridis'):
        
        grid = sns.relplot(x='SalePrice', y='1st Flr SF', data=df.sample(2000, random_state=42), hue='Yr Sold', palette='viridis', alpha=.5,
                          col='Neighborhood', col_order=['NAmes','Gilbert', 'GrnHill', 'Veenker'], col_wrap=2)
        grid.fig.suptitle('Sale Price against SF')
        grid.set_xlabels('Sales Price ($)')        
        plt.subplots_adjust(top=.9)  # don't overlap title


# +
df2 = (df
      .assign(color=np.where(df.Neighborhood == 'NWAmes', 'NWAmes', 'Other')))

with sns.plotting_context('talk'):
    grid = sns.catplot(y='Neighborhood', data=df2, order=df.Neighborhood.value_counts().index[:10],
                       kind='count', legend=False,
                       palette={'NWAmes': '#fed726', 'Other': '#bbbbbb'},
                       hue='color', dodge=False,  # dodge required for non-shifting
                       col='Yr Sold', col_wrap=2, col_order=[2006, 2007,2008,2009],
                       aspect=1.6
                      )

    grid.fig.suptitle('Number of Neigborhood Sales')
    plt.subplots_adjust(top=.9)  # don't overlap title
# -

# alternate view of above
neighborhoods = ['NAmes', 'OldTown', 'NWAmes', 'SawyerW', 'CollgCr']
data = (df
        .groupby(['Yr Sold','Neighborhood'])
        .size()
        .unstack()
        .loc[:,neighborhoods]
       )
pal = {n:'#bbb' for n in neighborhoods}
pal['NWAmes'] = '#fed726'
with sns.plotting_context('talk'):
    fig, ax = plt.subplots(figsize=(10,6))
    ax = sns.lineplot(data=data,
                      ax=ax,
                      palette=pal,
                      dashes=False,
                      legend=False,
                      )
    ax.yaxis.set_ticks(range(0, 101, 20))
    ax.xaxis.set_ticks(range(2006, 2011))
    fig.suptitle('Number of Neigborhood Sales')
    sns.despine()
    year = 2010
    for label in neighborhoods:
        ax.text(year+.1, data.loc[year:,label], label, fontsize=8)


# pd.crosstab(index=df['Yr Sold'], columns=df['Neighborhood']).loc[:, neighborhoods]
neighborhoods = ['NAmes', 'OldTown', 'NWAmes', 'SawyerW', 'CollgCr']
data = (df
        .groupby(['Yr Sold','Neighborhood'])
        .size()
        .unstack()
        .loc[:,neighborhoods]
       )
data

# ## Summary
#
# Pros:
# * Good for static images (books, presentations, etc)
# * Seaborn does a decent job out of the box
# * Can facet easily
# * Handles many standard continuous and categorical plots
#
# Cons:
# * No interactivity
# * Need to understand some Matplotlib to tweak
# * Font's hard to use (Matplotlib feature)
#
# https://github.com/mattharrison/2020-visinpractice
#
# Follow me on my newsletter to learn Python, Vis, and More https://matthewharrison.podia.com
