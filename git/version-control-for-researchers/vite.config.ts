import { defineConfig } from 'vite'

export default defineConfig(({ command }) => ({
  // Slidev's `export` command spins up a dev server but always navigates
  // assuming base "/", so only apply the deployed subpath during `build`.
  base: command === 'build' ? '/version-control-for-researchers/' : '/',
}))

