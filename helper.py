import pandas as pd
import numpy as np


PROGRAM_STYLES = {
    'Balanced': 'background-color: #babdb6; color: #000',
    'Pro-Control': 'background-color: #204a87; color: #fff',
    'Anti-Control': 'background-color: #a40000; color: #fff',
    'todo': 'background-color: #ce5c00; color: #fff;',
    np.NaN: 'background-color: #fff; color: #555753',
}
TABLE_STYLES = [
    dict(selector="th", props=[("text-align", "center")]),
    dict(selector="td", props=[("text-align", "center")]),
]

def cell_text(df, i):
    if len(df) > i:
        title = df.loc[i, 'source title']
        typ = df.loc[i, 'type']
        return '{title}<br>({type})'.format(title=title, type=typ)
    return ''

def cell_style(df, i):
    if len(df) > i:
        program = df.loc[i, 'program']
        return PROGRAM_STYLES[program]
    return ''

def highlight_table(data, reviewed_search_results):
    stop = min([len(x) for x in reviewed_search_results.values()])
    return pd.DataFrame({k: pd.Series([cell_style(v, i) for i in range(stop)]) for (k, v) in reviewed_search_results.items()},
        index=data.index, columns=data.columns)

def visualize_reviewed_search_results(reviewed_search_results):
    stop = min([len(x) for x in reviewed_search_results.values()])
    vis_df = pd.DataFrame({k: pd.Series([cell_text(v, i) for i in range(stop)]) for (k, v) in reviewed_search_results.items()})
    return vis_df.style.set_table_styles(TABLE_STYLES).apply(highlight_table, reviewed_search_results=reviewed_search_results, axis=None)
