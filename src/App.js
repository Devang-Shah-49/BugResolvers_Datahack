import {
  BrowserRouter as Router,
  Routes,
  Navigate,
  Route,
} from "react-router-dom";
import Landing from "./components/Landing";
import Login from "./components/login";
import Signup from "./components/signup";
import PrivateRoute from './helpers/PrivateRoutes/PrivateRoute';
import UserPage from "./components/userPage";
import UserChart from "./components/UserChart";
import PopChat from "./components/PopupChat";

function App() {
  return (
    <div>
      <Router>
          <Routes>
            <Route path="/" element={<Navigate replace to="/landing" />} />
            <Route exact path="/login" element={<Login />} />
            <Route exact path="/signup" element={<Signup />} />
            <Route exact path="/landing" element={<Landing />} />
            <Route exact path="/user" element={<UserPage/>} />

            {/* <Route exact path="/dashboard" element={<PrivateRoute component={Login} />} >
              <Route index element={<PrivateRoute component={Landing} />} />
              <Route exact path="landing" element={<PrivateRoute component={Landing} />} />
              <Route exact path="doctor/bulk-create" element={<Landing />} />
            </Route> */}
            <Route path="*" element={<Navigate replace to="/landing" />} />
          </Routes>          
          <h1>User Dashboard </h1>
          <UserChart/>
          <PopChat/>
        </Router>
    </div>
  );
}

export default App;