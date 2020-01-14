import pytest
from inventoryallocator import InventoryAllocator, Order, Warehouse, Shipment
@pytest.fixture
def inventory_allocator():
  return InventoryAllocator()

@pytest.fixture
def empty_order():
    '''Returns a Order instance with empty dict'''
    return {}

@pytest.fixture
def single_product_order_5():
  '''Returns a Order instance with single product'''
  return {"apple": 5}

@pytest.fixture
def single_product_order_10():
  '''Returns a Order instance with single product'''
  return {"apple": 10}
  
@pytest.fixture
def mul_products_order():
  '''Returns a Order instance with multiple products'''
  return {"apple": 5, "orange": 5, "berry": 30}

@pytest.fixture
def empty_warehouse():
  return []

@pytest.fixture
def warehouse():
  return [{ "name": "owd", "inventory": {'apple': 5, 'orange': 5, 'berry': 30}}]

@pytest.fixture
def mul_warehouses():
  return [{ "name": "owd", "inventory": { "apple": 5} }, { "name": "dm", "inventory": { "apple": 5, "orange": 5 }},{"name": "Dan", "inventory": { "berry": 40} }]

def test_update_order(single_product_order_5, mul_products_order):
  order = Order(single_product_order_5)
  order.update_order("apple", 2)
  assert order.products == {"apple": 3}
  mul_order = Order(mul_products_order)
  mul_order.update_order("berry", 30)
  assert mul_order.products == {"apple": 5, "orange": 5, "berry": 0}

def test_update_inventory():
  w = Warehouse("owd", {'apple': 5, 'orange': 5, 'berry': 30})
  # enough in warehouse
  w.update_inventory("apple", 1)
  assert w.inventory ==  { "apple": 4, 'orange': 5, 'berry': 30}
  # not enough in warehouse, return all in warehouse, delete key
  assert w.update_inventory("apple", 6) == 4
  assert w.inventory == { 'orange': 5, 'berry': 30}

def test_gen_warehouse_list(inventory_allocator, warehouse, mul_warehouses):
  for w in inventory_allocator.gen_warehouse_list(warehouse):
    assert w.name == "owd"
    assert w.inventory == {'apple': 5, 'orange': 5, 'berry': 30}
  for mul_w in inventory_allocator.gen_warehouse_list(mul_warehouses):
    assert mul_w.name in ["owd", "dm", "Dan"]
    assert mul_w.inventory in [{ "apple": 5}, { "apple": 5, "orange": 5 }, { "berry": 40}]

def test_gen_output(inventory_allocator):
  shipment = Shipment({})
  shipment.update_shipment("dm" ,"apple" ,5)
  assert inventory_allocator.gen_output([shipment]) == [{"dm":{"apple": 5}}]

def test_check_order_unsatisfied(inventory_allocator, single_product_order_10, warehouse):
  assert inventory_allocator.cheapest_shipment(single_product_order_10, warehouse) == []

def test_empty_order(inventory_allocator, empty_order, warehouse):
  assert inventory_allocator.cheapest_shipment(empty_order, warehouse) == []

def test_empty_warehouses(inventory_allocator, single_product_order_5, empty_warehouse):
  assert inventory_allocator.cheapest_shipment(single_product_order_5, empty_warehouse) == []

def test_single_order_single_warehouse(single_product_order_5, warehouse, inventory_allocator):
  assert inventory_allocator.cheapest_shipment(single_product_order_5, warehouse) == [{'owd': {'apple': 5}}]

def test_single_product_order_mul_warehouses(inventory_allocator, single_product_order_10, mul_warehouses):
  assert inventory_allocator.cheapest_shipment(single_product_order_10, mul_warehouses) == [{'owd': {'apple': 5}}, {'dm': {'apple': 5}}]

def test_mul_products_order_single_warehouse(inventory_allocator,mul_products_order, warehouse):
  assert inventory_allocator.cheapest_shipment(mul_products_order, warehouse) == [{'owd': {'apple': 5, 'orange': 5, 'berry': 30}}]

def test_mul_products_order_mul_warehouses(inventory_allocator,mul_products_order, mul_warehouses):
  assert inventory_allocator.cheapest_shipment(mul_products_order, mul_warehouses) == [{'owd': {'apple': 5}}, {'dm': {'orange': 5}}, {'Dan': {'berry': 30}}]

def test_mul_products_order_mul_warehouses_unsatisfied(inventory_allocator, mul_warehouses):
  assert inventory_allocator.cheapest_shipment({"apple": 60}, mul_warehouses) == []
  assert inventory_allocator.cheapest_shipment({"pineapple": 60}, mul_warehouses) == []