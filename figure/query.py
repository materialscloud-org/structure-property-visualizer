# -*- coding: utf-8 -*-
"""Querying the DB
"""
from bokeh.models.widgets import RangeSlider, CheckboxButtonGroup
from .config import max_points
# pylint: disable=too-many-locals
data_empty = dict(x=[0], y=[0], uuid=['1234'], color=[0], name=['no data'])


def get_data_sqla(projections, sliders_dict, quantities, plot_info):
    """Query database using SQLAlchemy.

    Note: For efficiency, this uses the the sqlalchemy.sql interface which does
    not go via the (more convenient) ORM.
    """
    from import_db import automap_table, engine
    from sqlalchemy.sql import select, and_

    Table = automap_table(engine)

    selections = []
    for label in projections:
        selections.append(getattr(Table, label))

    filters = []
    for k, v in sliders_dict.items():
        if isinstance(v, RangeSlider):
            if not v.value == quantities[k]['range']:
                f = getattr(Table, k).between(v.value[0], v.value[1])
                filters.append(f)
        elif isinstance(v, CheckboxButtonGroup):
            if not len(v.active) == len(v.labels):
                f = getattr(Table, k).in_([v.tags[i] for i in v.active])
                filters.append(f)

    s = select(selections).where(and_(*filters))

    results = engine.connect().execute(s).fetchall()

    nresults = len(results)
    if not results:
        plot_info.text = 'No matching COFs found.'
        return data_empty
    elif nresults > max_points:
        results = results[:max_points]
        plot_info.text = '{} COFs found.\nPlotting {}...'.format(
            nresults, max_points)
    else:
        plot_info.text = '{r} COFs found.\nPlotting {r}...'.format(r=nresults)

    # x,y position
    x, y, clrs, names, filenames = list(zip(*results))
    x = list(map(float, x))
    y = list(map(float, y))

    if projections[2] == 'bond_type':
        #clrs = map(lambda clr: bondtypes.index(clr), clrs)
        clrs = list(map(str, clrs))
    else:
        clrs = list(map(float, clrs))

    return dict(x=x, y=y, filename=filenames, color=clrs, name=names)


def get_data_aiida(projections, sliders_dict, quantities, plot_info):
    """Query the AiiDA database"""
    from figure.aiida import load_profile
    from aiida.orm import QueryBuilder, Dict

    load_profile()

    filters = {}

    def add_range_filter(bounds, label):
        # a bit of cheating until this is resolved
        # https://github.com/aiidateam/aiida_core/issues/1389
        #filters['attributes.'+label] = {'>=':bounds[0]}
        filters['attributes.' + label] = {
            'and': [{
                '>=': bounds[0]
            }, {
                '<': bounds[1]
            }]
        }

    for k, v in sliders_dict.items():
        # Note: filtering is costly, avoid if possible
        if not v.value == quantities[k]['range']:
            add_range_filter(v.value, k)

    qb = QueryBuilder()
    qb.append(
        Dict,
        filters=filters,
        project=['attributes.' + p
                 for p in projections] + ['uuid', 'extras.cif_uuid'],
    )

    nresults = qb.count()
    if nresults == 0:
        plot_info.text = 'No matching COFs found.'
        return data_empty

    plot_info.text = '{} COFs found. Plotting...'.format(nresults)

    # x,y position
    x, y, clrs, uuids, names, cif_uuids = list(zip(*qb.all()))
    plot_info.text = '{} COFs queried'.format(nresults)
    x = list(map(float, x))
    y = list(map(float, y))
    cif_uuids = list(map(str, cif_uuids))
    uuids = list(map(str, uuids))

    if projections[2] == 'bond_type':
        #clrs = map(lambda clr: bondtypes.index(clr), clrs)
        clrs = list(map(str, clrs))
    else:
        clrs = list(map(float, clrs))

    return dict(x=x, y=y, uuid=cif_uuids, color=clrs, name=names)
