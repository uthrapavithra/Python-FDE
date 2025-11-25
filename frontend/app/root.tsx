import {
  isRouteErrorResponse,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "react-router";

import type { Route } from "./+types/root";
import "./app.css";



export default function App() {
  return( <html>
    <head>
      <title>Jobify</title>
    </head>
    <body>
      <Outlet></Outlet>
    </body>
  </html>);
}

