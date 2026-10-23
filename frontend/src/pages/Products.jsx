import { useState, useEffect } from "react";
import api from "../api/client";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", sku: "", price: "", description: "" });
  const [error, setError] = useState("");

  const fetchProducts = async () => {
    const res = await api.get("/products/");
    setProducts(res.data);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleChange = (field, value) => {
    setForm({ ...form, [field]: value });
    if (error) setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.post("/products/", {
        ...form,
        price: parseFloat(form.price),
      });
      setForm({ name: "", sku: "", price: "", description: "" });
      fetchProducts();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create product");
    }
  };

  return (
    <div>
      <h2>Products</h2>

      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => handleChange("name", e.target.value)}
          required
        />
        <input
          placeholder="SKU"
          value={form.sku}
          onChange={(e) => handleChange("sku", e.target.value)}
          required
        />
        <input
          placeholder="Price"
          type="number"
          step="0.01"
          value={form.price}
          onChange={(e) => handleChange("price", e.target.value)}
          required
        />
        <input
          placeholder="Description"
          value={form.description}
          onChange={(e) => handleChange("description", e.target.value)}
        />
        <button type="submit">Add Product</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>SKU</th>
            <th>Price</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.name}</td>
              <td>{p.sku}</td>
              <td>₹{p.price}</td>
              <td>{p.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}