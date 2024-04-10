import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,  // Listen on all network interfaces
    port: 3000,  // Use the default port 3000
    // add the next lines if you're using windows and hot reload doesn't work
    // https://github.com/vitejs/vite/issues/1153
    // TODO: probably NOT needed for production
    watch: {
        usePolling: true
    },
    hmr: {
      clientPort: 3000
    },
  },
})