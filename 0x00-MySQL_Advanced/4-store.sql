-- Create trigger to decrease quantity after adding a new order
DELIMITER //

CREATE TRIGGER after_new_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  UPDATE items
  SET quantity = quantity - NEW.number
  WHERE items.name = NEW.item_name;
END//

DELIMITER ;