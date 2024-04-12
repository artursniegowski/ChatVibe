// context provides a way of sharing data between componenet without
// the need to pass props explicity like, in the other components.
// so by createing a context we have a central place to store and access certain
// types of data or functionnality methods
import React from "react";

// so basicaly what we do here is sahring the toggleColorMode
// between differnt compoenets so we can easily access it
interface ColorModeContextProps {
    toggleColorMode: () => void;
}
export const ColorModeContext = React.createContext<ColorModeContextProps>({
    toggleColorMode: () => {},
});