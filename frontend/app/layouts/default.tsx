import { NavLink, Outlet  ,Link} from "react-router";
import "./DefaultLayout.css";

export default function DefaultLayout() {
  const navLinkClass = ({ isActive }) =>
    isActive ? "nav-link active" : "nav-link";

  return (
    <main className="layout-container">
      
      <nav className="navbar">
        <img src="uploads/job.jpg" width="50" height = "50" ></img>
        <NavLink to="/" className={navLinkClass}>Home</NavLink>
        <NavLink to="/job-boards" className={navLinkClass}>JobBoards</NavLink>
      </nav>
      <Outlet/>
    </main>
  );
}