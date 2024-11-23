select *
from SourcesTemp s
where source GLOB "*[^a-zA-Z &,--'/]*";