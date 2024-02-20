tables_info = [
        {
            'index': 0,
            'header_skip': 2,
            'column_range': slice(1, 7),
            'columns': ['currency', 'bank_account', 'opening_balance', 'money_in', 'money_out', 'closing_balance', 'report_period'],
            'date_columns': ['report_period'],
            'table_name': 'e_money_movement'
        },
        {
            'index': 1,
            'header_skip': 2,
            'column_range': slice(1, 9),
            'columns': ['financial_instrument', 'isin', 'ticker', 'opening_balance', 'amount_in', 'amount_out', 'closing_balance', 'currency_of_issue', 'report_period'],
            'date_columns': ['report_period'],
            'table_name': 'e_financial_instruments_movement'
        },
        {
            'index': 2,
            'header_skip': 3,
            'column_range': slice(1, 16),
            'columns': ['order_number', 'order_date', 'passport_number', 'passport_date', 'settlement_date', 'trade_type', 'market', 'currency', 'isin', 'ticker', 'price', 'quantity', 'amount', 'interest_rate', 'accrued_interest', 'report_period'],
            'date_columns': ['order_date', 'passport_date', 'settlement_date', 'report_period'],
            'table_name': 'e_trade_documents'},
        {
            'index': 3,
            'header_skip': 3,
            'column_range': slice(1, 16),
            'columns': ['passport_number', 'opening_date', 'settlement_date', 'trade_type', 'market', 'currency', 'isin', 'ticker', 'opening_price', 'closing_price', 'quantity', 'opening_amount', 'closing_amount', 'interest_rate', 'accrued_interest', 'report_period'],
            'date_columns': ['opening_date', 'settlement_date', 'report_period'],
            'table_name': 'e_repo_documents'
        },
        {
            'index': 4,
            'header_skip': 2,
            'column_range': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13],
            'columns': ['order_number', 'date', 'order_type', 'payment_order', 'counterparty', 'isin', 'ticker', 'currency', 'price', 'quantity', 'amount', 'report_period'],
            'date_columns': ['date', 'report_period'],
            'table_name': 'e_orders'
        },
        {
            'index': 4,
            'header_skip': 2,
            'column_range': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13],
            'columns': ['order_number', 'date', 'order_type', 'payment_order', 'counterparty', 'isin', 'ticker',
                        'currency', 'price', 'quantity', 'amount', 'report_period'],
            'date_columns': ['date', 'report_period'],
            'table_name': 'e_orders'
        },
        {
            'index': 5,
            'header_skip': 2,
            'column_range': slice(1, 4),
            'columns': ['planned_balance', 'accrued_commission', 'unpaid_commission', 'report_period'],
            'date_columns': ['report_period'],
            'table_name': 'e_planned_balance'
        },
        {
            'index': 6,
            'header_skip': 3,
            'column_range': slice(1, 7),
            'columns': ['document_number', 'document_date', 'document_type', 'period', 'tariff', 'amount', 'report_period'],
            'date_columns': ['document_date', 'period', 'report_period'],
            'table_name': 'e_accrued_commissions'
        },
    ]