"""Acquisition of raw source data, one module per source.

``SOURCE_MODULES`` is the registry. Its order is the order in which sources
are acquired and reported; it is fixed so that runs are reproducible.
"""

SOURCE_MODULES = (
    "randi2023",
    "white1986",
    "witvliet2021",
    "fenyves2020",
    "ripollsanchez2023",
    "taylor2021",
    "bentley2016",
    "canonical_neurons",
)
