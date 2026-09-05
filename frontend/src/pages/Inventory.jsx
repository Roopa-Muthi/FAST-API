import { useState } from "react";
import api from "../api/client";

export default function Inventory() {
  const [form, setForm] = useState({ product_id: "", quantity_available: "" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    try {
      const res = await api.post("/inventory/", {
        product_id: parseInt(form.product_id),
        quantity_available: parseInt(form.quantity_available),
      });
      setResult(res.data);
      setForm({ product_id: "", quantity_available: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add inventory");
    }
  };

  return (
    <div>
      <h2>Add Inventory</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Product ID"
          type="number"
          value={form.product_id}
          onChange={(e) => setForm({ ...form, product_id: e.target.value })}
          required
        />
        <input
          placeholder="Quantity Available"
          type="number"
          value={form.quantity_available}
          onChange={(e) => setForm({ ...form, quantity_available: e.target.value })}
          required
        />
        <button type="submit">Add Stock</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && (
        <p style={{ color: "green" }}>
          Stock added: Product {result.product_id} now has {result.quantity_available} units
        </p>
      )}
    </div>
  );
}