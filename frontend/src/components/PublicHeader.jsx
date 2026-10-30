import { Link } from "react-router-dom";
import BrandMark from "./BrandMark.jsx";

export default function PublicHeader() {
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link to="/" className="brand-link">
          <BrandMark />
        </Link>
      </div>
    </header>
  );
}
