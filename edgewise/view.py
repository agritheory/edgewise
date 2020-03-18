from __future__ import annotations

import types
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

import edgedb
from attr import attrib, attrs, make_class


@attrs
class EdgeDBView:
    pass
