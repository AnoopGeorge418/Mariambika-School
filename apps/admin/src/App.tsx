import { Route, Routes } from "react-router";
import Login from "./features/auth/login";

const App = () => {
	return (
        <Routes>
            <Route path="/" element={ <Login /> } />
		</Routes>
	);
};

export default App;
