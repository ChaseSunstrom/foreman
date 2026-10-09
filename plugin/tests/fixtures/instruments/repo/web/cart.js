function applyDiscount(price, pct) {
  return price - (price * pct) / 100;
}

function subtotal(items) {
  return items.reduce((sum, it) => sum + it.price * it.qty, 0);
}

function cartTotal(cart) {
  const net = applyDiscount(subtotal(cart.items), cart.discount);
  return net * (1 + cart.tax.rate);
}

module.exports = { applyDiscount, subtotal, cartTotal };

if (require.main === module) {
  console.log(cartTotal({ items: [{ price: 10, qty: 2 }], discount: 0 }));
}
