# -*- coding: utf-8 -*-
""" Queries to the DB
"""

from __future__ import absolute_import


def get_sqlite_data(name, plot_info):
    """Query the sqlite database"""
    # disable=no-member,no-name-in-module,import-error
    from import_db import automap_table, engine
    from sqlalchemy.orm import sessionmaker

    # configure Session class with desired options
    Session = sessionmaker(bind=engine)
    session = Session()

    Table = automap_table(engine)

    query = session.query(Table).filter_by(name=str(name))  # pylint:disable=no-member

    nresults = query.count()
    if nresults == 0:
        plot_info.text = 'No matching COF found.'
        return None
    return query.one()


def get_data_aiida(cif_uuid, plot_info):
    """Query the AiiDA database"""
    from figure.aiida import load_profile
    from aiida.orm import QueryBuilder, Dict, CifData

    load_profile()

    qb = QueryBuilder()
    qb.append(CifData,
              filters={'uuid': {
                  '==': cif_uuid
              }},
              tag='cifs',
              project='*')
    qb.append(
        Dict,
        descendant_of='cifs',
        project='*',
    )

    nresults = qb.count()
    if nresults == 0:
        plot_info.text = 'No matching COF found.'
        return None
    return qb.one()
