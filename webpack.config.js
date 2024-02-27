const path = require('path');

module.exports = {
  mode: 'production',
  entry: './bulk_pay/js/index.js',
  output: {
    path: path.resolve(__dirname, 'bulk_pay', 'static'),
    filename: 'bulk_pay.bundle.js'
  }
};
