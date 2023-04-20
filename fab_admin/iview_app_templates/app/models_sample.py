"""
Created on {* now *}
@desc: Model sample
@app: {* app_name *}
"""
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.sql.sqltypes import BigInteger


class SampleBenchmark(Model):
    """Sample benchmark model."""

    __tablename__ = 'fab_sample'
    id = Column(Integer, Sequence('id'), primary_key=True)
    server = Column(String(255), nullable=False)
    ben_server = Column(String(255), nullable=False)
    operation = Column(String(255), nullable=False)
    site = Column(String(255), nullable=True)
    start = Column(BigInteger)
    end = Column(BigInteger)

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __repr__(self):
        return self.instance
