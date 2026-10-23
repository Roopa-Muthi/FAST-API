import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import api from "../api/client";

export default function Checkout() {
  const { cart, cartTotal, clearCart } = useCart();
  const navigate = useNavigate();

  const [form, setForm] = useState({ customer_name: "", customer_email: "" });
  const [error, setError] = useState("");
  const [placing, setPlacing] = useState(false);

  const handleChange = (field, value) => {
    setForm({ ...form, [field]: value });
    if (error) setError("");
  };

  const handlePlaceOrder = async (e) => {
    e.preventDefault();
    setError("");
    setPlacing(true);
    try {
      const res = await api.post("/orders/", {
        customer_name: form.customer_name,
        customer_email: form.customer_email,
        items: cart.map((item) => ({
          product_id: item.product_id,
          quantity: item.quantity,
        })),
      });
      clearCart();
      navigate("/order-confirmation", { state: { order: res.data } });
    } catch (err) {
      setError(err.response?.data?.detail || "Order failed");
    } finally {
      setPlacing(false);
    }
  };

  if (cart.length === 0) {
    return (
      <div>
        <h2>Checkout</h2>
        <p>Your cart is empty.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Checkout</h2>

      <h3>Order Summary</h3>
      <ul>
        {cart.map((item) => (
          <li key={item.product_id}>
            {item.name} × {item.quantity} = ₹{(item.price * item.quantity).toFixed(2)}
          </li>
        ))}
      </ul>
      <p style={{ fontWeight: "bold" }}>Total: ₹{cartTotal.toFixed(2)}</p>

      <form onSubmit={handlePlaceOrder}>
        <input
          placeholder="Your Name"
          value={form.customer_name}
          onChange={(e) => handleChange("customer_name", e.target.value)}
          required
        />
        <br />
        <input
          placeholder="Your Email"
          type="email"
          value={form.customer_email}
          onChange={(e) => handleChange("customer_email", e.target.value)}
          required
        />
        <br />
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={placing}>
          {placing ? "Placing Order..." : "Place Order"}
        </button>
      </form>
    </div>
  );
}