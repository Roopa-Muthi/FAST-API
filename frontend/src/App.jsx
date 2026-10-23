import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { CartProvider, useCart } from "./context/CartContext";
import Storefront from "./pages/Storefront";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import OrderConfirmation from "./pages/OrderConfirmation";
import Products from "./pages/Products";
import Inventory from "./pages/Inventory";

function NavBar() {
  const { cartCount } = useCart();
  return (
    <nav style={{ marginBottom: "20px" }}>
      <Link to="/" style={{ marginRight: "15px" }}>Shop</Link>
      <Link to="/cart" style={{ marginRight: "15px" }}>Cart ({cartCount})</Link>
      <Link to="/admin/products" style={{ marginRight: "15px" }}>Admin: Products</Link>
      <Link to="/admin/inventory">Admin: Inventory</Link>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <CartProvider>
        <div style={{ maxWidth: "900px", margin: "0 auto", padding: "20px", fontFamily: "sans-serif" }}>
          <h1>Order & Inventory Management</h1>
          <NavBar />

          <Routes>
            <Route path="/" element={<Storefront />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/order-confirmation" element={<OrderConfirmation />} />
            <Route path="/admin/products" element={<Products />} />
            <Route path="/admin/inventory" element={<Inventory />} />
          </Routes>
        </div>
      </CartProvider>
    </BrowserRouter>
  );
}

export default App;