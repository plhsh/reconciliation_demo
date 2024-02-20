from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from db_config import get_engine

Base = declarative_base()


class EMoneyMovement(Base):
    __tablename__ = 'e_money_movement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String)
    bank_account = Column(String)
    opening_balance = Column(Numeric)
    money_in = Column(Numeric)
    money_out = Column(Numeric)
    closing_balance = Column(Numeric)
    report_period = Column(TIMESTAMP)


class EFinancialInstrumentsMovement(Base):
    __tablename__ = 'e_financial_instruments_movement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    financial_instrument = Column(String)
    isin = Column(String)
    ticker = Column(String)
    opening_balance = Column(Integer)
    amount_in = Column(Integer)
    amount_out = Column(Integer)
    closing_balance = Column(Integer)
    currency_of_issue = Column(String)
    report_period = Column(TIMESTAMP)


class ETradeDocuments(Base):
    __tablename__ = 'e_trade_documents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String)
    order_date = Column(TIMESTAMP)
    passport_number = Column(String)
    passport_date = Column(String)
    settlement_date = Column(TIMESTAMP)
    trade_type = Column(String)
    market = Column(String)
    currency = Column(String)
    isin = Column(String)
    ticker = Column(String)
    price = Column(Numeric)
    quantity = Column(Integer)
    amount = Column(Numeric)
    interest_rate = Column(Numeric)
    accrued_interest = Column(Numeric)
    report_period = Column(TIMESTAMP)


class ERepoDocuments(Base):
    __tablename__ = 'e_repo_documents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    passport_number = Column(String)
    opening_date = Column(TIMESTAMP)
    settlement_date = Column(TIMESTAMP)
    trade_type = Column(String)
    market = Column(String)
    currency = Column(String)
    isin = Column(String)
    ticker = Column(String)
    opening_price = Column(Numeric)
    closing_price = Column(Numeric)
    quantity = Column(Integer)
    opening_amount = Column(Numeric)
    closing_amount = Column(Numeric)
    interest_rate = Column(Numeric)
    accrued_interest = Column(Numeric)
    report_period = Column(TIMESTAMP)


class EOrders(Base):
    __tablename__ = 'e_orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String)
    date = Column(TIMESTAMP)
    order_type = Column(String)
    payment_order = Column(String)
    counterparty = Column(String)
    isin = Column(String)
    ticker = Column(String)
    currency = Column(String)
    price = Column(Numeric)
    quantity = Column(Integer)
    amount = Column(Numeric)
    report_period = Column(TIMESTAMP)


class EPlannedBalance(Base):
    __tablename__ = 'e_planned_balance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    planned_balance = Column(Numeric)
    accrued_commission = Column(Numeric)
    unpaid_commission = Column(Numeric)
    report_period = Column(TIMESTAMP)


class EAccruedCommissions(Base):
    __tablename__ = 'e_accrued_commissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_number = Column(String)
    document_date = Column(TIMESTAMP)
    document_type = Column(String)
    period = Column(TIMESTAMP)
    tariff = Column(String)
    amount = Column(Numeric)
    report_period = Column(TIMESTAMP)


def main():
    engine = get_engine()

    # Создание sessionmaker
    Session = sessionmaker(bind=engine)

    # Создание сессии
    with Session() as session:
        Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
    column_names = [column.name for column in EAccruedCommissions.__table__.columns]
    print(column_names)

