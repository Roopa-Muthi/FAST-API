import { useState, useEffect } from "react";
import api from "../api/client";
import ProductCard from "../components/ProductCard";

export default function Storefront() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    api.get("/products/").then((res) => setProducts(res.data));
  }, []);

  return (
    <div>
      <h2>Shop</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
        {products.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}