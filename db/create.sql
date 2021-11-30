-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE EXTENSION pgcrypto;

CREATE TABLE Account (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR NOT NULL
);

CREATE TABLE Balance (
    id UUID NOT NULL PRIMARY KEY REFERENCES Account(id),
    balance FLOAT(2) NOT NULL CHECK (balance >= 0)
);

CREATE TABLE Seller(
    id UUID PRIMARY KEY REFERENCES Account(id)
);

CREATE TABLE Product (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    price FLOAT(2) NOT NULL CHECK (price >= 0),
    available BOOLEAN DEFAULT TRUE,
    lister UUID REFERENCES Seller(id)
);

CREATE TABLE ProductInventory (
    product UUID NOT NULL REFERENCES Product(id),
    seller UUID NOT NULL REFERENCES Seller(id),
    quantity INT NOT NULL CHECK (quantity >= 0),
    PRIMARY KEY (product, seller)
);

CREATE TABLE Tag (
    id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(25) NOT NULL
);

CREATE TABLE ProductTag(
    tag INT NOT NULL REFERENCES Tag(id),
    product UUID NOT NULL REFERENCES Product(id),
    PRIMARY KEY (tag, product)   
);

CREATE TABLE ProductImage(
    product UUID NOT NULL PRIMARY KEY REFERENCES Product(id),
    url VARCHAR NOT NULL
);

CREATE TABLE CartProduct(
    account UUID NOT NULL REFERENCES Account(id),
    product UUID NOT NULL REFERENCES Product(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (account, product)
);

CREATE TABLE SavedProduct(
    account UUID NOT NULL REFERENCES Account(id),
    product UUID NOT NULL REFERENCES Product(id),
    PRIMARY KEY (account, product)
);

CREATE TABLE AccountOrder(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    account UUID REFERENCES Account(id),
    placed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE AccountOrderProduct(
    account_order UUID NOT NULL REFERENCES AccountOrder(id),
    product UUID NOT NULL REFERENCES Product(id),
    seller UUID NOT NULL REFERENCES Seller(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    price FLOAT(2) NOT NULL CHECK (price > 0),
    status VARCHAR(20) NOT NULL,
    shipped_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    delivered_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    PRIMARY KEY (account_order, product, seller)
);

CREATE TABLE Review(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    author UUID NOT NULL REFERENCES Account(id),
    title VARCHAR(50) NOT NULL,
    description VARCHAR NOT NULL,
    written_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    edited_at TIMESTAMP WITHOUT TIME ZONE,
    rating SMALLINT NOT NULL CHECK (rating >= 1 AND rating <= 5)
);

CREATE TABLE ReviewImage(
    review UUID NOT NULL PRIMARY KEY REFERENCES Review(id),
    url VARCHAR NOT NULL
);

CREATE TABLE ReviewVote(
    account UUID NOT NULL REFERENCES Account(id),
    review UUID NOT NULL REFERENCES Review(id),
    rating SMALLINT NOT NULL CHECK (rating = -1 OR rating = 1),
    PRIMARY KEY (account, review)
);

CREATE TABLE ProductReview(
    review UUID NOT NULL PRIMARY KEY REFERENCES Review(id),
    product UUID NOT NULL REFERENCES Product(id)
);

CREATE TABLE SellerReview(
    review UUID NOT NULL PRIMARY KEY REFERENCES Review(id),
    seller UUID NOT NULL REFERENCES Seller(id)
);

-- Trigger to create Balance on Account creation
CREATE FUNCTION TF_InitBalance() RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT id FROM Balance WHERE id = NEW.id) IS NOT NULL THEN
    RAISE EXCEPTION 'A balance already exists for account %.', NEW.id;
  END IF;

  INSERT INTO Balance (id, balance) VALUES(NEW.id, 0);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_InitBalance
AFTER INSERT ON Account
FOR EACH ROW
EXECUTE PROCEDURE TF_InitBalance();

-- Trigger to maintain availability field in Product during transactions
CREATE FUNCTION TF_WatchAvail() RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT SUM(quantity) FROM ProductInventory WHERE product = NEW.product GROUP BY product) = 0 AND
    (SELECT available FROM Product WHERE id = NEW.product) IS True THEN
    UPDATE Product SET available = False WHERE Product.id = NEW.product;
  ELSIF (SELECT SUM(quantity) FROM ProductInventory WHERE product = NEW.product GROUP BY product) <> 0 AND 
    (SELECT available FROM Product WHERE id = NEW.product) IS False THEN
    UPDATE Product SET available = True WHERE Product.id = NEW.product;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_WatchAvail
AFTER INSERT OR UPDATE ON ProductInventory
FOR EACH ROW
EXECUTE PROCEDURE TF_WatchAvail();

-- 
-- View that maps new db design to template schema. Should be replaced once python code is rewritten
-- 
CREATE VIEW Purchase AS
    SELECT AccountOrder.id AS id, AccountOrder.account AS uid, AccountOrderProduct.product AS pid, AccountOrder.placed_at AS time_purchased
    FROM AccountOrder, AccountOrderProduct
    WHERE AccountOrder.id = AccountOrderProduct.account_order;
