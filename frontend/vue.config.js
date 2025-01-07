// vue.config.js
const webpack = require('webpack');
const path = require('path');

module.exports = {
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
        // 根据需要定义其他 Vue Feature Flags
        // 例如：
        // __VUE_OPTIONS_API__: true,
        // __VUE_PROD_DEVTOOLS__: false,
      }),
    ],
  },
  chainWebpack: config => {
    config.resolve.alias.set('@', path.resolve(__dirname, 'src'));
  },
};
