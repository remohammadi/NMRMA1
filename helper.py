from math import log2
from urllib.parse import urlparse

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


def source_analysis_cell_style(df, i, source_score_procontrol, source_score_anticontrol):
    if len(df) > i:
        base = 'width: 20em;'
        url = df.loc[i, 'url']
        domain = urlparse(url).netloc
        score_procontrol = log2(1 + source_score_procontrol[domain])
        score_anticontrol = log2(1 + source_score_anticontrol[domain])
        return (base + 'background: linear-gradient(to right, transparent 0%'
        ', transparent {pro:.1f}%, #97c4f0 {pro:.1f}%'
        ', #97c4f0 50%, #f78787 50%'
        ', #f78787 {anti:.1f}%, transparent {anti:.1f}%)').format(
            pro=(50 - score_procontrol * 50), anti=(50 + score_anticontrol * 50))
    return ''

def highlight_source_analysis_table(data, reviewed_search_results, source_score_procontrol, source_score_anticontrol):
    stop = min([len(x) for x in reviewed_search_results.values()])
    return pd.DataFrame(
        {k: pd.Series([source_analysis_cell_style(
            v, i, source_score_procontrol, source_score_anticontrol) for i in range(stop)])
        for (k, v) in reviewed_search_results.items()},
        index=data.index, columns=data.columns)

def visualize_source_analysis_results(reviewed_search_results, source_score_procontrol, source_score_anticontrol):
    stop = min([len(x) for x in reviewed_search_results.values()])
    vis_df = pd.DataFrame({k: pd.Series([cell_text(v, i) for i in range(stop)]) for (k, v) in reviewed_search_results.items()})
    return vis_df.style.set_table_styles(TABLE_STYLES).apply(highlight_source_analysis_table, reviewed_search_results=reviewed_search_results, source_score_procontrol=source_score_procontrol, source_score_anticontrol=source_score_anticontrol, axis=None)
