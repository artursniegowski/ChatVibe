import { useFormik } from "formik";
import { useNavigate } from "react-router-dom";
import { useAuthServiceContext } from "../context/AuthContext";
import { Box, Button, Container, TextField, Typography } from "@mui/material";

const Register = () => {
   // Function to validate email format
   const isValidEmail = (email: string) => {
        // Regular expression for email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const { register } = useAuthServiceContext();
    const navigate = useNavigate();
    const formik = useFormik({
        initialValues: {
            email: "",
            password: "",
        },
        validate: (values) => {
            // the partial indicates that errors should conform to the type
            // where all properties of values are optional
            const errors: Partial<typeof values> = {};
            // check if values have been typed in
            if (!values.email) {
                errors.email = "Email is required";
            } else if (!isValidEmail(values.email)){
                errors.email = "Invalid email address";
            };
            if (!values.password) {
                errors.password = "Password is required";
            };
            return errors;
        },
        onSubmit: async (values) => {
            const {email, password} = values;
            const responseStatus = await register(email, password);
            if ( responseStatus === 409 ){
                console.log("409: CONFLICT");
                formik.setErrors({
                    email: "Invalid email",
                });  
            } else if ( responseStatus === 400 ){
                console.log("400: Bad Request");
                formik.setErrors({
                    email: "Invalid email",
                });  
            } else if (responseStatus === 401) {
                console.log("401: Unauthorized");
                formik.setErrors({
                    email: "Invalid email or password",
                    password: "Invalid email or password",
                });
            } else {
                // after they are signed up
                // if no error occured we want to navigate the user to the login page
                navigate("/login");
            };
        },
    });

    return (
        <Container component="main" maxWidth="xs">
            <Box sx={{
                    marginTop: 8 , 
                    display: "flex", 
                    alignItems: "center", 
                    flexDirection: "column",
                    }}
            >
                <Typography 
                    variant="h5"
                    noWrap
                    component="h1"
                    sx={{
                        fontWeight: 500,
                        pb: 2,
                    }}
                >
                    Register
                </Typography>
                <Box component="form" onSubmit={formik.handleSubmit}
                    sx={{ mt: 1}}
                >
    
                    <TextField 
                        autoFocus
                        fullWidth
                        id="email" 
                        name="email"
                        label="email" 
                        value={formik.values.email}
                        onChange={formik.handleChange}
                        error={!!formik.touched.email && !! formik.errors.email}
                        helperText={formik.touched.email && formik.errors.email} 
                    >
                    </TextField>
                    <TextField
                        margin="normal" 
                        fullWidth
                        id="password" 
                        name="password"
                        label="password"  
                        type="password" 
                        value={formik.values.password}
                        onChange={formik.handleChange}
                        error={!!formik.touched.password && !! formik.errors.password}
                        helperText={formik.touched.password && formik.errors.password} 
                    >
                    </TextField>
                    <Button variant="contained" disableElevation type="submit"
                        sx={{ mt:1, mb:2}}
                    >
                        Next
                    </Button>
                </Box>
            </Box>
        </Container>
    );
};
export default Register;