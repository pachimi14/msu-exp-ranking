import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// GitHub Pages project site: https://<user>.github.io/<repo>/
const repoName = process.env.GITHUB_REPOSITORY?.split("/")[1];
const pagesBase =
  process.env.GITHUB_PAGES === "true" && repoName ? `/${repoName}/` : "/";

export default defineConfig({
  base: pagesBase,
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
