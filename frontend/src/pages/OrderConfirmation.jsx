import { useLocation, Link } from "react-router-dom";

export default function OrderConfirmation() {
  const location = useLocation();
  const order = location.state?.order;

  if (!order) {
    return (
      <div>
        <h2>No order found</h2>
        <Link to="/">Back to Shop</Link>
      </div>
    );
  }

  return (
    <div>
      <h2>Order Confirmed 🎉</h2>
      <p>Order #{order.id} — Status: {order.status}</p>
      <p>Thank you, {order.customer_name}! A confirmation email is on its way.</p>
      <Link to="/">Continue Shopping</Link>
    </div>
  );
}