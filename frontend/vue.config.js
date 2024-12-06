module.exports = {
  chainWebpack: (config) => {
    config.module
      .rule("js")
      .exclude.add(/node_modules/)
      .end()
      .use("babel-loader")
      .loader("babel-loader")
      .tap((options) => {
        return {
          presets: ["@babel/preset-env"],
        };
      });
  },
  transpileDependencies: ["lucide-vue-next"],
};
