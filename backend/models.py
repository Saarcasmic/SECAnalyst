from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Company(Base):
    __tablename__ = 'companies'

    cik = Column(String, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String, nullable=True)

    metrics = relationship("FinancialMetric", back_populates="company")

    def __repr__(self):
        return f"<Company(cik='{self.cik}', ticker='{self.ticker}', name='{self.name}')>"

class FinancialMetric(Base):
    __tablename__ = 'financial_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_cik = Column(String, ForeignKey('companies.cik'), nullable=False)
    metric_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_period = Column(String, nullable=False) # e.g. FY, Q1, Q2, Q3
    form_type = Column(String, nullable=True) # e.g. 10-K, 10-Q

    company = relationship("Company", back_populates="metrics")

    def __repr__(self):
        return f"<FinancialMetric(metric='{self.metric_name}', val={self.value}, year={self.fiscal_year})>"
