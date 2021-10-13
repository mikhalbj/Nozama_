\COPY Account FROM 'data/Account.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller FROM 'data/Seller.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Product FROM 'data/Product.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductInventory FROM 'data/ProductInventory.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductImage FROM 'data/ProductImage.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Tag FROM 'data/Tag.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductTag FROM 'data/ProductTag.csv' WITH DELIMITER ',' NULL '' CSV


\COPY CartProduct FROM 'data/CartProduct.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SavedProduct FROM 'data/SavedProduct.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Review FROM 'data/Review.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ReviewImage FROM 'data/ReviewImage.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductReview FROM 'data/ProductReview.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerReview FROM 'data/SellerReview.csv' WITH DELIMITER ',' NULL '' CSV


\COPY AccountOrder FROM 'data/AccountOrder.csv' WITH DELIMITER ',' NULL '' CSV
\COPY AccountOrderProduct FROM 'data/AccountOrderProduct.csv' WITH DELIMITER ',' NULL '' CSV
