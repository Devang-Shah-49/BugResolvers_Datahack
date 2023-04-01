import { Navigate } from "react-router-dom";

const PrivateRoute = ({ component: Component }) => {
  // const isAuthorized = localStorage.getItem("access_token") !== null && localStorage.getItem("refresh_token") !== null
  const isAuthorized = localStorage.getItem("isAuthorized") && localStorage.getItem("appToken") !== null && localStorage.getItem("appUser") !== null;

  return isAuthorized ? <Component /> : <Navigate to="/login" />;
};

export default PrivateRoute;
