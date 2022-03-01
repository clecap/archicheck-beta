const path = require("path");
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  entry: {
    background: "./js/background.js",
    crypto: "./js/crypto.js",
    options: "./js/options.js",
    subscribeFactChecker: "./js/subscribeFactChecker.js",
    factChecksForWebsite: "./js/factChecksForWebsite.js",
    publishNewFactCheck: "./js/publishNewFactCheck.js",
    myPublishedFactChecks: "./js/myPublishedFactChecks.js",
    createAccount: "./js/createAccount.js",
    canonize: "./js/canonize.js",
    popup: "./js/popup.js",
    deleteAccount: "./js/deleteAccount.js",
    unsubscribeFactChecker: "./js/unsubscribeFactChecker.js",
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].js",
  },
  resolve: {
    extensions: [".js", ""],
  },
  plugins: [
    new CopyPlugin({
      patterns: [{ from: "./ui" }],
    }),
  ],
};
