\COPY Users FROM 'data/Account.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/Product.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/AccountOrder.csv' WITH DELIMITER ',' NULL '' CSV
