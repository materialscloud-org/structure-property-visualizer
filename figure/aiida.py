# -*- coding: utf-8 -*-
"""Functions for loading AiiDA environment from environment variables.

See also the Dockerfile.
"""
import os


def update_config():
    """Add AiiDA profile from environment variables, if specified"""
    from aiida.manage.configuration import load_config
    from aiida.manage.configuration.profile import Profile

    profile_name = os.getenv('AIIDA_PROFILE')
    config = load_config(create=True)
    if profile_name and profile_name not in config.profile_names:
        profile = Profile(
            profile_name, {
                'database_hostname':
                os.getenv('AIIDADB_HOST'),
                'database_port':
                os.getenv('AIIDADB_PORT'),
                'database_engine':
                os.getenv('AIIDADB_ENGINE'),
                'database_name':
                os.getenv('AIIDADB_NAME'),
                'database_username':
                os.getenv('AIIDADB_USER'),
                'database_password':
                os.getenv('AIIDADB_PASS'),
                'database_backend':
                os.getenv('AIIDADB_BACKEND'),
                'default_user':
                os.getenv('default_user_email'),
                'repository_uri':
                'file://{}/.aiida/repository/{}'.format(
                    os.getenv('AIIDA_PATH'), profile_name),
            })
        config.add_profile(profile)
        config.set_default_profile(profile_name)
        config.store()

    return config


def load_profile():
    """Load AiiDA profile according to environment variables."""
    import aiida

    update_config()
    aiida.load_profile()
