from sanic import Blueprint
from .ipfs import ipfs
from .heartbeat import heartbeat
from .cdms import cdms
from .tables import tables
from .columns import columns
from .values import values
from .alexa import alexa

api_v1 = Blueprint.group(
  ipfs,
  cdms,
  heartbeat,
  tables,
  columns,
  values,
  alexa,
  url_prefix='/v1'
)