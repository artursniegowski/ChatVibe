import { useFormik } from "formik";
import { useNavigate } from "react-router-dom";
import { useAuthServiceContext } from "../context/AuthContext";

const Login = () => {
    const { login } = useAuthServiceContext();
    const navigate = useNavigate();
    const formik = useFormik({
        initialValues: {
            email: "",
            password: "",
        },
        onSubmit: async (values) => {
            const {email, password} = values;
            const res = await login(email, password);
            if (res) { // if error occurs
                console.log(res);
            } else {
                navigate("/testlogin");
            }
        },
    });

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={formik.handleSubmit}>
                <label>email</label>
                <input 
                    id="email" 
                    name="email" 
                    type="text" 
                    value={formik.values.email}
                    onChange={formik.handleChange} 
                >
                </input>
                <label>password</label>
                <input 
                    id="password" 
                    name="password" 
                    type="password" 
                    value={formik.values.password}
                    onChange={formik.handleChange} 
                >
                </input>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};
export default Login;