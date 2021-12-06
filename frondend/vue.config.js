const path = require("path");

function resolve(dir) {
  return path.join(__dirname, dir);
}

module.exports = {
  devServer: {
    proxy: {
      '/': {
        target: 'http:localhost:5000',
        changeOrigin: true
      }
    }
  }
}
