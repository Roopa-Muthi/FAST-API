import { useState } from "react";
import { useCart } from "../context/CartContext";
import { checkAvailability } from "../api/client";

export default function ProductCard({ product }) {
  const { addToCart } = useCart();
  const [stockMsg, setStockMsg] = useState("");
  const [checking, setChecking] = useState(false);

  const handleCheckAvailability = async () => {
    setChecking(true);
    setStockMsg("");
    try {
      const data = await checkAvailability(product.id);
      setStockMsg(`${data.available} in stock`);
    } catch (err) {
      setStockMsg(err.response?.data?.detail || "Unable to check stock");
    } finally {
      setChecking(false);
    }
  };

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "16px",
        width: "220px",
        display: "flex",
        flexDirection: "column",
        gap: "8px",
      }}
    >
      <h3 style={{ margin: 0 }}>{product.name}</h3>
      <p style={{ margin: 0, color: "#666", fontSize: "14px" }}>{product.description}</p>
      <p style={{ margin: 0, fontWeight: "bold" }}>₹{product.price}</p>

      <button onClick={handleCheckAvailability} disabled={checking}>
        {checking ? "Checking..." : "Check Availability"}
      </button>
      {stockMsg && <p style={{ margin: 0, fontSize: "13px" }}>{stockMsg}</p>}

      <button onClick={() => addToCart(product)}>Add to Cart</button>
    </div>
  );
}