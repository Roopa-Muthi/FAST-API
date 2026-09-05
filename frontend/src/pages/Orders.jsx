import { useState } from "react";
import api from "../api/client";

export default function Orders() {
  const [form, setForm] = useState({
    customer_name: "",
    customer_email: "",
    product_id: "",
    quantity: "",
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleChange = (field, value) => {
    setForm({ ...form, [field]: value });
    // Clear old messages as soon as the user starts editing again
    if (result) setResult(null);
    if (error) setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    try {
      const res = await api.post("/orders/", {
        customer_name: form.customer_name,
        customer_email: form.customer_email,
        items: [
          {
            product_id: parseInt(form.product_id),
            quantity: parseInt(form.quantity),
          },
        ],
      });
      setResult(res.data);
      setForm({ customer_name: "", customer_email: "", product_id: "", quantity: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Order failed");
    }
  };

  return (
    <div>
      <h2>Place an Order</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Customer Name"
          value={form.customer_name}
          onChange={(e) => handleChange("customer_name", e.target.value)}
          required
        />
        <input
          placeholder="Customer Email"
          type="email"
          value={form.customer_email}
          onChange={(e) => handleChange("customer_email", e.target.value)}
          required
        />
        <input
          placeholder="Product ID"
          type="number"
          value={form.product_id}
          onChange={(e) => handleChange("product_id", e.target.value)}
          required
        />
        <input
          placeholder="Quantity"
          type="number"
          value={form.quantity}
          onChange={(e) => handleChange("quantity", e.target.value)}
          required
        />
        <button type="submit">Place Order</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && (
        <p style={{ color: "green" }}>
          Order #{result.id} — Status: {result.status}
        </p>
      )}
    </div>
  );
}