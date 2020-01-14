import argparse
import yaml
import copy

class Order:
  def __init__(self, products = {}):
    self.products = products
  def update_order(self, product_name, shipped_quantity):
    self.products[product_name] -= shipped_quantity
class Warehouse:
  def __init__(self, name, inventory = {}):
    self.name = name
    self.inventory = inventory
  def update_inventory(self, product_name, quantity):
    if self.inventory[product_name] > quantity:
      self.inventory[product_name] -= quantity
      return quantity
    else:
      shipped_quantity = self.inventory[product_name]
      del self.inventory[product_name]
      return shipped_quantity 
class Shipment:
  def __init__(self, Shipment):
    self.shipment = {}
  def update_shipment(self, warehouse, product_name, quantity):
    if (self.shipment.get(warehouse) == None):
      self.shipment[warehouse] = {product_name: quantity}
    else:
      self.shipment[warehouse][product_name] = quantity
  def __repr__(self):
    for warehouse in self.shipment:
      return "{\'%s\': %s}" % (warehouse, self.shipment[warehouse])

class InventoryAllocator:
  def gen_warehouse_list(self, warehouses_init):
    warehouse_list = []
    for warehouse in warehouses_init:
      warehouse_list.append(Warehouse(warehouse["name"], warehouse["inventory"]))
    return warehouse_list
  def check_order_unsatisfied(self, order):
    return any(value != 0 for value in order.products.values())
  def gen_output(self, result_shipments):
    return [shipment.shipment for shipment in result_shipments if shipment]
  def cheapest_shipment(self, order_init, warehouse_list_init):
    order = Order(copy.deepcopy(order_init))
    warehouse_list = self.gen_warehouse_list(copy.deepcopy(warehouse_list_init))
    result_shipments = []    
    for warehouse in warehouse_list:
      shipment = Shipment({})
  # if this warehouse contains this product, create new Shipment object and update Order, Warehouse
      for product in order.products:
        if (product in warehouse.inventory) & (order.products[product] != 0) :
          shipped_quantity = warehouse.update_inventory(product, order.products[product])
          order.update_order(product, shipped_quantity)
          shipment.update_shipment(warehouse.name, product, shipped_quantity)
  # check is shipment empty
      if shipment.shipment:
        result_shipments.append(shipment)
    if self.check_order_unsatisfied(order):
      return []
    else:
      return self.gen_output(result_shipments)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-o","--order" ,type = yaml.load, required = True, help="order argument required in dictionary format, i.e.\"{ apple: 1 , orange: 5}\"")
  parser.add_argument("-s", "--storage" ,type = yaml.load, required = True, help="storage argument required in a list of dictionaries format, i.e.\"[{name: owd, inventory: { apple: 5} }, { name: dm, inventory: { orange: 5 }}]\"")
  args = parser.parse_args()
  # Enter InventoryAllocator class and do all the shipment calculations
  inventroy_allocator = InventoryAllocator()
  print(inventroy_allocator.cheapest_shipment(args.o, args.s))
