#!/usr/bin/env python
"""
file: errors
author: adh
created_at: 8/24/21 2:43 PM
"""


class LabyrinthError(Exception):
    pass


class LabyrinthFileProcessorError(LabyrinthError):
    pass


class LabyrinthDirHelperError(LabyrinthError):
    pass


class LabyrinthDateHelperError(LabyrinthError):
    pass


class LabyrinthPatternError(LabyrinthError):
    pass


class LabyrinthRateLimitError(LabyrinthError):
    pass


class LabyrinthSearchError(LabyrinthError):
    pass
