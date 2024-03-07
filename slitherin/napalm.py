import napalm.package
import slitherin as slitherin


def entry_point():
    """This is the entry point for the napalm package.

    It provisions your detection modules and provides them to napalm.

    It returns a dictionary of Collections, keyed by the name of the collection.
    """
    _include = ("detectors",)

    return [
        collection
        for collection in napalm.package.entry_point(slitherin)
        if collection.collection_name in _include
    ]
