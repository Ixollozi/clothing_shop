import { createBrowserRouter } from "react-router";
import { Root } from "./components/Root";
import { Home } from "./components/Home";
import { About } from "./components/About";
import { Catalog } from "./components/Catalog";
import { Product } from "./components/Product";
import { Cart } from "./components/Cart";
import { Checkout } from "./components/Checkout";
import { FAQ } from "./components/FAQ";
import { NotFound } from "./components/NotFound";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      { index: true, Component: Home },
      { path: "about", Component: About },
      { path: "catalog", Component: Catalog },
      { path: "product/:id", Component: Product },
      { path: "cart", Component: Cart },
      { path: "checkout", Component: Checkout },
      { path: "faq", Component: FAQ },
      { path: "*", Component: NotFound },
    ],
  },
]);
